import time
import re
import logging

class VLMClient:

    def __init__(self, model_name, prompt_template):
        self.model_name = model_name
        self.prompt_template = prompt_template
        logging.info("VLMClient initialized with model: %s", self.model_name)
        # Note: In real deployment, model loading (e.g., HuggingFace transformers) happens here.

    def infer_state(self, image_array):
        # In actual deployment, this would be:
        # inputs = processor(text=self.prompt_template, images=image_array, return_tensors="pt")
        # generated_ids = model.generate(**inputs)
        # response = processor.batch_decode(...)
        
        # Simulating VLM inference delay (~3.8s as reported in the paper on RTX 3060 Laptop)
        time.sleep(3.8)
        
        # Simulating a successful VLM extraction
        mock_vlm_response = "148.5" 
        
        return self._parse_temperature(mock_vlm_response)

    def _parse_temperature(self, text):
        match = re.search(r'\d+\.\d+|\d+', text)
        if match:
            return float(match.group())
        else:
            logging.warning("VLM Hallucination or failed extraction: %s", text)
            return None
