import re, functools, itertools, operator as op, math, sys, os 
from fuckerupper import fuckitup
stenv = { '+':op.__add__,'-':op.__sub__,'*':op.__mul__,'/':op.__truediv__, 'len':len, 'or':op.__or__, 'and':op.__and__, 'not':op.__not__,
    '>=':op.ge, '<=':op.le, '=':op.eq, '<':op.lt, '>':op.gt, 'nth':lambda x, y: y[x], 'range':lambda x, y: list(range(x, y)), 'read':lambda x: open(x, 'r').read(),
    'map':lambda x, y: list(map(y, x)),'reduce': lambda x,y: functools.reduce(y, x), 'scan': lambda x, y: list(itertools.accumulate(x, y)), 'write':lambda x, y: open(x, 'w').write(y),
    'slice':lambda x, y, z: x[y:z], 'print':print, 'input':input, 'nil':None, 'true':True, 'false':False}; stenv.update(vars(math))
def parse(s):
    l = re.sub(r'\s+', ', ', (' '+s.lower()+' ').replace('(', '[').replace(')', ']'))[2:-2]
    return eval(re.sub(r'(?P<symbol>[\w#%\\/^*+_\|~<>?!:.\-=]+)', lambda m : '"%s"' % m.group('symbol'), l))
def l_eval(i, env):
    if type(i) == str:
        if i.replace('.','',1).isdigit():
            try: return int(i)
            except: return float(i)
        else: return env[i]
    if type(i) == list:
        if i[0] == 'q': return [l_eval(x, env) for x in i[1:]]
        elif i[0] == 'lambda':
            args, body = i[1], i[2]
            def lambdafunc(*argv):
                n_env = dict(stenv)
                for i in range(len(args)): n_env[args[i]] = argv[i]
                return l_eval(body, n_env)
            return lambdafunc
        elif i[0] == 'set':
            env[i[1]] = l_eval(i[2], env)
        elif i[0] == 'if': 
            if l_eval(i[1], env): return l_eval(i[2], env) 
            else: return l_eval(i[3], env)
        elif i[0] == 's': return ' '.join(i[1:])
        elif i[0] == 'import':
            parsed = parse(open(i[1]).read())
            if isinstance(parsed[0], list): 
                for k in parsed: l_eval(k, env)
            else: l_eval(parsed, env)
        elif i[0] == 'while':
            while l_eval(i[1], env): l_eval(i[2], env)
        elif i[0] == 'do':
            for k in i[1:]: l_eval(k, env)
        else: return fuckitup(env[i[0]](*[l_eval(j, env) for j in i[1:]]))
if len(sys.argv) == 1:
    while True:
        text = input('<) ')
        try: print('=> ', l_eval(parse(text), stenv))
        except Exception as e: print(e); continue
else:
    file, argv = open(sys.argv[1]).read(), sys.argv[2:]
    stenv['argv'], parsed = argv, parse(file)
    if isinstance(parsed[0], list): 
        for i in parsed: l_eval(i, stenv)
    else: l_eval(parsed, stenv)