from enum import Enum
from typing import Self

class DegreeOfSuccess(Enum):
    CRITICAL_FAILURE = 0
    FAILURE = 1
    SUCCESS = 2
    CRITICAL_SUCCESS = 3

    def one_better(self) -> Self:
        if self != DegreeOfSuccess.CRITICAL_SUCCESS:
            return DegreeOfSuccess(self.value + 1)
        else:
            return self
        
    def one_worse(self) -> Self:
        if self != DegreeOfSuccess.CRITICAL_FAILURE:
            return DegreeOfSuccess(self.value - 1)
        else:
            return self


def outcome(d20: int, bonus: int, dc: int) -> DegreeOfSuccess:
    if d20 < 1 or d20 > 20:
        raise Exception(f"a d20 can't be lower than 1 or larger than 20 (d20=={d20})")

    if d20 + bonus <= dc - 10:
        outcome = DegreeOfSuccess.CRITICAL_FAILURE
    elif d20 + bonus < dc:
        outcome = DegreeOfSuccess.FAILURE
    elif d20 + bonus < dc + 10:
        outcome = DegreeOfSuccess.SUCCESS
    else:
        outcome = DegreeOfSuccess.CRITICAL_SUCCESS
    
    if d20 == 1:
        outcome = outcome.one_worse()
    elif d20 == 20:
        outcome = outcome.one_better()
    
    return outcome