# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:30:55 2017

@author: cesar
"""

from crontab import CronTab  #module= python-crontab

cron=CronTab(user=None)

cmd='cd /home/pi/python/bogleapp/ && /home/pi/python/venv/bin/python /home/pi/python/bogleapp/portfolio.py'

pjob = cron.new(cmd, comment='Bogleapp')
pjob.hour.on(00)
#pjob.minute.on(25)
#pjob.minute.every(1)
#pjob.hour.during(12,18)
#pjob.day.on(1)  #dia del mes
#pjob.dow.on(1) #dia de la semana


##cron_job = cron.find_command(cmd) #find and delete commands
##if len(next(cron_job)) > 0:
##    cron.remove_all(command='cmd') 
##
##print(cron.render())
##
##pjob.delete() #elimina el trabajo

cron.write_to_user(user=True) #escribe en crontab
