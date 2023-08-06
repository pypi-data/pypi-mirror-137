import datetime
import random
import json
import jwt
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from dl2050utils.core import listify

def get_required(d, attrs):
    args = []
    for e in listify(attrs):
        if e not in d or d[e] is None:
            raise HTTPException(401, detail=f'Missing required arg {e}')
        args.append(d[e])
    return args

def get_required_args(d, attrs):
    args = {}
    for e in listify(attrs):
        if e not in d or d[e] is None:
            raise HTTPException(401, detail=f'Missing required arg {e}')
        args[e] = d[e]
    return args

def get_args(d, attrs): return {e:d[e] for e in listify(attrs) if e in d and d[e] is not None}

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

async def get_meta(db, model):
    row = await db.select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None

def mk_weeks(ds1='2018-01-01', ds2=None, weekday=6):
    d1 = datetime.datetime.strptime(ds1, '%Y-%m-%d').date()
    delta = 5 - d1.weekday()
    if delta<0: delta+=7
    d1 += datetime.timedelta(days=delta)
    d2 = datetime.datetime.now().date() if ds2 is None else datetime.datetime.strptime(ds2, '%Y-%m-%d').date()
    ds = [d.strftime("%Y-%m-%d") for d in rrule.rrule(rrule.WEEKLY, dtstart=d1, until=d2)]
    return ds[::-1]

def get_week2(weeks, week): return weeks[weeks.index(week)+1] if weeks.index(week)+1<len(weeks) else None

def s3_urls(s3, bucket_name, prefix):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix, MaxKeys=1024)['Contents']
    return [f'http://{bucket_name}.s3-eu-west-1.amazonaws.com/{e["Key"]}' for e in response]
