import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry


class mecanumFK(Node):
    def __init__(self) -> Node:
        super().__init__("mecanumIK checker")
        
        self.state_pub = self.create_publisher(JointState, "joint_state", 10)
        
        self.odom_sub = self.create_subscription(Odometry, "encoder_odom", self.odom_callback, 10)
        
        self.pose = Odometry()
        self.state = -1
        
        self.create_timer(1, self.timer_callback)
        
        self.states = [
            JointState( # Do nothing
                name=["front_left_wheel", "front_right_wheel", "back_left_wheel", "back_right_wheel"],
                velocity=[0.0,0.0,0.0,0.0]
            ), 
            JointState( #Drive forward
                name=["front_left_wheel", "front_right_wheel", "back_left_wheel", "back_right_wheel"],
                velocity=[1.0,1.0,1.0,1.0]
            ),
            JointState( #Drive Left
                name=["front_left_wheel", "front_right_wheel", "back_left_wheel", "back_right_wheel"],
                velocity=[-1.0,1.0,1.0,-1.0]
            ),
            JointState( #drive back and right
                name=["front_left_wheel", "front_right_wheel", "back_left_wheel", "back_right_wheel"],
                velocity=[0.0,-1.0,-1.0,0.0]
            )]
        self.timer_callback()
        
        
    def timer_callback(self) -> None:
        self.state += 1
        if not self.state in [0, 1, 2, 3]: self.state = 0
        self.state_pub(self.states[self.state])
    
    def odom_callback(self, msg: Odometry) -> None:
        last_pose = self.pose.pose.pose
        new_pose = msg.pose.pose
        
        xDif = new_pose.position.x - last_pose.position.x
        yDif = new_pose.position.y - last_pose.position.y
        
        match self.state:
            case 0: assert xDif == 0 and yDif == 0, f"Shouldnt be moving position {xDif} {yDif}"
            case 1: assert xDif > 0 and yDif == 0, f"shouldnt be moving sideways {xDif} {yDif}"
            case 2: assert xDif == 0 and yDif > 0, f"shouldnt be moving forwards {xDif} {yDif}"
            case 3: assert xDif < 0 and yDif < 0, f"should be moving back right {xDif} {yDif}"
        
        
        self.pose = msg