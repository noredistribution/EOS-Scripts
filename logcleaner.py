#!/usr/bin/env python
#Note: run the script with sudo

from __future__ import print_function,unicode_literals
import os
import re
from subprocess import Popen, PIPE
from pprint import pprint as pp
import time


#get all the filenames from /var/log/agents

agents_dir = '/var/log/agents'
agents = os.listdir(agents_dir)

agents_div=[]

for i in agents:
        m = re.match(r'(^[a-zA-Z].*)-(.*)',i)
        agents_div.append([m.groups()[0], m.groups()[1]])

#pp(agents_div)


#get the running process IDs

sub_proc = Popen(['ps','aux'],shell=False,stdout=PIPE)
proc_list = []
for line in sub_proc.stdout:
        proc_info = re.split(" *",line.strip())
        proc_list.append(proc_info[1])

#pp(proc_list)


#check if the PID from agent_name-<PID> is active in the running processes list
#and if not delete the log file if it's older than 10 minutes
#large log files will logrotate and will have the format of <agentname>-<pid>.<rotation_number>.gz
#check for files that end in .gz and only delete them if the pid is not active

current_time = time.time()

for i in agents_div:
        if ('gz' in i[1] and i[1].split('.')[0] not in proc_list) or ('gz' not in i[1] and i[1] not in proc_list):
                i_time = os.path.getmtime(agents_dir + '/' + i[0] + '-' +i[1])
#                print(i[0], i_time)
                if (int(current_time) - int(i_time)) > 360:
                        print("Deleting {}-{}".format(i[0],i[1]))
                        os.remove('{}/{}-{}'.format(agents_dir,i[0],i[1]))

