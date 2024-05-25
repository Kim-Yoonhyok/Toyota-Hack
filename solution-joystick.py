#start with imports, ie: import the wrapper
import TMMC_Wrapper
import rclpy
import numpy as np
import math

#start ros
if not rclpy.ok():
    rclpy.init()

TMMC_Wrapper.is_SIM = True
if not TMMC_Wrapper.is_SIM:
    #specify hardware api
    TMMC_Wrapper.use_hardware()
    global is_SIM
    
if not "robot" in globals():
    robot = TMMC_Wrapper.Robot()

#debug messaging 
print("running main")

#start processes
robot.start_keyboard_control()   #this one is just pure keyboard control

rclpy.spin_once(robot, timeout_sec=0.1)

#run the keyboard control functions
try:
    print("Listening for keyboard events. Press keys to test, Ctrl C to exit")
    while True: 
        rclpy.spin_once(robot, timeout_sec=0.1)
        scan_data = robot.checkScan()
        th1 = 0.78 #math.pi/2  # -45 degrees in radians
        th2 = -0.78 #3*math.pi/2 # 135 degrees in radians
        percent = robot.lidar_data_too_close(scan_data, th1, th2, 0.5)

        if (percent > 0.3):
            print("Too close to wall")
            
            robot.stop_keyboard_control()
            #Back up 
            robot.set_cmd_vel(-1.0, 0.0, 1)
            #robot.start_keyboard_control()
        robot.start_keyboard_control()

        
except KeyboardInterrupt:
    print("keyboard interrupt receieved.Stopping...")
finally:
    #when exiting program, run the kill processes
    robot.stop_keyboard_control()
    robot.destroy_node()
    rclpy.shutdown()


