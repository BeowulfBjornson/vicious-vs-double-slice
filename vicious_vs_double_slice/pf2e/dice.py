import re
from dyce import H

# Limitation: we don't support starting with a negative modifier (i.e. `-4 + 3d6`)
_VALID_EXPRESSION_REGEX = re.compile(r"^((\d+d\d+)|\d+)( *(\+|-) *((\d+d\d+)|\d+))*$")
_DICE_EXPRESSION_SUBPART = re.compile(r"(^| *(?P<operator>\+|-)) *(((?P<count>\d+)d(?P<faces>\d+))|(?P<number>\d+))")


def _signed_number(operator: str, number: float) -> float:
    if operator == "+":
        return number
    else:
        return -1.0 * number


def average_value(expr: str) -> float:
    if _VALID_EXPRESSION_REGEX.match(expr) is None:
        raise ValueError(f"expr must be a valid dice expression")
    
    total: list[float] = []
    
    for match in _DICE_EXPRESSION_SUBPART.finditer(expr):
        operator = match.group("operator")
        if operator is None:
            operator = "+"  # this is the start of the string, we are adding
        number = match.group("number")
        if number is not None:
            total.append(_signed_number(operator, float(number)))
        else:
            count = float(match.group("count"))
            faces = float(match.group("faces"))
            total.append(_signed_number(operator, round(count * ((1.0 + faces)/2),1)))

    return sum(total)


def to_dyce_expression(expr: str) -> H:
    if _VALID_EXPRESSION_REGEX.match(expr) is None:
        raise ValueError(f"expr must be a valid dice expression")
    
    expression = H((0,)) # start with a 0 expression to make it easier to add elements
    
    for match in _DICE_EXPRESSION_SUBPART.finditer(expr):
        operator = match.group("operator")
        if operator is None:
            operator = "+"  # this is the start of the string, we are adding
        number = match.group("number")
        if number is not None:
            if operator == "+":
                expression = expression + int(number)
            else:
                expression = expression - int(number)
        else:
            count = int(match.group("count"))
            faces = int(match.group("faces"))
            d = count @ H(faces)
            if operator == "+":
                expression = expression + d
            else:
                expression = expression - d
    return expression
