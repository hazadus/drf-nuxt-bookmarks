from typing import List

import requests
from bs4 import BeautifulSoup


def parse_url_info(url: str) -> List[str]:
    """
    Parse meta tag contents from `url`.
    Reference: https://stackoverflow.com/questions/36768068/get-meta-tag-content-property-with-beautifulsoup-and-python
    """
    request = requests.get(url)
    html = BeautifulSoup(request.content, "html.parser")

    title = html.title.string
    description = html.find("meta", property="og:description")
    image_url = html.find("meta", property="og:image")

    return [
        title if title else "No title set",
        description["content"] if description else "",
        image_url["content"] if image_url else "",
    ]
