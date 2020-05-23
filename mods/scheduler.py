import subprocess
import asyncio
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler



def runner(path_of_exe):
    subprocess.call(path_of_exe)





def schedule(path_of_exe,dt):
    scheduler = BackgroundScheduler()
    print(scheduler.get_jobs())
    try:
        pass
    except:
        pass
    try:
        scheduler.add_job(runner,args=[path_of_exe],next_run_time=dt,id='software')
        try:scheduler.start()
        except:pass
        print(scheduler.get_jobs())
    except Exception as e:
        print("done")
    