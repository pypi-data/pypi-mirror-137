import re

__all__ = ["deployment_to_skip"]

def deployment_to_skip(skip: list, name: str):
    for token in skip:
        if re.search(token, name):
            return True
    return False
