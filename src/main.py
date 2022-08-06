import socket
import os

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


def get_upstream_info_from_env():
    upstream_db = {
        "web.localhost": {
            "pool": ["localhost:8081", "localhost:8082", "localhost:8083"]
        },

        "default": {
            "pool": ["localhost:8081", "localhost:8082", "localhost:8083"]
        }
    }

    counter = 0
    while 1:
        upstream = os.environ.get(f"UPSTREAM-{counter}", None)
        if not upstream:
            break

        """
        Upstream is a:
        {"domain": "app.localhost", "pool": ["host_1:port_1", "host_2:port_2", "host_3:port_3"], "default": 1}
        """

        counter += 1

    return upstream_db


HOST, PORT = os.environ.get("HOST", ""), os.environ.get("PORT", 80)
UPSTREAMS = get_upstream_info_from_env()


def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)
    print('Serving HTTP on port {PORT} ...')

    while True:
        client_connection, client_address = listen_socket.accept()
        p = HttpParser()
        body = []
        raw_request = b""

        while True:
            request_data = client_connection.recv(1024)
            raw_request += request_data

            if not request_data:
                break

            recved = len(request_data)
            nparsed = p.execute(request_data, recved)

            assert recved == nparsed

            if p.is_partial_body():
                body.append(p.recv_body())

            if p.is_message_complete():
                break

        addressed_host = p.get_headers()["Host"]

        http_response = b"""
        HTTP/1.1 200 OK
        bebra
        """
        client_connection.sendall(http_response)
        client_connection.close()


if __name__ == "__main__":
    main()
