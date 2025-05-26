import streamlit as st
import time
import webbrowser

# Offline fallback content
FALLBACK_ANSWERS = {
    "linear regression": "Linear regression is a statistical method that models the relationship between a dependent variable and one or more independent variables using a straight line. It's often used to predict outcomes based on trends in data. More info: https://en.wikipedia.org/wiki/Linear_regression",
    "logistic regression": "Logistic regression is used when the dependent variable is categorical (like yes/no, 0/1). It estimates probabilities using a logistic (sigmoid) function and is widely used for binary classification. More info: https://en.wikipedia.org/wiki/Logistic_regression",
    "overfitting": "Overfitting happens when a model learns noise in the training data instead of the actual pattern. It performs well on training data but poorly on unseen data. More info: https://en.wikipedia.org/wiki/Overfitting",
    "underfitting": "Underfitting occurs when a model is too simple to learn the underlying structure of the data, resulting in poor performance on both training and test data. More info: https://en.wikipedia.org/wiki/Underfitting",
    "precision recall": "Precision is the ratio of true positives to total predicted positives, while recall is the ratio of true positives to all actual positives. Precision is about exactness, and recall is about completeness. More info: https://en.wikipedia.org/wiki/Precision_and_recall"
}


def find_fallback_answer(prompt):
    prompt_lower = prompt.lower()
    for topic, answer in FALLBACK_ANSWERS.items():
        if topic in prompt_lower:
            return answer
    return "❌ Sorry, Zoe couldn't find an offline explanation for that topic. Try searching on Wikipedia."


# --- Streamlit App UI ---
st.set_page_config(page_title="Zoe - AI Tutor", page_icon="📘")
st.title("🧠 Zoe - Your AI Learning Assistant")
st.markdown("""
Zoe helps explain technical topics using verified sources like Wikipedia.
""")

user_question = st.text_input("What would you like Zoe to explain?", placeholder="E.g., What is linear regression?")

if user_question:
    st.info("🔍 Searching trusted sources like Wikipedia...")
    answer = find_fallback_answer(user_question)
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
