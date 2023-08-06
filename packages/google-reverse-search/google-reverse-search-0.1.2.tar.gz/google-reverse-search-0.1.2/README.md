# google-reverse-search
Simple python3 library to reverse search any image via url or file

## Installation

install with `setup.py`:

    python setup.py

install from `pip`:

    pip install google-reverse-search

## Example Usage:

```py
from GoogleSearch import Search

#file_path example
output = Search(file_path="home/user/Pictures/image.jpg")
#url example
output = Search(url="https://telegra.ph/file/2018f3575ffa4ae93739b.jpg")
print(output)

#sample output
{'s_image': 'https://www.google.com/search?tbm=isch&q=zero+two+chilling', 'output': 'Results for\xa0zero two chilling'}
```

## Credits
This library was inspired from this [stackoverflow](http://stackoverflow.com/questions/23270175/ddg#28792943) discussion.

## NOTE

Google might change their working function any time, that day this library may work or not, so when you face any error please open issue [here](https://github.com/Black-Bulls-Bots/google-reverse-search/issues).