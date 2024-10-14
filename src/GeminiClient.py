import google.generativeai as genai
import os 
import json
import subprocess
from dotenv import load_dotenv

class GeminiClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GENAI_API_KEY')

    def send_to_gemini(self, natural_language_config):
        prompt = f'Extract the variables from the following message and return them in JSON format, Return only the JSON object without any explanations or text formatting like backticks or extra characters, using the following keys: number_of_tables, number_of_waiters, simulation_duration, arrival_rate, initial_temp, final_temp, alpha, max_iter, nights_per_layout. If the message doesnt include some value, ignore it. The instruction is: {natural_language_config}'
        
        command = [
            'curl',
            '-H', 'Content-Type: application/json',
            '-d', json.dumps({"contents": [{"parts": [{"text": prompt}]}]}),
            '-X', 'POST', f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}'
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)
        
        print(result.stdout)

        return result.stdout

    def process_gemini_response(self, response):
        response_json = json.loads(response) 

        extracted_text = response_json['candidates'][0]['content']['parts'][0]['text'] 

        try:
            extracted_data = json.loads(extracted_text)
        except json.JSONDecodeError as e:
            print(f"Error al convertir la respuesta en JSON: {e}")
            return None

        with open('config.json', 'r') as file:
            config = json.load(file)

        for key, value in extracted_data.items():
            if value is not None:  # Solo actualizamos si el valor no es null
                config[key] = value

        with open('config.json', 'w') as file:
            json.dump(config, file, indent=4, separators=(',', ': '))