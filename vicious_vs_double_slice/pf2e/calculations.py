def misses(attack: int, ac: int) -> int:
    if attack >= ac + 9:
        return 0 # all our attacks are crits, so a 1 would be one degree lower, still a hit
    if attack + 1 >= ac:
        return 1 # we only miss on a 1
    max_fails = 20 if attack + 30 <= ac else 19 # if a 20 is a crit-miss, then we can miss on all 20 rolls
    return min(ac - attack - 1, max_fails)

def crits(attack: int, ac: int) -> int:
    if ac >= attack + 30: # all our attacks are crit-misses, so a 20 would be one degree higher, still a miss
        return 0 
    if ac > attack + 20: # a 20 is a miss, which is promoted to a hit, but not a crit
        return 0
    return max(1, min(20 + attack - ac - 10 + 1, 19)) # we can always crit AT MOST 19 times, a 1 will always be a regular hit

def hits(attack: int, ac: int) -> int:
    if ac >= attack + 30:
        return 0 # all our attacks are crit-misses, so a 20 would be one degree higher, still a miss
                # technically when ac = attack + 20, a 20 would hit but it is also a crit, we're only interested in hits
    if ac > attack + 20:
        return 1 # all our attacks are misses, so a 20 would be one degree higher, a regular hit
    if attack + 1 >= ac + 10:
        return 20 - crits(attack, ac) # all our attacks are crits
    if attack + 1 >= ac:
        return 19 - crits(attack, ac) # all our non-1s are hits or crits
    return min(20 + attack - ac + 1, 20) - crits(attack, ac)