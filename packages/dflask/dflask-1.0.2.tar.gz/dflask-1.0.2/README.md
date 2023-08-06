# Direct-Flask

Use responses for Flask directly

## Installation

### From PyPI

```sh
pip3 install dflask
```

### From GitHub

```sh
pip3 install git+https://github.com/donno2048/Direct-Flask
```

## Usage

```py
from dflask import DirectFlask, Response
app = DirectFlask(__name__)
app.add_response("/", Response("<html><head><link href='/style.css' rel='stylesheet'></head><body></body></html>"))
app.add_response("/style.css", "body{background-color: red;}").run()
```
