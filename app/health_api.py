from collections.abc import Callable, Mapping
from http.server import BaseHTTPRequestHandler
import json


def default_health_check() -> dict[str, str]:
    return {"status": "ok"}


def make_health_handler(
    health_func: Callable[[], object] = default_health_check,
) -> type[BaseHTTPRequestHandler]:
    class HealthHandler(BaseHTTPRequestHandler):
        timeout = 2

        def _send_json_response(
            self,
            status_code: int,
            data: object,
            extra_headers: Mapping[str, str] | None = None,
        ) -> None:
            try:
                body_bytes = json.dumps(data).encode("utf-8")
            except Exception:
                status_code = 500
                body_bytes = b'{"error":"Internal server error"}'

            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body_bytes)))

            if extra_headers:
                for key, val in extra_headers.items():
                    self.send_header(key, val)
            self.end_headers()
            self.wfile.write(body_bytes)

        def handle_request(self, method: str) -> None:
            if self.path != "/health":
                self._send_json_response(404, {"error": "Not found"})
                return

            if method == "GET":
                try:
                    result = health_func()
                except Exception:
                    self._send_json_response(500, {"error": "Internal server error"})
                    return
                self._send_json_response(200, result)

            else:
                self._send_json_response(405, {"error": "Method not allowed"}, extra_headers={"Allow": "GET"})

        def do_GET(self) -> None:
            self.handle_request("GET")

        def do_PUT(self) -> None:
            self.handle_request("PUT")

        def do_POST(self) -> None:
            self.handle_request("POST")

    return HealthHandler
