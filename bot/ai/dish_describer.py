import requests 
import pprint
import json
from dotenv import load_dotenv
import os
load_dotenv()
token = os.getenv("TOKEN_AI")
name_model = None

def run():    
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        data = {
            "model": name_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Представь что ты повар."
                },
                {
                    "role": "user",
                    "content": 
                    ("Тебя попросили описать блюдо: выдать историческую справку, "
                    "а также выдать расчет БЖУ. Формат ответа строгий:"
                    "Историческая справка"
                    "Расчет БЖУ"
                    "Рекомендации")
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        result = response.json()
        if 'choices' in result:
            result = result['choices'][0]['message']['content']
            if "<think>" in result:
                result = result.split("</think>")[-1]
        return result
