import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai
import panel as pn

# Load API key
_ = load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Use the correct model name
model = genai.GenerativeModel(model_name="gemini-2.5-flash")

# Panel GUI setup
pn.extension()

# Chat history and display panels
context = [{
    'role': 'user',
    'parts': ["""
You are OrderBot, an automated service to collect orders for a pizza restaurant.
You first greet the customer, then collect the order,
and then ask if it's a pickup or delivery.
You wait to collect the entire order, then summarize it and check for a final
time if the customer wants to add anything else.
If it's a delivery, you ask for an address.
Finally you collect the payment.
Make sure to clarify all options, extras and sizes to uniquely
identify the item from the menu.
You respond in a short, very conversational friendly style.
The menu includes:
- Pepperoni pizza: 12.95 (large), 10.00 (medium), 7.00 (small)
- Cheese pizza: 10.95 (large), 9.25 (medium), 6.50 (small)
- Eggplant pizza: 11.95 (large), 9.75 (medium), 6.75 (small)
- Fries: 4.50 (large), 3.50 (small)
- Greek salad: 7.25

Toppings:
- Extra cheese: 2.00
- Mushrooms: 1.50
- Sausage: 3.00
- Canadian bacon: 3.50
- AI sauce: 1.50
- Peppers: 1.00

Drinks:
- Coke: 3.00 (large), 2.00 (medium), 1.00 (small)
- Sprite: 3.00 (large), 2.00 (medium), 1.00 (small)
- Bottled water: 5.00
"""]
}]
panels = []

# Input widget
inp = pn.widgets.TextInput(value="Hi", placeholder="Enter your message…")
button_conversation = pn.widgets.Button(name="Chat!")

# Chat handler
def collect_messages(_):
    user_input = inp.value
    inp.value = ''
    context.append({'role': 'user', 'parts': [user_input]})
    response = model.generate_content(
    context,
    generation_config={"temperature": 0.0}  # You can adjust this value
)

    bot_reply = response.text
    context.append({'role': 'model', 'parts': [bot_reply]})
    panels.append(pn.Row('User:', pn.pane.Markdown(user_input, width=600)))
    panels.append(pn.Row('OrderBot:', pn.pane.Markdown(bot_reply, width=600)))  # ✅ No style argument
    return pn.Column(*panels)

# Bind button to chat handler
interactive_conversation = pn.bind(collect_messages, button_conversation)

# Build dashboard
dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard.servable()