"""
json rpc helper
"""

import socket
from json import dumps, loads
from uuid import uuid4

from sanic.log import logger


def jsonrpc(data: dict, host: str = "localhost", port: int = 7583):
    """
    json rpc connection
    """
    request_id = str(uuid4())
    data.update({"jsonrpc": "2.0", "id": request_id})
    recv_buffer = []
    sock_type = socket.AF_INET
    sock_conn = (host, port)
    if host.startswith("unix://"):
        sock_type = socket.AF_UNIX
        sock_conn = host.replace("unix://", "")
    with socket.socket(sock_type, socket.SOCK_STREAM) as sock:
        try:
            sock.connect(sock_conn)
            sock.settimeout(10)
            sock.sendall(dumps(data).encode("utf-8"))
            sock.shutdown(socket.SHUT_WR)
            while True:
                chunk = sock.recv(1)
                recv_buffer.append(chunk)
                if chunk == b"\n":
                    res = loads(b"".join(recv_buffer).decode("utf-8"))
                    recv_buffer = []
                    if res.get("id") == request_id:
                        return res
        except Exception as err:
            error = getattr(err, "message", repr(err))
            logger.error(error)
            raise
