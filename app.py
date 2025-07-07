import chainlit as cl
from unsloth import FastLanguageModel
from transformers import AutoTokenizer

base_model = "unsloth/llama-3.2-3b-bnb-4bit"
adapter_path = "./Llama-3.2-3B-bnb-4bit-MedMCQA"

print("Loading base model...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = base_model,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

print("Loading LoRA adapter...")
model.load_adapter(adapter_path)
model.eval()

@cl.on_message
async def main(message: cl.Message):
    prompt = message.content

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=512)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    await cl.Message(content=response).send()
