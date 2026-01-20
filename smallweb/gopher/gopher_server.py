#!/usr/bin/env python3
"""
Simple gopher server for testing.
Serves files from /var/gopher directory.
"""

import socketserver
import os
import sys
from pathlib import Path

GOPHER_ROOT = "/var/gopher"
HOST = "0.0.0.0"
PORT = 7070


class GopherHandler(socketserver.StreamRequestHandler):
    """Simple gopher protocol handler."""

    def handle(self):
        """Handle a gopher request."""
        try:
            # Read the selector (path) from client
            selector = self.rfile.readline().decode('utf-8').strip()

            # Default to root if empty
            if not selector or selector == "/":
                selector = "/gophermap"

            # Security: prevent directory traversal
            selector = selector.lstrip('/')
            filepath = os.path.normpath(os.path.join(GOPHER_ROOT, selector))

            if not filepath.startswith(GOPHER_ROOT):
                self.send_error("Access denied")
                return

            # Check if it's a directory
            if os.path.isdir(filepath):
                gophermap = os.path.join(filepath, "gophermap")
                if os.path.exists(gophermap):
                    filepath = gophermap
                else:
                    self.send_error("Directory listing not available")
                    return

            # Serve the file
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    content = f.read()
                    self.wfile.write(content)
                    # Gopher protocol requires terminator
                    if not content.endswith(b'\n.\n'):
                        self.wfile.write(b'\n.\n')
            else:
                self.send_error("File not found")

        except Exception as e:
            print(f"Error handling request: {e}", file=sys.stderr)
            self.send_error(str(e))

    def send_error(self, message):
        """Send an error message to the client."""
        error_msg = f"3Error: {message}\r\n.\r\n"
        self.wfile.write(error_msg.encode('utf-8'))


class GopherServer(socketserver.TCPServer):
    """Gopher server with SO_REUSEADDR."""
    allow_reuse_address = True


def main():
    """Run the gopher server."""
    print(f"Starting gopher server on {HOST}:{PORT}")
    print(f"Serving files from: {GOPHER_ROOT}")

    # Check if gopher root exists
    if not os.path.exists(GOPHER_ROOT):
        print(f"Error: {GOPHER_ROOT} does not exist")
        sys.exit(1)

    try:
        with GopherServer((HOST, PORT), GopherHandler) as server:
            print("Gopher server is running...")
            server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down gopher server...")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
