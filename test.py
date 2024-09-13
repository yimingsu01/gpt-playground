from openai import OpenAI
from datetime import datetime

SYSTEM_PROMPT = "You are a cloud-native application expert. You are proficient in kubernetes."
MODEL = "gpt-4o"
INTERACTIVE = True

with open("./API_KEY", "r", encoding="utf-8") as f:
    api_key = f.readline()

client = OpenAI(api_key=api_key)

first_prompt = "Hello"

first_round = True
msg_arr = []
if INTERACTIVE:
    while INTERACTIVE:
        if first_round:
            msg_arr.append({"role": "system", "content": f"{SYSTEM_PROMPT}"})
            msg_arr.append({"role": "user", "content": f"{first_prompt}"})
            first_round = False

        response = client.chat.completions.create(
            model=MODEL,
            messages=msg_arr
        )

        response_str = response.choices[0].message.content

        print(f"AI: {response_str}\n")

        ai_response = response_str
        ai_msg = {"role": "assistant", "content": f"{ai_response}"}
        msg_arr.append(ai_msg)

        next_prompt = input("Human: ")
        match next_prompt:
            case "Q":
                exit(0)
            case "SAVE_CHAT":
                dt_string = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                print("date and time =", dt_string)
                with open(f"./{dt_string}.txt", "w", encoding="utf-8") as chat_history:
                    for msg in msg_arr:
                        role = msg["role"]
                        message = msg["content"]
                        line = f"{role}: {message}\n"
                        chat_history.write(line)
                exit(0)
            case _:
                next_usr_msg = {"role": "user", "content": f"{next_prompt}"}
                msg_arr.append(next_usr_msg)




