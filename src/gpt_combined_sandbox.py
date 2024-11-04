import requests
import base64
import time
import threading
import json

class GPTCookingAssistant:
    def __init__(self, api_key, image_data):
        self.api_key = api_key
        self.base_prompt = (
            "You are a cooking assistant robot in a kitchen setting, designed to help and interact with people as they prepare food. "
            "Your first task is to greet the person as they approach you, and then engage in a conversation with them to determine how you can assist. "
            "Based on the person’s responses, offer help with recipe suggestions, step-by-step cooking instructions, or ingredient recommendations. "
            "Keep the tone friendly, helpful, and encouraging, and ask questions to clarify what the person wants to cook. "
            "Additionally, incorporate any ingredient data available to enhance your suggestions or provide context."
        )
        self.image_data = image_data

    def create_payload(self, user_input, table_status=None, max_tokens=500):
        prompt = self.base_prompt
        if table_status:
            prompt += f" Current table status: {json.dumps(table_status)}."

        payload = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_input}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        return payload

    def gpt_call(self, user_input, table_status=None):
        payload = self.create_payload(user_input, table_status)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response)
        response = response.json()
        print(response)
        ans = response['choices'][0]['message']['content']
        return ans

    def start_conversation(self):
        print("Cooking Assistant: Hello! How can I assist you in the kitchen today?")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Cooking Assistant: Goodbye! Happy cooking!")
                break

            # Access recent image data if available
            table_status = None
            if self.image_data:
                latest_data = self.image_data[-1]
                try:
                    # Attempt to parse the latest data as JSON if it's not already in dict format
                    table_status = json.loads(latest_data) if isinstance(latest_data, str) else latest_data
                    print("Current table status:", table_status)
                except json.JSONDecodeError:
                    print("Error decoding table status JSON.")

            assistant_response = self.gpt_call(user_input, table_status)
            print(f"Cooking Assistant: {assistant_response}")

class GPTImageAnalyzer:
    def __init__(self, api_key, image_data):
        self.api_key = api_key
        self.base_prompt = '''
        For the provided image and question, generate only a scene graph in JSON format that includes the following:
        1. Objects that are relevant to answering the question
        2. Object attributes that are relevant to answering the question
        3. Object relationships that are relevant to answering the question
        '''
        self.image_data = image_data

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def create_payload(self, cur_img, cur_text, max_tokens=500):
        payload = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": [ 
                        {
                            "type": "text",
                            "text": cur_text
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{cur_img}"
                            }
                        }
                    ]
                }
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": max_tokens,
            "temperature": 0
        }
        return payload

    def gpt_call(self, image_path, question="What objects are on the image and where?"):
        base64_image = self.encode_image(image_path)
        payload = self.create_payload(base64_image, question + self.base_prompt)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        print(response)
        response = response.json()
        print(response)
        ans = response['choices'][0]['message']['content']
        return ans

    def run_periodically(self, image_path, interval=2):
        while True:
            json_response = self.gpt_call(image_path)
            # print("Image analysis result:", json_response)
            
            # Add the response to the shared list, maintaining a max size of 5
            if len(self.image_data) >= 5:
                self.image_data.pop(0)
            self.image_data.append(json_response)
            
            time.sleep(interval)


# Initialize shared list and API keys
image_data = []
# api_key = ""
api_key = ""

image_path = "./media/example_1.png"


# Initialize both agents
cooking_assistant = GPTCookingAssistant(api_key, image_data)
image_analyzer = GPTImageAnalyzer(api_key, image_data)

# Start the image analyzer in a separate thread
image_thread = threading.Thread(target=image_analyzer.run_periodically, args=(image_path,))
image_thread.daemon = True
image_thread.start()

# Start the cooking assistant
cooking_assistant.start_conversation()
