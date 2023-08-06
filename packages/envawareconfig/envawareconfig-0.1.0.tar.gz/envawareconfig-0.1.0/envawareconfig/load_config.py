import io
import os

import dotenv
import yaml

from .expand_variables import expand_variables


def load_config(file: str) -> dict:
    with open(file, "rt") as f:
        text = f.read()

    dotenv.load_dotenv()
    context = dict(os.environ)
    text = expand_variables(text=text, context=context)

    properties = yaml.safe_load(io.StringIO(text))
    return properties
