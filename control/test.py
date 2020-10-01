import urx

robot = urx.Robot("172.31.1.26")

pos = robot.get_pos()
print("Pos: {0}".format(pos))

pose = robot.get_pose()
print("Pose: {0}".format(pose))

orientation = robot.get_orientation()
print("Orientation: (0)".format(orientation))

init_endeffector_pose = robot.getl()
print("Initial pose  end_effector (joints): {0}".format(init_endeffector_pose))

robot.stop()
robot.close()