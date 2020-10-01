import urx
import time

robot = urx.Robot("172.31.1.26")

f = open('log.txt', 'r')

initial_pos =  [-1.0587751761201067, -0.11921497119500135, 0.609480861771145, 2.941498103125462, -1.0023832831045307, 0.08831311307550381]
robot.movel(initial_pos, acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)

init_pose = robot.get_pos()
init_endeffector_pose = robot.getl()
print("Initial pose end: {0}".format(init_pose))
print("Initial pose  end_effector (joints): {0}".format(init_endeffector_pose))


pos1 = [-0.8988240897113172, -0.21605483164909475, 0.7015355331732347, -2.870707769590583, 1.1651019753043326, -0.027579315132054822]

pos2 = [-0.9074712493785123, -0.11748948344753173, 0.6625095337406617, -2.7673541755739914, 1.3001765387896345, -0.17223587521868697]

pos3 = [-0.7665681020250611, -0.17705009516652287, 0.7642263715688047, -2.84650590479123, 1.2258301541682215, -0.024897230711219267]

pos4 = [-0.9233348465258112, -0.15953213863962765, 0.6173506798132884, -2.775787360168886, 1.224456769365248, -0.2300918128537496]

i = 0
while i<5:
    robot.movel(pos1,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
    time.sleep(1)
    
    robot.movel(pos2,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
    time.sleep(1)
    
    robot.movel(pos3,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
    time.sleep(1)
    
    robot.movel(pos4,  acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
    time.sleep(1)
    
    i = i+1


with open('./log.txt') as fp:
   line = fp.readline()
   cnt = 1
   while line:
       print("Measurent camera frame pose {0}: {1}".format(cnt, line.strip()))
       # one point 
       u, v = fp.readline().strip().split(',')
       
       end_effector_pose = mapping_tcp(u, v)
       cube_pos = end_effector_pose
       robot.movel(cube_pos, acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
       time.sleep(1)
       
       cnt += 1
       
def mapping_tcp(u, v, acc, vel, r):
    T = np.array([ 1.60288777,
                   3.18281425,
                  13.78702889])
    
    R = np.array([[0.1074576 ,1.46403148,2.71542687],
                  [0.04510354, -0.451017  , -3.06188704],
                  [-0.01608162,-0.87880069,-2.8779496 ]])
  
    camera_cor = np.array([u, v, 1])
    
    # z = np.zeros((max(R.shape), max(R.shape)))
    # z[:R.shape[0],:R.shape[1]] = R
    # R = z

    XYZ = (camera_cor - T).dot(np.linalg.inv(R))/10000
    
    np.append(XYZ, [acc, vel, r])
    
    return XYZ
    

robot.stop()
robot.close()
