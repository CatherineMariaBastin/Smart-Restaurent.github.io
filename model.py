import openai

# Set up OpenAI API Key
openai.api_key = "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"
def get_ai_recommendation(order_history):
    prompt = f"Suggest a menu item based on these past orders: {order_history}. Keep it short."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful restaurant AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# Example usage
if __name__ == "__main__":
    order_history = ["Margherita Pizza", "Garlic Bread", "Coke"]
    print(get_ai_recommendation(order_history))
