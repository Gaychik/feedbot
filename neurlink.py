import requests 
import pprint
import json
token = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImExM2YyMjExLWVkOGUtNDE4YS05NzA4LTNhYTkwOTRhMjEzYyIsImV4cCI6NDkwMzI1OTc3OX0.Ln6dXoCHq1nmwTFb8lnOVbIHDqhq3_Kz5bzZcjkS604fbdq6RpmZeOFuGnSLAcILa0u2cEgIBfemUJkB7q3V_g"
name_model = None
def get_models():
        with open("models.json",encoding="utf-8") as file: 
          return json.load(file)

def set_model(name):
     global name_model
     name_model=name

def run(content):    
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        if name_model==None:
             raise Exception("Выберите модель для запроса!")
        data = {
            "model": name_model,
            "messages": [
                {
                    "role": "system",
                    "content": "Разговаривай на русском языке. Ответы должны быть не более 10 предложений. "
                },
                {
                    "role": "user",
                    "content": content
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


# response = requests.get(url, headers=headers)
# ans =  response.json()
# models = []
# for i in ans['data']:
#     models.append(i['id'])
# pprint.pprint(models)


