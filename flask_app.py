'''
  Script- Flask Web page
  Author - Vivek Sheel Banger

  '''
import os
import time
import logging
import copy
from   flask import Flask
from   flask import render_template
from   flask import request
from   apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig() #just to suppport BackgroundScheduler

#########################################################
#master_list = edit this list to add and remove router
#list_router will be update automatically
#########################################################
master_list = ["1.1.1.1","2.2.2.2","3.3.3.3","4.4.4.4","5.5.5.5","6.6.6.6"]
list_router = []

app=Flask("first APP")
cron =BackgroundScheduler()

#initiasize the list
list_router = copy.copy(master_list)
print "First initialozing the list_router........[Ok]"
print "Server is ready to accept the router list.[Ok]"

#######################################################
# this function must be sceduled just after shut_lc_card
# is called. Please think about this later
#######################################################
def restore_list():
      global list_router
      global master_list
      # delete al the member first
      # yeah i know its dirty way
      while len(list_router) > 0:
            list_router.pop()
      #restore the list 
      list_router = copy.copy(master_list)
      print "restoration of Router List Done........[Ok]"    

########################################################
# This function must be called 11:00 IST  at every night. 
# this will shut down all the LC card
#
#########################################################
def shut_down_card():
      print "Shuting down all the LC.........[Ok]"
      print "Shut down is done !You did a great job..[Ok]"
      restore_list()
########################################################
# This function must be called 7:00 IST  at every night. 
# this will power on  all the LC card
#
#########################################################
def power_on_card():
      print "Powering on  all the LC.........[Ok]"
      print "Routers are reday to use .......[Ok]"

########################################################
# starting point of the app
########################################################
@app.route('/', methods=['GET'])
def hello():
      print "Loading Welcome Page ............[Ok]"
      return render_template('first.html')

########################################################
# Update method called from hello.html
########################################################
@app.route('/update', methods=['POST'])
def update():
    global list_router
    if request.form.get('bhokal'):
       print "bhokal=" + (request.form.get('bhokal'))
       print list_router
       del list_router[list_router.index("1.1.1.1")]
       print list_router

    if request.form.get('cluster'):
       print "cluster-peer=" + (request.form.get('cluster'))
       print list_router
       del list_router[list_router.index("2.2.2.2")]
       print list_router

    print "Update done..................[Ok]"
    return render_template('saved.html')

###################################################
# Shcedule the cron jobs to proper timeing
# not sure if 11:00 is proper timing
##################################################
#cron.add_job(shut_down_card, 'cron', hour=23, minute=00)
cron.add_job(shut_down_card, 'interval', seconds=15)
#cron.add_job(power_on_card,'cron', hour=7, minuts=00)
cron.start()
if __name__ == "__main__":
     app.run(host="173.39.51.85", port=5000)

