from groq import Groq
from json import dump,load
import datetime
from dotenv import dotenv_values
env_vars = dotenv_values(".env")

Username = env_vars.get("USERNAME")
AssistantName = env_vars.get("ASSISTANT_NAME")
GroqAPIKey = env_vars.get("GROQ_API_KEY")

client = Groq(api_key=GroqAPIKey)  # Initialize the Groq client with your API key

messages = []

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {AssistantName} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in English(until I ask), even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and do not mention your training data unitl I say. ***
"""

# a list of system instructions for the chatbot
SystemChatBot = [
    {"role": "system", "content": System}
]

try:
    with open(r"Data/ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data/ChatLog.json", "w") as f:
        dump([] , f)
        
def RealtimeInformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%h")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")
    
    data = f"Please use this real-time information if needed , \n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}\n"
    data += f"Hour: {hour}\nMinute: {minute}\nSecond: {second}\n"
    return data

def AnswerModifier(answer):
    lines = answer.split("\n")
    non_Empty_lines = [line for line in lines if line.strip()]
    modified_Ans = "\n".join(non_Empty_lines)
    return modified_Ans

def ChatBot(Query):
    try:
        with open(r"Data/ChatLog.json", "r") as f: 
            messages = load(f)
            
        messages.append({"role": "user", "content": f"{Query}"})
        
        completion = client.chat.completions.create(
                model="llama3-70b-8192",  # Specify the AI model to use.
                messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,# sys instruction  + realtime info + chat history
                max_tokens=2048,  # Limit the maximum tokens in the response.
                temperature=0.7,  # Adjust response randomness (higher means more random).
                top_p=1,  # Use nucleus sampling to control diversity.
                stream=True,  # Enable streaming response.
                stop=None  # Allow the model to determine when to stop.
            )
        Answer = ""  #AI response
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content
        Answer = Answer.replace("</s>", "") 
        
        messages.append({"role": "assistant", "content": Answer})  # Append the AI's response to the chat history.
        
        with open(r"Data/ChatLog.json", "w") as f:
            dump(messages, f, indent=4)  # Save the updated chat history to the file.
            
        return AnswerModifier(Answer)  # Return the modified answer.
    except Exception as e:
        print(f"Error: {e}")
        with open(r"Data/ChatLog.json", "w") as f:
            dump([], f, indent=4)
        return ChatBot(Query)  # Retry the function in case of an error.
    
if __name__ == "__main__":
    while True:
        user_input = input("Enter your Query: ")
        print(ChatBot(user_input))
        

        
        
    

