from vicious_vs_double_slice.pf2e import calculations


def test_hits():
    for attack in range(0, 51):
        for ac in range(0, 51):
            total_hits = 0
            for d20 in range (1, 21):
                if d20 == 1:
                    if attack + d20 >= ac + 10: # 1 will hit if it is a crit success
                        total_hits += 1
                elif d20 == 20:
                    if attack + d20 < ac and attack + d20 > ac - 10: # 20 is a regular hit only if the attack is a miss, but not a crit miss 
                        total_hits += 1
                else:
                    if attack + d20 >= ac and attack + d20 < ac + 10: # hits and not crits
                        total_hits += 1
            assert calculations.hits(attack, ac) == total_hits, f"Incorrect number of hits for attack={attack}, ac={ac}"

def test_crits():
    for attack in range(0, 51):
        for ac in range(0, 51):
            total_crits = 0
            for d20 in range (2, 21): # starting from 2 because a 1 will never be a crit
                if d20 == 20:
                    if attack + d20 >= ac: # a 20 is a crit on a regular hit
                        total_crits += 1
                else:
                    if attack + d20 >= ac + 10:
                        total_crits += 1
            assert calculations.crits(attack, ac) == total_crits, f"Incorrect number of crits for attack={attack}, ac={ac}"

def test_misses():
    for attack in range(0, 51):
        for ac in range(0, 51):
            total_misses = 0
            for d20 in range (1, 21):
                if d20 == 1:
                    if not (attack + d20 >= ac + 10): # 1 isn't a miss if it is a crit success
                        total_misses += 1
                elif d20 == 20:
                    if attack + d20 <= ac - 10: # 20 is still a miss if it is a crit fail, but not a regular miss
                        total_misses += 1
                else:
                    if attack + d20 < ac:
                        total_misses += 1
            assert calculations.misses(attack, ac) == total_misses, f"Incorrect number of misses for attack={attack}, ac={ac}"
