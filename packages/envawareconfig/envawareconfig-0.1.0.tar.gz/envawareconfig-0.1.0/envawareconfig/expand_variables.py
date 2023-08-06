import re
from typing import Optional

from .errors import MissingEnvVarError

env_var_regexp = re.compile(r"\${.*?}")


def expand_variables(text: str, context: dict) -> str:
    match = re.search(pattern=env_var_regexp, string=text)
    while match is not None:
        identifier, default = _extract_identifier_and_default(match.group())
        replacement = context.get(identifier)
        if replacement is None and default is None:
            raise MissingEnvVarError(f"No value found for: {identifier}")
        text = text.replace(match.group(), replacement or default, 1)
        match = re.search(pattern=env_var_regexp, string=text)
    return text


def _extract_identifier_and_default(to_expand: str) -> tuple[str, Optional[str]]:
    to_expand = to_expand.removeprefix("${").removesuffix("}")
    if ":" in to_expand:
        identifier, default = to_expand.split(":")
    else:
        identifier = to_expand
        default = None
    return identifier, default
