import yaml
import time
import logging
import cv2

# Import custom modules demonstrating the Eye-Brain-Hand architecture
from perception.image_processor import ImageProcessor
from cognition.vlm_client import VLMClient
from cognition.state_machine import ThermalStateMachine
from actuation.robot_controller import RobotActuator

# Setup logging for demonstration output
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] %(message)s')

def load_config(config_path="config.yaml"):
    with open(config_path, "r") as file:
        return yaml.safe_load(file)

def main():
    logging.info("=== Starting VLM-Driven Cognitive Automation Loop ===")
    
    # 1. Load Configurations
    config = load_config()
    target_temp = config['task_settings']['target_temperature']
    tolerance = config['task_settings']['tolerance']
    
    # 2. Initialize Subsystems
    # The 'Eye'
    eye = ImageProcessor(
        roi_coords=config['perception_settings']['roi_coordinates'],
        apply_contrast_norm=config['perception_settings']['apply_contrast_norm']
    )
    # The 'Brain'
    vlm = VLMClient(
        model_name=config['vlm_settings']['model_name'],
        prompt_template=config['vlm_settings']['prompt_template']
    )
    state_machine = ThermalStateMachine(target_temp, tolerance)
    # The 'Hand'
    hand = RobotActuator()

    logging.info("System Ready. Target Temp: %.1f C. Beginning Closed-Loop...", target_temp)

    # 3. Enter Cyber-Physical Loop
    cycle_count = 0
    max_demo_cycles = 3  # Run for 3 cycles for demonstration purposes

    while cycle_count < max_demo_cycles:
        cycle_count += 1
        logging.info("--- Cycle %d Initiated ---", cycle_count)
        start_time = time.time()

        # Step A (Eye): Acquire and Preprocess Visual Feedback
        raw_frame = eye.capture_frame()
        processed_frame = eye.preprocess_for_vlm(raw_frame)
        logging.info("Step A: Visual feedback acquired and preprocessed.")

        # Step B (Brain - Perception): VLM Inference
        logging.info("Step B: Sending ROI to Vision-Language Model for state extraction...")
        current_temp = vlm.infer_state(processed_frame)
        logging.info("          > VLM Extracted State: Current Temp = %s C", current_temp)

        # Step C (Brain - Decision): State Machine Evaluation
        action_cmd = state_machine.decide_action(current_temp)
        logging.info("Step C: State Machine decided action -> %s", action_cmd)

        # Step D (Hand): Robotic Actuation
        logging.info("Step D: Executing action via Robot Actuator.")
        hand.execute_action(action_cmd)

        # Calculate latency
        elapsed_time = time.time() - start_time
        logging.info("--- Cycle %d Complete. Latency: %.2f seconds ---\n", cycle_count, elapsed_time)

        # Enforce loop interval (simulating thermodynamic lag)
        sleep_time = max(0, config['task_settings']['loop_interval_sec'] - elapsed_time)
        time.sleep(sleep_time)

    logging.info("=== Demonstration Completed Successfully ===")

if __name__ == "__main__":
    main()
