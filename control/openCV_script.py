
# Python program to save a  
# video using OpenCV 
  
import urx
import time

import cv2 
  
robot = urx.Robot("172.31.1.26")

f = open('log_pos.txt', 'w')

# Create an object to read  
# from camera 
video = cv2.VideoCapture("/dev/video2") 
   
# We need to check if camera 
# is opened previously or not 
if (video.isOpened() == False):  
    print("Error reading video file") 
  
# We need to set resolutions. 
# so, convert them from float to integer. 
frame_width = int(video.get(3)) 
frame_height = int(video.get(4)) 
   
size = (frame_width, frame_height) 
   
# Below VideoWriter object will create 
# a frame of above defined The output  
# is stored in 'filename.avi' file. 
result = cv2.VideoWriter('filename.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 
 

def robot_init():

    # initial_pos =  [-1.0587751761201067, -0.11921497119500135, 0.609480861771145, 2.941498103125462, -1.0023832831045307, 0.08831311307550381]
    # robot.movel(initial_pos, acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
    
    init_pose = robot.get_pos()
    init_endeffector_pose = robot.getl()
    print("Initial pose end: {0}".format(init_pose))
    print("Initial pose  end_effector (joints): {0}".format(init_endeffector_pose))

def main_loop():
    pos1 = [-0.8988240897113172, -0.21605483164909475, 0.7015355331732347, -2.870707769590583, 1.1651019753043326, -0.027579315132054822]

    pos2 = [-0.9074712493785123, -0.11748948344753173, 0.6625095337406617, -2.7673541755739914, 1.3001765387896345, -0.17223587521868697]

    pos3 = [-0.7665681020250611, -0.17705009516652287, 0.7642263715688047, -2.84650590479123, 1.2258301541682215, -0.024897230711219267]

    pos4 = [-0.9233348465258112, -0.15953213863962765, 0.6173506798132884, -2.775787360168886, 1.224456769365248, -0.2300918128537496]

    i = 0
    while i<2:
        robot.movel(pos1,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
        time.sleep(1)
        
        pos = robot.get_pos()
        print("Pos: {0}".format(pos))
        f.write("Pos: {0}".format(pos))
        
        pose = robot.get_pose()
        print("Pose: {0}".format(pose))
        f.write("Pose: {0} \n".format(pose))

        orientation = robot.get_orientation()
        print("Orientation: (0)".format(orientation))
        f.write("Orientation: (0)\n".format(orientation))

        endeffector_pose = robot.getl()
        print("End-effector position {0}".format(endeffector_pose))
        f.write("End-effector position {0} \n".format(endeffector_pose))
         # --------------------------------------------------------------------------------------------------------------------------
        robot.movel(pos2,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
        time.sleep(1)
        
        pos = robot.get_pos()
        print("Pos: {0}".format(pos))
        f.write("Pos: {0}\n".format(pos))
        
        pose = robot.get_pose()
        print("Pose: {0}".format(pose))
        f.write("Pose: {0} \n".format(pose))

        orientation = robot.get_orientation()
        print("Orientation: (0)".format(orientation))
        f.write("Orientation: (0)\n".format(orientation))

        endeffector_pose = robot.getl()
        print("End-effector position {0}".format(endeffector_pose))
        f.write("End-effector position {0} \n".format(endeffector_pose))
        # ---------------------------------------------------------------------------------------------------------------------------
        
        robot.movel(pos3,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
        time.sleep(1)
        
        pos = robot.get_pos()
        print("Pos: {0}".format(pos))
        f.write("Pos: {0}\n".format(pos))
        
        pose = robot.get_pose()
        print("Pose: {0}".format(pose))
        f.write("Pose: {0} \n".format(pose))

        orientation = robot.get_orientation()
        print("Orientation: (0)".format(orientation))
        f.write("Orientation: (0)\n".format(orientation))

        endeffector_pose = robot.getl()
        print("End-effector position {0}".format(endeffector_pose))
        f.write("End-effector position {0} \n".format(endeffector_pose))
        # ----------------------------------------------------------------------------------------------------------------------------
        
        robot.movel(pos4,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
        time.sleep(1)
        
        pos = robot.get_pos()
        print("Pos: {0}".format(pos))
        f.write("Pos: {0}\n".format(pos))
        
        pose = robot.get_pose()
        print("Pose: {0}".format(pose))
        f.write("Pose: {0} \n".format(pose))

        orientation = robot.get_orientation()
        print("Orientation: (0)".format(orientation))
        f.write("Orientation: (0)\n".format(orientation))

        endeffector_pose = robot.getl()
        print("End-effector position {0}".format(endeffector_pose))
        f.write("End-effector position {0} \n".format(endeffector_pose))
        # -------------------------------------------------------------------------------------------------------------------------------
        i = i+1


    robot.stop()
    robot.close()
 
"""while(True): 
    ret, frame = video.read() 
    
    if ret == True:  
        # Write the frame into the 
        # file 'filename.avi' 
        result.write(frame) 
       

        # Display the frame 
        # saved in the file 
        cv2.imshow('Frame', frame)
  
        # Press S on keyboard  
        # to stop the process 
        if cv2.waitKey(1) & 0xFF == ord('s'): 
            break
  
    # Break the loop 
    else: 
        break
"""
 
robot_init()

main_loop()

f.close()
# When everything done, release  
# the video capture and video  
# write objects 
video.release() 
result.release() 
    
# Closes all the frames 
cv2.destroyAllWindows() 
   
print("The video was successfully saved") 