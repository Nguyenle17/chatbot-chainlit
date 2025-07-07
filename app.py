import chainlit as cl
import requests

SERVER_URL = "https://eceb1a9338f2.ngrok-free.app/chat"

@cl.on_chat_start
async def on_chat_start():
    elements = [
        cl.Image(name="doctor_avatar", display="inline", path="assets/doctor.png")
    ]
    
    await cl.Message(
        content="👩‍⚕️ Xin chào! Tôi là trợ lý y khoa AI. Bạn muốn hỏi gì hôm nay?",
        elements=elements
    ).send()

@cl.on_message
async def on_message(message: cl.Message):
    prompt = message.content

    try:
        res = requests.post(SERVER_URL, json={"prompt": prompt})
        res.raise_for_status()
        response = res.json().get("response", " Không nhận được phản hồi hợp lệ từ mô hình.")
    except Exception as e:
        response = f"Lỗi khi kết nối tới server: {e}"

    msg = cl.Message(content="Đang suy nghĩ...")  
    await msg.send()
    
    msg.content = response
    await msg.update()
