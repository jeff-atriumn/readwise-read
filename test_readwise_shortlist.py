import unittest
import requests
import logging
from unittest.mock import MagicMock, patch
from readwise_shortlist import load_config, get_readwise_shortlist, process_response, logger

class TestReadwiseShortlist(unittest.TestCase):

    def test_load_config(self):
        config = load_config('config.ini')
        self.assertIsNotNone(config.get('readwise', 'api_token'))

    @patch('readwise_shortlist.requests.get')
    def test_get_readwise_shortlist(self, mock_get):
        # Mock a successful API response
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api_token = "TEST TOKEN"
        response = get_readwise_shortlist(api_token)
        self.assertIsNotNone(response)

        # Mock a 500 Internal Server Error response
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = get_readwise_shortlist(api_token)
        self.assertIsNotNone(response)

    def test_process_response_200(self):
        response = requests.Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'
        response._content = b'{"example": "data", "results": []}'
        try:
            process_response(response)
        except Exception as e:
            self.fail(f"process_response() raised {type(e).__name__} unexpectedly")

    def test_process_response_500(self):
        response = requests.Response()
        response.status_code = 500
        response.headers['Content-Type'] = 'application/json'
        response._content = b'{"error": "Internal Server Error"}'
        with self.assertLogs(logger, level=logging.INFO) as log:
            process_response(response)
            self.assertIn("500 Internal Server Error", log.output[0])

    def test_process_response_400(self):
        response = requests.Response()
        response.status_code = 400
        response.headers['Content-Type'] = 'application/json'
        response._content = b'{"error": "Bad Request"}'
        with self.assertLogs(logger, level=logging.INFO) as log:
            process_response(response)
            self.assertIn("unexpected status code: 400", log.output[0])

if __name__ == '__main__':
    unittest.main()
