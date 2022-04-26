#!/usr/bin/env python3

from example_service.srv import Fibonacci, FibonacciResponse
from std_msgs.msg import String
import rospy
import actionlib
import example_action_server.msg

rospy.init_node("fib_client", anonymous=True)
def fibonacci_server_client(x):
    rospy.wait_for_service("/service_node/calc_fibonacci")
    rospy.loginfo("waiting for startup")
    try:
        fibonacci = rospy.ServiceProxy("/service_node/calc_fibonacci", Fibonacci)
        resp1 = fibonacci(x)
        server_now_time= rospy.get_rostime()
        elapse_time = server_now_time-server_start_time
        rospy.loginfo("Server Elapsed Time = %i.%i", elapse_time.secs, elapse_time.nsecs)
        #rospy.logwarn(resp1.sequence)
        return resp1.sequence
    except rospy.ServiceException as e:
        rospy.logwarn("service call failed: %s" %e)

def fibonacci_action_client1():
    rospy.loginfo('action function running')
    client1 = actionlib.SimpleActionClient('/action_node/fibonacci', example_action_server.msg.FibonacciAction)
    client1.wait_for_server()                                    #wait for server to start
    #rospy.loginfo('waiting for server')
    goal1 = example_action_server.msg.FibonacciGoal(order=3)    #set up goal
    client1.send_goal(goal1)                                      #send goal
    #rospy.loginfo('sending goal')
    client1.wait_for_result()                     #wait for result or have node continue other operations
    #rospy.loginfo('waiting for result')
    action_finish_time = rospy.get_rostime()
    action_elapse_time = action_finish_time-action_start_time
    rospy.loginfo("Action1 Elapsed Time = %i.%i", action_elapse_time.secs, action_elapse_time.nsecs)
    return client1.get_result()                                #get final result

def fibonacci_action_client2():
    rospy.loginfo('action function running')
    client2 = actionlib.SimpleActionClient('/action_node/fibonacci', example_action_server.msg.FibonacciAction)
    client2.wait_for_server()                                    #wait for server to start
    #rospy.loginfo('waiting for server')    
    goal2 = example_action_server.msg.FibonacciGoal(order=15)
    client2.send_goal(goal2)                                      #send goal
    #rospy.loginfo('sending goal')
    client2.wait_for_result()                     #wait for result or have node continue other operations
    #rospy.loginfo('waiting for result')
    action_finish_time = rospy.get_rostime()
    action_elapse_time = action_finish_time-action_start_time
    rospy.loginfo("Action2 Elapsed Time = %i.%i", action_elapse_time.secs, action_elapse_time.nsecs)
    return client2.get_result()                                #get final result





if __name__=="__main__":
    #rospy.loginfo("function")
    server_start_time = rospy.get_rostime()
    fibonacci_server_client(3)
    fibonacci_server_client(15) 
    try:
        #rospy.init_node('fibonacci_client.py')
        action_start_time = rospy.get_rostime()
        result = fibonacci_action_client1()
        result = fibonacci_action_client2()
        rospy.loginfo("result:",','.join([str(n) for n in result.sequence]))
    except rospy.ROSInterruptException:
        rospy.logwarn("program interrupted before completion", file=sys.stderr)
        