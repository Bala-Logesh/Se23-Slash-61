import requests
import unittest
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",  # noqa: E501
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1",
}


class TestAPI(unittest.TestCase):
    searchTerm = "dell laptops"

    def test_server(self):
        self.assertEqual(
            requests.get("http://localhost:8000", headers=headers).status_code,
            200,
            "Server is not up and running",
        )

    # def test_amazon(self):
    #     response = json.loads(
    #         requests.get(
    #             "http://localhost:8000/az/" + self.searchTerm,
    #             headers=headers,
    #         ).text
    #     )
    #     assert response is None or (response is not None and len(response) > 0)

    def test_walmart(self):
        response = json.loads(
            requests.get(
                "http://localhost:8000/wm/" + self.searchTerm,
                headers=headers,
            ).text
        )
        assert response is None or (response is not None and len(response) > 0)

    def test_bestbuy(self):
        response = json.loads(
            requests.get(
                "http://localhost:8000/bb/" + self.searchTerm,
                headers=headers,
            ).text
        )
        assert response is None or (response is not None and len(response) > 0)

    # def test_target(self):
    #     response = json.loads(
    #         requests.get(
    #             "http://localhost:8000/tg/" + self.searchTerm,
    #             headers=headers,
    #         ).text
    #     )
    #     assert response is None or (response is not None and len(response) > 0)

    def test_costco(self):
        response = json.loads(
            requests.get(
                "http://localhost:8000/cc/" + self.searchTerm,
                headers=headers,
            ).text
        )
        assert response is None or (response is not None and len(response) > 0)

    def test_ebay(self):
        response = json.loads(
            requests.get(
                "http://localhost:8000/eb/" + self.searchTerm,
                headers=headers,
            ).text
        )
        assert response is None or (response is not None and len(response) > 0)


if __name__ == "__main__":
    unittest.main()
