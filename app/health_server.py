from http.server import ThreadingHTTPServer
from app import health_api


def run():
    server_address = ("127.0.0.1", 8000)
    handler_class = health_api.make_health_handler()
    httpd = ThreadingHTTPServer(server_address, handler_class)

    print("Server running on http://127.0.0.1:8000 ... Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    # Keep the established command while loading the composed auth runtime.
    from app.runtime import main

    main()
