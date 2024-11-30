import pytest
from vicious_vs_double_slice.pf2e import degrees

"""
Test matrix for dice outcomes:

d20 = 1, 10, 20
bonus = 0, 10, 20, 30, 2**32
dc = 0, 10, 20, 30, 2**32
"""
@pytest.mark.parametrize("d20, bonus, dc, outcome", [
    (1, 0, 0, degrees.DegreeOfSuccess.FAILURE),
    (1, 0, 10, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 0, 20, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 0, 30, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 0, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 10, 0, degrees.DegreeOfSuccess.SUCCESS),
    (1, 10, 10, degrees.DegreeOfSuccess.FAILURE),
    (1, 10, 20, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 10, 30, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 10, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 20, 0, degrees.DegreeOfSuccess.SUCCESS),
    (1, 20, 10, degrees.DegreeOfSuccess.SUCCESS),
    (1, 20, 20, degrees.DegreeOfSuccess.FAILURE),
    (1, 20, 30, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 20, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 30, 0, degrees.DegreeOfSuccess.SUCCESS),
    (1, 30, 10, degrees.DegreeOfSuccess.SUCCESS),
    (1, 30, 20, degrees.DegreeOfSuccess.SUCCESS),
    (1, 30, 30, degrees.DegreeOfSuccess.FAILURE),
    (1, 30, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (1, 4294967296, 0, degrees.DegreeOfSuccess.SUCCESS),
    (1, 4294967296, 10, degrees.DegreeOfSuccess.SUCCESS),
    (1, 4294967296, 20, degrees.DegreeOfSuccess.SUCCESS),
    (1, 4294967296, 30, degrees.DegreeOfSuccess.SUCCESS),
    (1, 4294967296, 4294967296, degrees.DegreeOfSuccess.FAILURE),
    (10, 0, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 0, 10, degrees.DegreeOfSuccess.SUCCESS),
    (10, 0, 20, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 0, 30, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 0, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 10, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 10, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 10, 20, degrees.DegreeOfSuccess.SUCCESS),
    (10, 10, 30, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 10, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 20, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 20, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 20, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 20, 30, degrees.DegreeOfSuccess.SUCCESS),
    (10, 20, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 30, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 30, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 30, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 30, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 30, 4294967296, degrees.DegreeOfSuccess.CRITICAL_FAILURE),
    (10, 4294967296, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 4294967296, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 4294967296, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 4294967296, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (10, 4294967296, 4294967296, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 0, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 0, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 0, 21, degrees.DegreeOfSuccess.SUCCESS), # Slightly modified to cover a scenario when a 20 is a regular success
    (20, 0, 30, degrees.DegreeOfSuccess.FAILURE),
    (20, 0, 4294967296, degrees.DegreeOfSuccess.FAILURE),
    (20, 10, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 10, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 10, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 10, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 10, 4294967296, degrees.DegreeOfSuccess.FAILURE),
    (20, 20, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 20, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 20, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 20, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 20, 4294967296, degrees.DegreeOfSuccess.FAILURE),
    (20, 30, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 30, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 30, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 30, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 30, 4294967296, degrees.DegreeOfSuccess.FAILURE),
    (20, 4294967296, 0, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 4294967296, 10, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 4294967296, 20, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 4294967296, 30, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
    (20, 4294967296, 4294967296, degrees.DegreeOfSuccess.CRITICAL_SUCCESS),
])
def test_outcomes(d20: int, bonus: int, dc: int, outcome: degrees.DegreeOfSuccess):
    actual = degrees.outcome(d20, bonus, dc)
    assert outcome == actual, f"Incorrect outcome for d20={d20}, bonus={bonus}, dc={dc}. Actual={actual}, expected={outcome}"