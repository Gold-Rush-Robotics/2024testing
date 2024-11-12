import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3
from control_msgs.msg import JointJog


class mecanumLogic(Node):
    def __init__(self):
        super().__init__('mecanum_logic_tester')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        self.joint_state_subscriber = self.create_subscription(JointJog, 'joint_jog', self.joint_jog_callback, 10)


        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = -1

        #declare messages
        self.cmd0 = Twist() #do nothing

        self.cmd1 = Twist() #drive forward
        self.cmd1.linear.x = 1.0

        self.cmd2 = Twist() #drive left
        self.cmd2.linear.y = 1.0

        self.cmd3 = Twist() #drive right and backwards
        self.cmd3.linear.x = -0.5
        self.cmd3.linear.y = -0.5

        self.cmd4 = Twist() #rotate counterclockwise
        self.cmd4.angular.z = 0.5


    def timer_callback(self):
        cmd = None
        self.i += 1
        
        match (self.i % 5):
            case 0: cmd = self.cmd0
            case 1: cmd = self.cmd1
            case 2: cmd = self.cmd2
            case 3: cmd = self.cmd3
            case _: cmd = self.cmd4
        self.cmd_vel_publisher.publish(cmd)

    def joint_jog_callback(self, msg:JointJog):
        velos = {joint:velocity for joint, velocity in zip(msg.joint_names, msg.velocities)}
        fl = velos["front_left_wheel"]
        fr = velos["front_right_wheel"]
        bl = velos["back_left_wheel"]
        br = velos["back_right_wheel"]
        match (self.i % 5):
            case 0: #do nothing
                assert(fl == fr == bl == br == 0, f"Wheels are moving when they shouldnt be {fl} {fr} {bl} {br}")
            case 1: #drive forward
                assert(fl >= 0 and fr >= 0 and bl >= 0 and br >= 0, f"{fl} {fr} {bl} {br}")
            case 2: #drive left
                assert(fl <= 0 and fr >= 0 and bl >= 0 and br <= 0, f"not sure the signs are right here {fl} {fr} {bl} {br}")
            case 3: #drive right and backwards
                assert(fl == 0 and fr <= 0 and bl <= 0 and br == 0, f"{fl} {fr} {bl} {br}")
            case 4: #rotate counterclockwise
                assert(fl <= 0 and fr >= 0 and bl <= 0 and br >= 0, f"{fl} {fr} {bl} {br}")
            case _:
                assert(False, "something went wrong with cases")


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = mecanumLogic()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()