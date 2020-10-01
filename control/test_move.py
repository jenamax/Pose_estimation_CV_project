import urx
import time

robot = urx.Robot("172.31.1.26")

init = [-0.583266965702818, -0.17924341655468268, 0.6324579325887602, 2.589 2461752618448, -1.1237510748104935, -0.7988089278120047]
robot.movel(init, acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)

cube_pos = [-0.8638683887747833, -0.16531380999090592, 0.42247938813372343, -2.81182782261324, 1.2321802029823103, -0.14377321591415151]
robot.movel(cube_pos, acc=0.5, vel=0.1, wait=False, relative=False, threshold=None)
time.sleep(1)


robot.stop()
robot.close()
