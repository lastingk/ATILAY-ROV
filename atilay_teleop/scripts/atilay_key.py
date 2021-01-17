#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

ATILAY_MAX_LIN_VEL = 0.8
ATILAY_MAX_HOR_VEL = 0.4
ATILAY_MAX_ANG_VEL = 2
ATILAY_MAX_DRF_VEL = 0.4
ATILAY_MAX_ROL_VEL = 0.4

LIN_VEL_STEP_SIZE = 0.05
HOR_VEL_STEP_SIZE = 0.025
ANG_VEL_STEP_SIZE = 0.1
DRF_VEL_STEP_SIZE = 0.025
ROL_VEL_STEP_SIZE = 0.05

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
   q    w    e         o
   a    s    d                  
        x              l

w/x : increase/decrease linear velocity 
a/d : increase/decrease angular velocity
o/l : increase/decrease horizontal velocity
q/e : increase/decrease drifting velocity
j/k : increase/decrease rolling velocity

space key, s : force stop

CTRL-C to quit
"""
e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
      return msvcrt.getch()

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel,target_horizontal_vel, target_angular_vel):
    return "currently:\tlinear vel %s\thorizontal vel %s\t angular vel %s " % (target_linear_vel, target_horizontal_vel, target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    vel = constrain(vel, -ATILAY_MAX_LIN_VEL, ATILAY_MAX_LIN_VEL)
    return vel
def checkAngularLimitVelocity(vel):
    vel = constrain(vel, -ATILAY_MAX_ANG_VEL, ATILAY_MAX_ANG_VEL)
    return vel
def checkHorizontalLimitVelocity(vel):
    vel = constrain(vel, -ATILAY_MAX_HOR_VEL, ATILAY_MAX_HOR_VEL)
    return vel
def checkDriftingLimitVelocity(vel):
    vel = constrain(vel, -ATILAY_MAX_DRF_VEL, ATILAY_MAX_DRF_VEL)
    return vel
def checkRollingLimitVelocity(vel):
    vel = constrain(vel, -ATILAY_MAX_ROL_VEL, ATILAY_MAX_ROL_VEL)
    return vel

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('atilay_keyboard')
    pub = rospy.Publisher('/atilay/cmd_vel', Twist, queue_size=10)


    status = 0
    target_linear_vel   = 0.0
    target_horizontal_vel   = 0.0	
    target_angular_vel  = 0.0
    target_drifting_vel  = 0.0
    target_rolling_vel  = 0.0
    control_linear_vel  = 0.0
    control_horizontal_vel  = 0.0
    control_angular_vel = 0.0
    control_drifting_vel  = 0.0
    control_rolling_vel  = 0.0

    try:
        print(msg)
        while(1):
            key = getKey()
            if key == 'w' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            elif key == 'x' :
                target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))

            elif key == 'o' :
                target_horizontal_vel = checkHorizontalLimitVelocity(target_horizontal_vel + HOR_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            elif key == 'l' :
                target_horizontal_vel = checkHorizontalLimitVelocity(target_horizontal_vel - HOR_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))

            elif key == 'j' :
                target_rolling_vel = checkRollingLimitVelocity(target_rolling_vel + ROL_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            elif key == 'k' :
                target_rolling_vel = checkRollingLimitVelocity(target_rolling_vel - ROL_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))

            elif key == 'q' :
                target_drifting_vel = checkDriftingLimitVelocity(target_drifting_vel + DRF_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            elif key == 'e' :
                target_drifting_vel = checkDriftingLimitVelocity(target_drifting_vel - DRF_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))

            elif key == 'a' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            elif key == 'd' :
                target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                status = status + 1
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))

            elif key == ' ' or key == 's' :
                target_linear_vel   = 0.0
                control_linear_vel  = 0.0
                target_horizontal_vel   = 0.0
                control_horizontal_vel  = 0.0
                target_angular_vel  = 0.0
                control_angular_vel = 0.0
		control_drifting_vel  = 0.0
		target_drifting_vel  = 0.0
		control_rolling_vel  = 0.0
		target_rolling_vel  = 0.0
                print(vels(target_linear_vel, target_horizontal_vel, target_angular_vel))
            else:
                if (key == '\x03'):
                    break

            if status == 20 :
                print(msg)
                status = 0

            twist = Twist()

            control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = control_drifting_vel; twist.linear.z = control_horizontal_vel

            control_drifting_vel = makeSimpleProfile(control_drifting_vel, target_drifting_vel, (DRF_VEL_STEP_SIZE/2.0))
            twist.linear.x = control_linear_vel; twist.linear.y = control_drifting_vel; twist.linear.z = control_horizontal_vel

            control_horizontal_vel = makeSimpleProfile(control_horizontal_vel, target_horizontal_vel, (HOR_VEL_STEP_SIZE/2.0))
            twist.linear.z = control_horizontal_vel; twist.linear.y = control_drifting_vel; twist.linear.x = control_linear_vel

            control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

            control_rolling_vel = makeSimpleProfile(control_rolling_vel, target_rolling_vel, (ROL_VEL_STEP_SIZE/2.0))
            twist.angular.x = 0.0; twist.angular.y = control_rolling_vel; twist.angular.z = control_angular_vel

            pub.publish(twist)

    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
