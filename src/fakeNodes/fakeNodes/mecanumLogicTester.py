import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import JointState


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.joint_state_subscriber = self.create_subscription(JointState, 'joint_states', self.joint_state_callback, 10)


        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        #declare messages
        self.cmd0 = Twist() #do nothing

        self.cmd1 = Twist() #drive forward
        self.cmd1.linear = Vector3()
        self.cmd1.linear.x = 1.0

        self.cmd2 = Twist() #drive left
        self.cmd2.linear = Vector3()
        self.cmd2.linear.y = 1.0

        self.cmd3 = Twist() #drive right and backwards
        self.cmd3.linear = Vector3()
        self.cmd3.linear.x = -0.5
        self.cmd3.linear.y = -0.5

        self.cmd4 = Twist() #rotate counterclockwise
        self.cmd4.linear = Vector3()
        self.cmd4.angular = Vector3()
        self.cmd4.angular.z = 0.5


    def timer_callback(self):

        match (self.i % 5):
            case 0:
                self.cmd_vel_publisher.publish(self.cmd0)
            case 1:
                self.cmd_vel_publisher.publish(self.cmd1)
            case 2:
                self.cmd_vel_publisher.publish(self.cmd2)
            case 3:
                self.cmd_vel_publisher.publish(self.cmd3)
            case 4:
                self.cmd_vel_publisher.publish(self.cmd4)
        
        self.i += 1

    def joint_state_callback(self, msg):
        pass

    
            


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