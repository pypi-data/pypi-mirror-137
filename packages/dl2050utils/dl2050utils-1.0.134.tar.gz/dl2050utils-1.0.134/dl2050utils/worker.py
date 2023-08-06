import asyncio
import sys
import json
from dl2050utils.env import config_load
from dl2050utils.log import AppLog
from dl2050utils.dbpg import DB
from dl2050utils.mq import MQ

class WorkerServer():

    def __init__(self, path, qs, cb):
        cfg = config_load()
        LOG = AppLog(cfg, service='worker')
        db = DB(cfg=cfg, log=LOG)
        mq = MQ(LOG, db, qs)
        self.LOG,self.db,self.mq = LOG,db,mq
        self.path,self.qs,self.cb = path,qs,cb

    def run(self):
        if self.db.sync_startup(): exit(1)
        if self.mq.sync_startup(): exit(1)
        self.LOG(2, 0, label='WORKER', label2='RUN', msg='OK')
        err = asyncio.get_running_loop().run_until_complete(self.mq.consumer(self.path, self.qs[0], self.cb))
        if err:
            self.LOG(4, 0, label='WORKER', label2='EXCEPTION', msg='Exit')
            sys.exit(1)
