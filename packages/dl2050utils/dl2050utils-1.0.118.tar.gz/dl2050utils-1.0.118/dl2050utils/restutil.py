import datetime
import random
import json
import jwt
from starlette.responses import JSONResponse

def mk_key(n=4):
    return ''.join([chr(48+i) if i<10 else chr(65-10+i) for i in [random.randint(0, 26+10-1) for _ in range(n)]])
    # return ''.join(random.choice(string.ascii_lowercase) for i in range(n))

def mk_jwt_token(uid, email, secret):
    JWT_EXP_DELTA_SECONDS = 30*24*3600
    payload = { 'uid': uid, 'email': email, 'username': '', 'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP_DELTA_SECONDS)}
    return jwt.encode(payload, secret, 'HS256') # .decode('utf-8')

def rest_ok(result):
    return JSONResponse({'status': 'OK', 'result': result})

def rest_error(LOG, label, label2, error_msg):
    LOG.log(4, 0, label=label, label2=label2, msg=error_msg)
    return JSONResponse({'status': 'ERROR', 'error_msg': error_msg})

def check_inputs(data, flds):
    for fld in flds:
        if fld not in data.keys(): raise Exception('Invalid request parameters')

def get_data(o, fs): return [o[e] if e in o else None for e in fs]
def get_value(o,f): return o[f] if f in o.keys() and o[f] else None
def get_array(o,f): return o[f] if f in o.keys() and o[f] and len(o[f]) else None
def get_arrays(o,fs): return [o[e] if e in o.keys() and o[e] and len(o[e]) else None for e in fs]

async def get_meta(db, model):
    row = await db.select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None
