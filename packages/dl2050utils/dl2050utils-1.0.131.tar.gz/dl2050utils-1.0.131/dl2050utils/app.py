import time
from pathlib import Path
from starlette.exceptions import HTTPException
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.authentication import requires
from dl2050utils.core import oget
from dl2050utils.restutils import rest_ok, rest_error, get_meta, get_required_args, get_required, get_args


class App():

    def __init__(self, cfg, LOG, NOTIFY, db, mq, auth, path, routes=[], appstartup=None, perm=None):
        self.cfg,self.LOG,self.NOTIFY,self.db,self.mq,self.auth = cfg,LOG,NOTIFY,db,mq,auth
        self.routes,self.appstartup,self.perm = routes,appstartup,perm
        self.d = {'LOG':LOG, 'db':db, 'path':path}

    async def startup(self):
        model,meta = oget(self.cfg, ['app','model']),None
        if model is not None: meta = await get_meta(self.db, model)
        self.d['meta'] = meta
        if self.appstartup is None: return False
        return await self.appstartup(self.d)

    def shutdown(self):
        self.LOG.log(2, 0, label='APP', label2='shutdown', msg='OK')
        return False   

    def get_routes(self):
        BASE_ROUTES = [
            Route('/api/get_meta', endpoint=self.get_meta, methods=['GET']),
            Route('/api/public2', endpoint=self.public2, methods=['GET']),
            Route('/api/private', endpoint=self.private, methods=['GET']),
            Route('/api/download', endpoint=self.download, methods=['GET']),
            Route('/api/request_job', endpoint=self.request_job, methods=['POST']),
            Route('/api/get_jobs', endpoint=self.get_jobs, methods=['POST']),
            Route('/api/get_job', endpoint=self.get_job, methods=['POST']),
        ]
        APP_ROUTES = [Route(e, endpoint=self.app_route, methods=['POST']) for e in self.routes]
        return BASE_ROUTES + APP_ROUTES

    @requires('authenticated')
    async def get_meta(self, request):
        u = await self.auth.check_auth(request)
        return rest_ok(self.d['meta'])

    @requires('authenticated')
    async def public2(self, request):
        u = await self.auth.check_auth(request)
        fname = request.query_params['fname']
        p = Path(f'/data/public2/{fname}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def private(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.query_params['fname']
        p = Path(f'/data/private/{uid}/{fname}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def download(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        fname = request.query_params['fname']
        p = Path(f'/data/tmp/{int(time.time())//30}-{uid}-{fname}')
        return FileResponse(str(p), media_type='application/vnd.ms-excel', filename=fname)

    @requires('authenticated')
    async def request_job(self, request):
        u = await self.auth.check_auth(request)
        uid,org = u['uid'],u['org']
        data = await request.json()
        args = get_required_args(data,['q','payload'])
        self.perm(self.meta, self.d, request.url.path, uid, org, **args)
        jid = await self.mq.publish(args['q'], uid, args['payload'])
        if jid is None :
            return rest_error(self.LOG, 'APP', 'request_job', '')
        self.LOG.log(2, 0, label='APP', label2='request_job',  msg={'jid':jid, 'uid': uid, 'payload': data})
        return rest_ok({'jid': jid})

    @requires('authenticated')
    async def get_jobs(self, request):
        u = await self.auth.check_auth(request)
        uid = u['uid']
        data = await request.json()
        kwargs = get_args(data,['status'])
        jobs = await self.mq.get_jobs(uid, kwargs)
        return rest_ok(jobs)

    @requires('authenticated')
    async def get_job(self, request):
        u = await self.auth.check_auth(request)
        data = await request.json()
        [jid] = get_required(data,['jid'])
        args = get_required_args
        job = await self.mq.get_job(jid)
        return rest_ok(job)

    @requires('authenticated')
    async def app_route(self, request):
        if request.url.path not in self.routes:
            raise HTTPException(401, detail=f'App route not available')
        d = self.routes[request.url.path]
        f,args,kwargs = d['f'],d['args'],d['kwargs']
        u = await self.auth.check_auth(request)
        data = await request.json()
        args = get_required_args(data, args)
        kwargs = get_args(data, kwargs)
        self.perm(d, u, request.url.path, {**args, **kwargs})
        res = await f(self.d, u, *[args[e] for e in args], **kwargs)
        return rest_ok(res)
