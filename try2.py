import rospy
from clover import srv
from std_srvs.srv import Trigger
from datetime import datetime, date, time

rospy.init_node('flight')

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)
a,b,c= map(float, input().split())
navigate(x=0, y=0, z=1.5, frame_id='body', auto_arm=True) 
rospy.sleep(5)
navigate(x=0, y=0, z=1.5, frame_id='aruco_map',speed=0.5)
rospy.sleep(3)
navigate(x=0, y=0, z=c, frame_id='aruco_map',speed=0.5)
rospy.sleep(3)
navigate(x=a, y=b, z=c, frame_id='aruco_map',speed=0.5)
rospy.sleep(5)
g=0
for i in range(700): 
    g+=1
    telemetry= get_telemetry(frame_id='aruco_map')
    print(f"{g}\t{telemetry.x}\t{telemetry.y}\t{telemetry.z}", end='\n\n')
    navigate(x=a, y=b, z=c, frame_id='aruco_map',speed=0.1)
    rospy.sleep(0.2)
land()