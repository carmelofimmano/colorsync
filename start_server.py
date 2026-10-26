import http.server
import socketserver
import socket
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # niente cache vecchia sui telefoni durante i test
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


if __name__ == "__main__":
    local_ip = get_local_ip()
    local_url = f"http://{local_ip}:{PORT}"

    print("=" * 60)
    print(" ColorSync Server Avviato con successo!")
    print("=" * 60)
    print(f"\n [Telefono 1 e Telefono 2] Connettiti al Wi-Fi e apri nel browser:\n -> {local_url}")
    print(f"\n [Computer locale] Puoi aprirlo anche da PC su:\n -> http://localhost:{PORT}")
    print("=" * 60)

    with Server(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer arrestato.")
