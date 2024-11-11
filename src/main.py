#region VEXcode Generated Robot Configuration
from vex import *
import urandom

# Brain should be defined by default
brain=Brain()

# Robot configuration code
left_motor_a = Motor(Ports.PORT8, GearSetting.RATIO_6_1, False)
left_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_6_1, False)
left_motor_c = Motor(Ports.PORT20, GearSetting.RATIO_6_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
right_motor_b = Motor(Ports.PORT5, GearSetting.RATIO_6_1, True)
right_motor_c = Motor(Ports.PORT11, GearSetting.RATIO_6_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain_inertial = Inertial(Ports.PORT1)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, drivetrain_inertial, 299.24, 320, 40, MM, 1)
controller_1 = Controller(PRIMARY)
optical = Optical(Ports.PORT15)


# wait for rotation sensor to fully initialize
wait(30, MSEC)

vexcode_initial_drivetrain_calibration_completed = False
def calibrate_drivetrain():
    # Calibrate the Drivetrain Inertial
    global vexcode_initial_drivetrain_calibration_completed
    sleep(200, MSEC)
    brain.screen.print("Calibrating")
    brain.screen.next_row()
    brain.screen.print("Inertial")
    drivetrain_inertial.calibrate()
    while drivetrain_inertial.is_calibrating():
        sleep(25, MSEC)
    vexcode_initial_drivetrain_calibration_completed = True
    brain.screen.clear_screen()
    brain.screen.set_cursor(1, 1)


# Calibrate the Drivetrain
calibrate_drivetrain()

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")



# define variables used for controlling motors based on controller inputs
drivetrain_l_needs_to_be_stopped_controller_1 = False
drivetrain_r_needs_to_be_stopped_controller_1 = False

# define a task that will handle monitoring inputs from controller_1
def rc_auto_loop_function_controller_1():
    global drivetrain_l_needs_to_be_stopped_controller_1, drivetrain_r_needs_to_be_stopped_controller_1, remote_control_code_enabled
    # process the controller input every 20 milliseconds
    # update the motors based on the input values
    while True:
        if remote_control_code_enabled:
            # stop the motors if the brain is calibrating
            if drivetrain_inertial.is_calibrating():
                left_drive_smart.stop()
                right_drive_smart.stop()
                while drivetrain_inertial.is_calibrating():
                    sleep(25, MSEC)
            
            # calculate the drivetrain motor velocities from the controller joystick axies
            # left = axis3
            # right = axis2
            drivetrain_left_side_speed = controller_1.axis3.position()
            drivetrain_right_side_speed = controller_1.axis2.position()
            
            # check if the value is inside of the deadband range
            if drivetrain_left_side_speed < 5 and drivetrain_left_side_speed > -5:
                # check if the left motor has already been stopped
                if drivetrain_l_needs_to_be_stopped_controller_1:
                    # stop the left drive motor
                    left_drive_smart.stop()
                    # tell the code that the left motor has been stopped
                    drivetrain_l_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the left motor next
                # time the input is in the deadband range
                drivetrain_l_needs_to_be_stopped_controller_1 = True
            # check if the value is inside of the deadband range
            if drivetrain_right_side_speed < 5 and drivetrain_right_side_speed > -5:
                # check if the right motor has already been stopped
                if drivetrain_r_needs_to_be_stopped_controller_1:
                    # stop the right drive motor
                    right_drive_smart.stop()
                    # tell the code that the right motor has been stopped
                    drivetrain_r_needs_to_be_stopped_controller_1 = False
            else:
                # reset the toggle so that the deadband code knows to stop the right motor next
                # time the input is in the deadband range
                drivetrain_r_needs_to_be_stopped_controller_1 = True
            
            # only tell the left drive motor to spin if the values are not in the deadband range
            if drivetrain_l_needs_to_be_stopped_controller_1:
                left_drive_smart.set_velocity(drivetrain_left_side_speed, PERCENT)
                left_drive_smart.spin(FORWARD)
            # only tell the right drive motor to spin if the values are not in the deadband range
            if drivetrain_r_needs_to_be_stopped_controller_1:
                right_drive_smart.set_velocity(drivetrain_right_side_speed, PERCENT)
                right_drive_smart.spin(FORWARD)
        # wait before repeating the process
        wait(20, MSEC)

# define variable for remote controller enable/disable
remote_control_code_enabled = True

rc_auto_loop_thread_controller_1 = Thread(rc_auto_loop_function_controller_1)

#endregion VEXcode Generated Robot Configuration

myVariable = 0

def ring_object_detected():
    global optical
    brain.screen.next_row()
    brain.screen.print("Object Found - ")
    brain.screen.print(optical.rgb(True))
    drivetrain.stop()
    if optical.color() == Color.BLUE:
        brain.screen.next_row()
        brain.screen.print("Blue Object")
    
    if optical.color() == Color.RED:
        brain.screen.next_row()
        brain.screen.print("Red Object")

def when_started1():
    global vexcode_initial_drivetrain_calibration_completed
    while not vexcode_initial_drivetrain_calibration_completed:
        wait (100, MSEC)
    drivetrain.set_heading(0, RotationUnits.DEG)
    optical.set_light_power(75, PercentUnits.PERCENT)
    optical.set_light(LedStateType.ON)
    optical.object_detected(ring_object_detected)

def onauton_autonomous_0():
    global myVariable
    drivetrain.set_drive_velocity(10, VelocityUnits.PERCENT)
    drivetrain.turn_to_heading(-45, RotationUnits.DEG)
    drivetrain.drive_for(FORWARD, 40, DistanceUnits.IN)
    drivetrain.turn_to_heading(-90, RotationUnits.DEG, 5, VelocityUnits.PERCENT)
    drivetrain.drive_for(REVERSE, 10, DistanceUnits.IN)
    drivetrain.turn_to_heading(-180, RotationUnits.DEG, 5, VelocityUnits.PERCENT)
    drivetrain.drive_for(FORWARD, 48, DistanceUnits.IN)
    drivetrain.turn_to_heading(-90, RotationUnits.DEG, 5, VelocityUnits.PERCENT)
    drivetrain.drive_for(FORWARD, 48, DistanceUnits.IN)

def ondriver_drivercontrol_0():
    global myVariable
    while True:
        wait(5, MSEC)

# create a function for handling the starting and stopping of all autonomous tasks
def vexcode_auton_function():
    # Start the autonomous control tasks
    auton_task_0 = Thread( onauton_autonomous_0 )
    # wait for the driver control period to end
    while( competition.is_autonomous() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the autonomous control tasks
    auton_task_0.stop()

def vexcode_driver_function():
    # Start the driver control tasks
    driver_control_task_0 = Thread( ondriver_drivercontrol_0 )

    # wait for the driver control period to end
    while( competition.is_driver_control() and competition.is_enabled() ):
        # wait 10 milliseconds before checking again
        wait( 10, MSEC )
    # Stop the driver control tasks
    driver_control_task_0.stop()


# register the competition functions
competition = Competition( vexcode_driver_function, vexcode_auton_function )

when_started1()
