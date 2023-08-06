import locale
from datetime import datetime
from typing import List

locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


def parenthesis_is_closed(phrase: str) -> bool:
    if phrase != "":
        if phrase.count("(") > phrase.count(")") or phrase.rfind(")") < phrase.rfind("("):
            return False
    return True


def contains_only_closing_parenthesis(phrase: str) -> bool:
    return phrase.count("(") == 0 and phrase.count(")") > 0


def is_closing_a_parenthesis(phrase: str) -> bool:
    return phrase.count(")") > phrase.count("(")


def is_valid_date_format(text: str) -> List[bool]:
    result = []
    for date_format in ["%d de %B de %Y"]:
        try:
            result.append(datetime.strptime(text, date_format) is not None)
        except ValueError:
            result.append(False)
    return result


def is_date_format(text: str) -> bool:
    return any(is_valid_date_format(text))
