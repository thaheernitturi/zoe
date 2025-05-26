import streamlit as st
import time
from openai import OpenAI, RateLimitError, APIError, Timeout

# Load API key safely
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Offline fallback content
FALLBACK_ANSWERS = {
    "linear regression": "Linear regression is a statistical method that models the relationship between a dependent variable and one or more independent variables using a straight line. It's often used to predict outcomes based on trends in data.",
    "logistic regression": "Logistic regression is used when the dependent variable is categorical (like yes/no, 0/1). It estimates probabilities using a logistic (sigmoid) function and is widely used for binary classification.",
    "overfitting": "Overfitting happens when a model learns noise in the training data instead of the actual pattern. It performs well on training data but poorly on unseen data.",
    "underfitting": "Underfitting occurs when a model is too simple to learn the underlying structure of the data, resulting in poor performance on both training and test data.",
    "precision recall": "Precision is the ratio of true positives to total predicted positives, while recall is the ratio of true positives to all actual positives. Precision is about exactness, and recall is about completeness."
}


def find_fallback_answer(prompt):
    prompt_lower = prompt.lower()
    for topic, answer in FALLBACK_ANSWERS.items():
        if topic in prompt_lower:
            return answer
    return "❌ Sorry, Zoe couldn't find an offline explanation for that topic."


def query_gpt_with_fallback(prompt):
    models = ["gpt-4", "gpt-3.5-turbo"]
    delay = 5

    for model in models:
        for attempt in range(3):
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are Zoe, an AI tutor that explains concepts clearly with examples."},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            except RateLimitError:
                st.warning(f"⚠️ Rate limit hit for {model}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            except (APIError, Timeout) as e:
                st.warning(f"🔁 Temporary error with {model}: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        st.info(f"⏭️ Switching to fallback model...")

    # Offline fallback
    return find_fallback_answer(prompt)


# --- Streamlit App UI ---
st.set_page_config(page_title="Zoe - AI Tutor", page_icon="📘")
st.title("🧠 Zoe - Your AI Learning Assistant")
st.markdown("""
Zoe helps explain technical topics like a kind and knowledgeable tutor. Ask anything about ML, AI, stats, or coding!
""")

user_question = st.text_input("What would you like Zoe to explain?", placeholder="E.g., What is linear regression?")

if user_question:
    st.info("💡 Zoe is thinking...")
    answer = query_gpt_with_fallback(user_question)
    st.success("✅ Zoe's Answer:")
    st.write(answer)

    # Optional: Custom visuals for some topics
    if "linear regression" in user_question.lower():
        import matplotlib.pyplot as plt
        import numpy as np

        X = np.linspace(0, 10, 50)
        y = 2.5 * X + 1.0 + np.random.randn(50)

        fig, ax = plt.subplots()
        ax.scatter(X, y, label='Data')
        ax.plot(X, 2.5 * X + 1.0, color='red', label='Regression Line')
        ax.set_title("Linear Regression Example")
        ax.legend()
        st.pyplot(fig)
