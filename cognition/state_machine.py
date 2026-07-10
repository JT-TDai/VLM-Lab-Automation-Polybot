import logging

class ThermalStateMachine:

    def __init__(self, target_temp, tolerance):
        self.target_temp = target_temp
        self.tolerance = tolerance

    def decide_action(self, current_temp):

        if current_temp is None:
            logging.error("Invalid temperature reading. Action: IDLE (Failsafe)")
            return "IDLE"

        delta = self.target_temp - current_temp
        
        if abs(delta) <= self.tolerance:
            return "IDLE"
        elif delta > self.tolerance:
            # Current temp is too low, need to increase
            return "PRESS_UP_BUTTON"
        else:
            # Current temp is too high, need to decrease
            return "PRESS_DOWN_BUTTON"
