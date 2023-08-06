from typing import Any, Dict, Union
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

def Search(file_path: str = None, url: str = None) -> Union[Dict, Any]:
    """Function to reverse search image on google with file or url

    Args:
        file_path (str, optional): File path to use for search. Defaults to None.
        url (str, optional): Url to use for search. Defaults to None.

    Raises:
        ValueError: Raises when both url and file_path are provided or not.

    Returns:
        Union[Dict, Any]: Returns a dict of similar image url and output name
    """
    
    headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}

    if file_path and url:
        raise ValueError("Please provide either file_path or url only, not both")

    elif isinstance(file_path, str) and not url:
        try:
            searchUrl = 'http://www.google.com/searchbyimage/upload'
            multipart = {'encoded_image': (file_path, open(file_path, 'rb')), 'image_content': ''}
            response = requests.post(searchUrl, files=multipart, allow_redirects=False)
            fetchUrl = response.headers['location']

            r = requests.get(fetchUrl, headers=headers)

            soup = BeautifulSoup(r.text, 'html.parser')

            result = {                            
                "similar": '',
                'output': ''
            }

            for similar_image in soup.find_all('input', {'class': 'gLFyf'}):
                url = f"https://www.google.com/search?tbm=isch&q={quote_plus(similar_image.get('value'))}"
                result['similar'] = url
            for best in soup.find_all('div', {'class': 'r5a77d'}):
                result['output'] = best.get_text()
        except (FileNotFoundError, PermissionError):
            raise
            

        return result
    
    elif isinstance(url, str) and not file_path:
        searchUrl = 'https://www.google.com/searchbyimage' + '?image_url=' + url

        r = requests.get(searchUrl, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')

        result = {                            
            "similar": '',
            'output': ''
        }

        for similar_image in soup.find_all('input', {'class': 'gLFyf'}):
            url = f"https://www.google.com/search?tbm=isch&q={quote_plus(similar_image.get('value'))}"
            result['similar'] = url
        for best in soup.find_all('div', {'class': 'r5a77d'}):
            result['output'] = best.get_text(strip=True)
        
        return result
    

    elif not file_path and not url:
        raise ValueError("Either file_path or url value is required.")
        