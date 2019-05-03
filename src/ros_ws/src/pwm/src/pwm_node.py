#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import Adafruit_PCA9685

PWM_FREQ = 50
MOTOR_CHANNEL = 13
SERVO_CHANNEL = 14

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(PWM_FREQ)

def set_pulse(channel, pulse):
    pulse = PWM_FREQ * pulse * 4096
    pwm.set_pwm(channel, 0, int(pulse))

def set_value(channel, value):
    value = min(max(value, -1.0), 1.0)
    pulse = 0.0015 + value * 0.0005
    set_pulse(channel, pulse)
    rospy.logdebug("set pulse: %f on channel channel %d", pulse, channel)

def motor_callback(data):
    value = data.data
    rospy.logdebug(rospy.get_caller_id() + "motor: %f", value)
    set_value(MOTOR_CHANNEL, value)

def servo_callback(data):
    value = data.data
    rospy.logdebug(rospy.get_caller_id() + "servo %f", value)
    set_value(SERVO_CHANNEL, value)
    
def main():
    rospy.init_node('pwm')
    rospy.Subscriber("pwm/motor", Float64, motor_callback)
    rospy.Subscriber("pwm/servo", Float64, servo_callback)
    rospy.spin()
  
if __name__ == '__main__':
    main()
