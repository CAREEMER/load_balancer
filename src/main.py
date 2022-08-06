import socket
import os

try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser


HOST, PORT = os.getenv("HOST", ""), os.getenv("PORT", 80)


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
