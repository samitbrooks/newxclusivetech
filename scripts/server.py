import http.server
import os
import socketserver
import sys

PORT = 8000

class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        translated = super().translate_path(path)
        # If the path doesn't exist and has no extension, check if an .html file exists
        if not os.path.exists(translated) and not translated.endswith('/'):
            if os.path.exists(translated + '.html'):
                return translated + '.html'
        # If it's a directory without trailing slash, redirect or check index.html
        if os.path.isdir(translated) and not path.endswith('/'):
            index_html = os.path.join(translated, 'index.html')
            if os.path.exists(index_html):
                return index_html
        return translated

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    with socketserver.TCPServer(("", port), CleanURLHandler) as httpd:
        print(f"Server with Clean URLs running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
