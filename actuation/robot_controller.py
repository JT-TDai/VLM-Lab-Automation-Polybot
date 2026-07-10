import time
import logging

class UR5eRemote:
    def __init__(self, robotIP):
        self.robotIP = robotIP
        self.port = 29999
        self.timeout = 5
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.getLogger().setLevel(logging.INFO)

    def connect(self):
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.robotIP, self.port))
        self.sock.recv(1096)

    def sendAndReceive(self, command):
        try:
            self.sock.sendall((command + '\n').encode())
            return self.get_reply()
        except (ConnectionResetError, ConnectionAbortedError):
            logging.warning('The connection was lost to the robot. Please connect and try running again.')
            self.close()
            sys.exit()

    def get_reply(self):
        """
        read one line from the socket
        :return: text until new line
        """
        collected = b''
        while True:
            part = self.sock.recv(1)
            if part != b"\n":
                collected += part
            elif part == b"\n":
                break
        return collected.decode("utf-8")
    
    def program_complete_check(self):
        while True:
            time.sleep(3)
            state = self.sendAndReceive('programState')
            
            if 'STOPPED' in state:
                break       
            else:
                continue

    def close(self):
        self.sock.close()

class RobotActuator:

    def __init__(self):
        logging.info("RobotActuator initialized and homed.")

    def execute_action(self, action_cmd):
        """
        Maps logical commands to physical robot trajectories.
        """
        if action_cmd == "IDLE":
            logging.info("Robot maintaining home position (No action required).")
            return

        logging.info("Robot beginning trajectory for command: %s", action_cmd)
        
        # Simulate physical movement time
        time.sleep(0.5) 
        
        if action_cmd == "PRESS_UP_BUTTON":
            self._move_and_press(target_button="UP")
        elif action_cmd == "PRESS_DOWN_BUTTON":
            self._move_and_press(target_button="DOWN")
        else:
            logging.warning("Unknown command received: %s", action_cmd)

    def _move_and_press(self, target_button):

        logging.info("--> [Kinematics] Moving End-Effector to %s button coords", target_button)
        logging.info("--> [Kinematics] Pressing button")
        logging.info("--> [Kinematics] Retracting to safe clearance plane")
