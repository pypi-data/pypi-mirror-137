# Flask-APIAlchemy

Flask-APIAlchemy is an extension for [Flask](https://palletsprojects.com/p/flask/), modeled after [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com), that adds support for [APIAlchemy](https://github.com/homedepot/apialchemy) to your application. It aims to simplify using APIAlchemy with Flask.

## Installation

```
pip install Flask-APIAlchemy
```

## A Simple Example

Output the contents of a file located in a GitHub repository:

```python
from flask import Flask
from flask_apialchemy import APIAlchemy

app = Flask(__name__)
app.config['APIALCHEMY_SERVICE_URI'] = 'github://apikey@github.com'
aa = APIAlchemy(app)

kwargs = {
    'org': 'org_name',
    'repo': 'repo_name',
    'path': 'path/to/file'
}

file_contents = aa.service.get_file_contents(aa.service.client, **kwargs)

print(file_contents)
```

## License

Distributed under the [BSD 3-Clause license](https://opensource.org/licenses/BSD-3-Clause).