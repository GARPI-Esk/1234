from re import T
import rospy
from clover import srv
from std_srvs.srv import Trigger
from datetime import datetime, date, time
import sys
from datetime import datetime, timedelta
from out import *
rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

print(navigate(x=0, y=0, z=1.5, frame_id='body',speed=0.5, auto_arm=True))
rospy.sleep(6)
navigate(x=0, y=0, z=1.5, frame_id='aruco_6',speed=0.5)
rospy.sleep(1)
navigate(x=1, y=1, z=0, frame_id='body',speed=1)
rospy.sleep(3)
navigate(x=0, y=0, z=1.5, frame_id='aruco_map',speed=0.5)
rospy.sleep(3)

e=0
while True:
    now=datetime.now().time()
    # print(datetime.strptime(data[e][0],'%H:%M:%S').time())
    #print(str(now-datetime.strptime(data[e][0],'%H:%M:%S'))[12:])
    if (now>=  datetime.strptime(data[e][0],'%H:%M:%S').time()):
        print (data[e][0], data[e][1], data[e][2], '0.77',sep="\t")
        navigate(x=data[e][1], y=data[e][2], z=0.92, frame_id='aruco_map', speed=0.1)
        e+=1
        telemetry= get_telemetry(frame_id='aruco_map')
        print(f"{now}\t{abs(data[e][1] - telemetry.x)}\t{abs(data[e][2] - telemetry.y)}\t{abs(0.92 - telemetry.z)}", end='\n\n')
        rospy.sleep(0.1)
    navigate(x=data[e-1][1], y=data[e-1][2], z=0.92, frame_id='aruco_map', speed=0.1)
    if (e==len(data)):
        break
land()