import streamlit as st
from openai import OpenAI
import matplotlib.pyplot as plt
import numpy as np

# Load OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

import time
from openai import RateLimitError, APIError, Timeout

def query_gpt(prompt):
    max_retries = 5
    delay = 5  # Start with 5 seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Zoe, an AI tutor who explains clearly with examples."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content

        except RateLimitError:
            st.warning(f"⚠️ Rate limit hit. Waiting {delay} seconds before retrying...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff

        except (APIError, Timeout) as e:
            st.warning(f"Temporary OpenAI error: {str(e)} — Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2

    return "❌ Sorry, Zoe hit the rate limit too many times. Please try again later."


# Function to visualize linear regression
def show_linear_regression_plot():
    st.subheader("📈 Linear Regression Visual Explanation")

    # Generate sample data
    np.random.seed(1)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # Fit a simple linear regression line
    X_b = np.c_[np.ones((100, 1)), X]
    theta_best = np.linalg.inv(X_b.T.dot(X_b)).dot(X_b.T.dot(y))

    X_new = np.array([[0], [2]])
    X_new_b = np.c_[np.ones((2, 1)), X_new]
    y_predict = X_new_b.dot(theta_best)

    fig, ax = plt.subplots()
    ax.plot(X_new, y_predict, "r-", label="Prediction Line")
    ax.scatter(X, y, alpha=0.6)
    ax.set_xlabel("X")
    ax.set_ylabel("y")
    ax.set_title("Simple Linear Regression")
    ax.legend()

    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Zoe - Your AI Tutor", page_icon="🧠")
st.title("👩‍🏫 Zoe - Your Personal AI Tutor")

st.markdown("Ask me anything about Machine Learning, Math, or Science!")

# User input
user_question = st.text_input("What would you like to learn?", "")

if user_question:
    st.info("Zoe is thinking...")
    response = query_gpt(user_question)
    st.success("Here's Zoe's answer:")
    st.write(response)

    # Show visual aid for certain topics
    if "linear regression" in user_question.lower():
        show_linear_regression_plot()
import streamlit as st

try:
    response = query_gpt(user_question)
    st.write(response.choices[0].message.content)
except openai.RateLimitError:
    st.warning("Rate limit exceeded. Please wait a moment and try again.")
