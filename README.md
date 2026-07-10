# VLM-Driven Cognitive Loop for Legacy Lab Equipment

This repository provides the core demonstration code for the closed-loop automation framework proposed in our paper: **"Non-Intrusive Closed-Loop Automation of Legacy Laboratory Equipment using Vision-Language Models and Collaborative Robots"**.

## Overview
To demonstrate the reproducibility and generalizability of our methodology, this repository isolates the core "Eye-Brain-Hand" cognitive loop. It abstracts away proprietary hardware SDKs (such as specific robot arm kinematics) while preserving the exact logical flow, perception preprocessing, and state-machine decision architecture presented in the paper.

## Repository Structure

- `config.yaml`: Centralized configuration for targets, Vision-Language Model (VLM) prompts, and visual ROI settings.
- `perception/`: The "Eye". Contains OpenCV-based preprocessing to mitigate environmental glare and sensor noise before feeding images to the VLM.
- `cognition/`: The "Brain". Handles VLM inference (prompting and parsing) and the deterministic state-machine logic for process control.
- `actuation/`: The "Hand". Abstracted robotic control interface for executing physical actions (e.g., button pressing).
- `main_closed_loop.py`: The entry point that runs the continuous Cyber-Physical feedback loop.

## Requirements
```bash
pip install opencv-python pyyaml
# Note: For actual VLM deployment (e.g., Qwen3-VL-8B), additional libraries such as transformers and torch are required.
```

## Usage
Run the simulated closed-loop process:
```bash
python main_closed_loop.py
```
