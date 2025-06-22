import os
import json
from dotenv import load_dotenv
import chainlit as cl
from litellm import acompletion  # Correct async function for LLM call

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env")

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])
    await cl.Message(
        content="Welcome to the **Translator Agent By Ayesha Aaqil**\n\nPlease tell me **what you want to translate** and **into which language?**"
    ).send()

@cl.on_message
async def on_message(message: cl.Message):  # Corrected class name
    msg = cl.Message(content="Translating...!")
    await msg.send()

    history = cl.user_session.get("chat_history") or []
    history.append({"role": "user", "content": message.content})

    try:
        response = await acompletion(  # Correct async call
            model="gemini/gemini-1.5-flash",
            api_key=gemini_api_key,
            messages=history
        )
        response_content = response.choices[0].message.content
        msg.content = response_content
        await msg.update()

        history.append({"role": "assistant", "content": response_content})
        cl.user_session.set("chat_history", history)

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()

@cl.on_chat_end
async def on_chat_end():
    history = cl.user_session.get("chat_history") or []
    with open("translation_chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
    print("Chat history saved.")
