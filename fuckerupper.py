import random, sys
from string import ascii_letters

def fuckitup(thing):
    if bool(random.getrandbits(1)):
        if isinstance(thing, list):
            return [fuckitup(i) for i in thing]
        elif type(thing) in (int, float):
            return thing + random.randint(0, thing)
        elif isinstance(thing, bool):
            return not thing
        elif isinstance(thing, str):
            inds = [i for i,_ in enumerate(thing) if not thing.isspace()]
            sam = random.sample(inds, round(len(thing) / 3))
            letts =  iter(random.sample(ascii_letters, 3))
            lst = list(thing)
            for ind in sam:
                try: lst[ind] = next(letts)
                except: continue
            return "".join(lst)
    return thing