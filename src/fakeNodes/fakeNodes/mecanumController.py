import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import JointState
from control_msgs.msg import JointJog


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.cmd_vel_sub = self.create_subscription(Twist, 'cmd_vel', self.mecanumController, 10)
        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)

    def mecanumController(self, msg):
        '''
        Take in a cmd_vel message, and publish joint state messages to command the mecanum wheels
        '''
        forward = msg.linear.x
        strafe = msg.linear.y
        rotate = msg.angular.z

        #Mecanum logic
        powerFL = forward + strafe - rotate
        powerFR = forward - strafe + rotate
        powerBL = forward - strafe - rotate
        powerBR = forward + strafe + rotate

        #normalize power levels on [0,1]
        powerMax = max(abs(powerBL), abs(powerFR), abs(powerFL), abs(powerBR))
        if powerMax >= 1.0:
            powerFL /= powerMax
            powerFR /= powerMax
            powerBL /= powerMax
            powerBR /= powerMax


        #publish jointJogs
        msg = JointJog()
        


        


    
            


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()