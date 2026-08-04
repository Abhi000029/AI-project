
import random

responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "hello": ["Hi!", "Hello!", "Hey, how are you?"],
    "how are you": ["I'm good, thanks!", "Doing great!", "All good!"],
    "name": ["I'm PyBot.", "You can call me PyBot."],
    "joke": [
        "Why do Python devs prefer dark mode? Because light attracts bugs!",
        "I told my computer I needed a break — it said 'No problem, I'll go to sleep.'",
    ],
    "help": ["I can chat! Try: hi, joke, name, time, bye"],
    "time": [],  # handled separately
}
while True:
    user = input("YOU: ").lower()
    if user == "bye":
        print("BOT:responses['bye']")
        break
    print("BOT:", responses.get(user,"Sorry,I dont understand :"), user)

import google.generativeai as genai
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-flash-latest ")
print("AI chatbot")
print("Type 'exit' to quit.\n")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        print("bot. Goodbye!")
        break
    response = model.generate_text(user)
    print("Bot:", response.text)

import requests
url = ""
response = requests.get(url)
print(response.json())


import requests
url =""
data={
    "title":"learning AI",
    "body":"Today i learned about Ai and its applications",
    "userID": 1
}
response = requests.post(url,json=data)
print(response.status_code)
print(response.json())


import requests
url = ""
response = requests.get(url)
data = response.json()
print(data)

print("name:", data.get("name"))
print("predicted age:", data.get("age"))
# Note: 'major' is not a field returned by the Agify API.
if "major" in data:
    print("major:", data["major"])
else:
    print("major: Field not found in API response")


import json
text = '{"name":"john","age":"20","major":"computer science","courses":["DS","Algorithm","Math"]}'
obj = json.loads(text)
print(obj["name",])
print(obj["age",])
print(obj["major",])

import requests
url = ""
response = requests.get(url)
print(response.json())

print("name:",response.json()["name"])
print("predicted age:",response.json()["age"])
print("major:",response.json()["major"])

import requests
username = input("Enter your username: ")
password = input("Enter your password: ")
url = f"/{username}"
response = requests.get(url)
print(response.json())

import requests
url = ""
response = requests.get(url)
print(response.json())

import requests
url = ""
response = requests.get(url)
print(response.json())

import google.generativeai as genai
genai.configure(api_key="")
model = genai.GenerativeModel("gemini-flash-latest")
print("AI chatbot")
print("Type 'exit' to quit.\n")
while True:
    user = input("You: ")
    if user.lower() == "exit":
        print("bot. Goodbye!")
        break
    response = model.generate_content(user)
    print("Bot:", response.text)