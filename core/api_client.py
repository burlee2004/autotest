import requests
from core.logger import get_logger

logger = get_logger("api_client")


class APIClient:
    def __init__(self, base_url, headers=None, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        self.default_headers = {
            "Content-Type": "application/json"
        }

        if headers:
            self.default_headers.update(headers)

    def _build_url(self, endpoint):
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def _log_request(self, method, url, **kwargs):
        logger.info(f"[API REQUEST] {method.upper()} {url}")

        headers = kwargs.get("headers")
        params = kwargs.get("params")
        json_data = kwargs.get("json")
        data = kwargs.get("data")

        if headers:
            logger.info(f"[API REQUEST HEADERS] {headers}")
        if params:
            logger.info(f"[API REQUEST PARAMS] {params}")
        if json_data is not None:
            logger.info(f"[API REQUEST JSON] {json_data}")
        if data is not None:
            logger.info(f"[API REQUEST DATA] {data}")

    def _log_response(self, response):
        logger.info(f"[API RESPONSE] status_code={response.status_code}")
        try:
            logger.info(f"[API RESPONSE BODY] {response.text}")
        except Exception:
            logger.info("[API RESPONSE BODY] <không đọc được response body>")

    def request(self, method, endpoint, **kwargs):
        url = self._build_url(endpoint)

        custom_headers = kwargs.pop("headers", {})
        timeout = kwargs.pop("timeout", self.timeout)

        final_headers = {**self.default_headers, **custom_headers}

        try:
            self._log_request(method, url, headers=final_headers, **kwargs)

            response = self.session.request(
                method=method,
                url=url,
                headers=final_headers,
                timeout=timeout,
                **kwargs
            )

            self._log_response(response)
            return response

        except requests.RequestException as e:
            logger.exception(f"[API ERROR] {method.upper()} {url} - {str(e)}")
            raise

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)