import unittest
import requests
import logging
import webbrowser
import re
from unittest.mock import MagicMock, patch, call
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

    @patch('webbrowser.open_new_tab')
    @patch('readwise_shortlist.requests.Response.json')
    def test_process_response_non_hn_url(self, mock_json, mock_open_new_tab):
        # Mock a JSON response containing both Hacker News and non-Hacker News URLs
        mock_json.return_value = {
            "results": [
                {
                    "summary": "Comments URL: https://news.ycombinator.com/item?id=12345",
                    "url": "https://example-hn.com/article1"
                },
                {
                    "summary": "A regular article",
                    "url": "https://example-non-hn.com/article2"
                }
            ]
        }

        response = requests.Response()
        response.status_code = 200
        response.headers['Content-Type'] = 'application/json'

        process_response(response)

        # Check if the webbrowser.open_new_tab is called with the correct URLs
        expected_urls = [
            "https://news.ycombinator.com/item?id=12345",
            "https://example-non-hn.com/article2"
        ]
        mock_open_new_tab_calls = [call(url) for url in expected_urls]
        mock_open_new_tab.assert_has_calls(mock_open_new_tab_calls, any_order=True)


if __name__ == '__main__':
    unittest.main()
