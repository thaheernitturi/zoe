import streamlit as st
import time
import webbrowser

# Offline fallback content
FALLBACK_ANSWERS = {
    "linear regression": "Linear regression is a statistical method that models the relationship between a dependent variable and one or more independent variables using a straight line. It's often used to predict outcomes based on trends in data. More info: https://en.wikipedia.org/wiki/Linear_regression",
    "logistic regression": "Logistic regression is used when the dependent variable is categorical (like yes/no, 0/1). It estimates probabilities using a logistic (sigmoid) function and is widely used for binary classification. More info: https://en.wikipedia.org/wiki/Logistic_regression",
    "overfitting": "Overfitting happens when a model learns noise in the training data instead of the actual pattern. It performs well on training data but poorly on unseen data. More info: https://en.wikipedia.org/wiki/Overfitting",
    "underfitting": "Underfitting occurs when a model is too simple to learn the underlying structure of the data, resulting in poor performance on both training and test data. More info: https://en.wikipedia.org/wiki/Underfitting",
    "precision recall": "Precision is the ratio of true positives to total predicted positives, while recall is the ratio of true positives to all actual positives. Precision is about exactness, and recall is about completeness. More info: https://en.wikipedia.org/wiki/Precision_and_recall",
    "math": "Mathematics is the study of numbers, quantities, shapes, and patterns. It's a foundational discipline in science and technology. More info: https://en.wikipedia.org/wiki/Mathematics",
    "science": "Science is the systematic study of the structure and behavior of the physical and natural world through observation and experiment. More info: https://en.wikipedia.org/wiki/Science",
    "physics": "Physics is the branch of science concerned with the nature and properties of matter and energy. More info: https://en.wikipedia.org/wiki/Physics"
}


def find_fallback_answer(prompt):
    prompt_lower = prompt.lower()
    for topic, answer in FALLBACK_ANSWERS.items():
        if topic in prompt_lower:
            return answer
    return None


# --- Streamlit App UI ---
st.set_page_config(page_title="Zoe - AI Tutor", page_icon="📘")
st.title("👩‍🏫 Zoe - Your Personal AI Tutor")
st.markdown("""
Ask me anything about Machine Learning, Math, or Science!
Zoe now uses trusted sources like Wikipedia to ensure reliable offline access.
""")

user_question = st.text_input("What would you like to learn?", placeholder="E.g., What is linear regression?")

if user_question:
    with st.spinner("🔍 Zoe is searching trusted offline sources..."):
        time.sleep(1.5)
        answer = find_fallback_answer(user_question)

    if answer:
        st.success("✅ Zoe's Answer:")
        st.write(answer)
    else:
        st.warning("❌ Zoe couldn't find a direct answer. Let's search Wikipedia together:")
        search_query = user_question.replace(" ", "+")
        wiki_link = f"https://en.wikipedia.org/w/index.php?search={search_query}"
        st.markdown(f"[🔗 Search on Wikipedia]({wiki_link})")

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
