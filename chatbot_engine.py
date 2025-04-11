from transformers import AutoTokenizer, AutoModelForCausalLM
from googletrans import Translator
from langdetect import detect
import torch

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en" 

translator = Translator()

def translate_text(text, dest_lang):
    try:
        result = translator.translate(text, dest=dest_lang)
        return result.text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def load_model():
    tokenizer = AutoTokenizer.from_pretrained("model/finetuned_llama3.2")
    model = AutoModelForCausalLM.from_pretrained("model/finetuned_llama3.2")

    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    return tokenizer, model

tokenizer, model = load_model()

def chatbot_response(user_input, merchant_name, insights):

    user_lang = detect_language(user_input)
    user_input_en = translate_text(user_input, "en") if user_lang != "en" else user_input

    system_message = f"""
    You are an intelligent AI assistant for merchants on Grab. 
    You assist a merchant named '{merchant_name}' by answering questions related to their sales, top-selling items, and business performance.
    Feel free to understand and respond in the language the user speaks — including English, Malay, Chinese, Tamil, and more.
    Here are the current performance insights:
    - Total orders: {insights['total_orders']}
    - Total sales: RM{insights['total_sales']:.2f}
    - Average order value: RM{insights['avg_order_value']:.2f}
    - Top items: {', '.join(insights['top_items'].keys())}
    - Alerts: {', '.join(insights['alerts']) if insights['alerts'] else 'None'}

    Keep your response short, friendly, and actionable.
    """

    input_text = f"{system_message}\nUser: {user_input_en}\nAssistant:"

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    # Use tokenizer that returns attention_mask
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=2048)
    input_ids = inputs["input_ids"].to(device)
    attention_mask = inputs["attention_mask"].to(device)

    outputs = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=500,
        temperature=0.7,
        top_p=0.9,
        do_sample=True,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.pad_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response_text = response.split("Assistant:")[-1].strip()

    return response_text
