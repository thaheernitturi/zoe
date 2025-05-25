# Zoe: AI ML Tutor with Visuals, Auto-Grading, Memory
import openai
import streamlit as st
import json
import os
import tempfile
import subprocess
import sys
import traceback
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

# --- Configuration ---
openai.api_key = "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"
USER_ID = "default_user"
MEMORY_FILE = f"zoe_memory_{USER_ID}.json"
EXPECTED_OUTPUT = [3.1, 4.2, 5.3]

# --- Load/Save User Memory ---
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"topics": {}, "quizzes": {}}

def save_memory(data):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=2)

memory = load_memory()

# --- Prompt Templates ---
PROMPTS = {
    "explain": lambda topic: f"You are Zoe, an AI tutor. Explain the topic '{topic}' to a college student in simple language using analogies and visuals where possible. Ask a follow-up question at the end to test understanding.",
    "quiz": lambda topic: f"Create a beginner-level quiz with 3 questions (MCQs or coding tasks) about '{topic}' with correct answers.",
    "review_code": lambda code: f"You are Zoe, an AI tutor. A student submitted the following code. Give friendly, clear feedback on what they did right, what they can improve, and how to fix any errors.\n\nCode:\n{code}"
}

# --- GPT Query ---
def query_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are Zoe, a kind and helpful AI tutor who explains clearly and adapts to student level."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

# --- Code Auto-Evaluation ---
def run_user_code(user_code):
    try:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.py', delete=False) as tmp:
            code_file = tmp.name
            tmp.write(user_code + '\nprint(list(model.predict([[1], [2], [3]])))')

        result = subprocess.run([sys.executable, code_file], capture_output=True, text=True, timeout=10)
        os.remove(code_file)

        if result.returncode != 0:
            return f"Execution Error:\n{result.stderr}", None

        try:
            output = eval(result.stdout.strip())
        except Exception as e:
            return f"Output Parsing Error: {e}\nRaw output: {result.stdout}", None

        return None, output
    except Exception as e:
        return f"Fatal Error: {str(e)}", None

# --- Visualization Examples ---
def show_linear_regression_plot():
    X = np.array([1, 2, 3])
    y = np.array([3.1, 4.2, 5.3])
    coef = np.polyfit(X, y, 1)
    poly1d_fn = np.poly1d(coef)

    fig, ax = plt.subplots()
    ax.scatter(X, y, color='blue', label='Data')
    ax.plot(X, poly1d_fn(X), color='red', label='Regression Line')
    ax.set_title("Linear Regression Fit")
    ax.set_xlabel("X")
    ax.set_ylabel("y")
    ax.legend()
    st.pyplot(fig)

# --- Streamlit UI ---
st.title("Zoe - Your AI ML Mentor")

mode = st.sidebar.selectbox("What would you like help with?", [
    "Explain a Topic", "Quiz Me", "Review My Code", "Auto-Grade Code", "View My Progress"])

if mode == "Explain a Topic":
    topic = st.text_input("Enter ML topic (e.g. Linear Regression)")
    if st.button("Teach Me!") and topic:
        prompt = PROMPTS["explain"](topic)
        response = query_gpt(prompt)
        st.markdown(response)
        if "linear regression" in topic.lower():
            show_linear_regression_plot()
        memory["topics"].setdefault(topic, {"explained": 0})
        memory["topics"][topic]["explained"] += 1
        save_memory(memory)

elif mode == "Quiz Me":
    topic = st.text_input("Enter topic for quiz")
    if st.button("Generate Quiz") and topic:
        prompt = PROMPTS["quiz"](topic)
        response = query_gpt(prompt)
        st.markdown(response)
        memory["quizzes"].setdefault(topic, [])
        memory["quizzes"][topic].append({"attempted": True})
        save_memory(memory)

elif mode == "Review My Code":
    code = st.text_area("Paste your ML code")
    if st.button("Review Code") and code:
        prompt = PROMPTS["review_code"](code)
        response = query_gpt(prompt)
        st.markdown(response)

elif mode == "Auto-Grade Code":
    st.info("Try writing a Linear Regression model using sklearn. Your model should be named `model` and trained to predict [3.1, 4.2, 5.3] from inputs [[1], [2], [3]]")
    code = st.text_area("Paste your code for auto-grading")
    if st.button("Grade Me") and code:
        error, output = run_user_code(code)
        if error:
            st.error(error)
        else:
            st.success(f"Output: {output}")
            score = sum([abs(o - e) < 0.1 for o, e in zip(output, EXPECTED_OUTPUT)]) / len(EXPECTED_OUTPUT)
            st.markdown(f"**Score:** {round(score*100)}% correct")
            feedback_prompt = f"A student wrote this code to predict y = [3.1, 4.2, 5.3] from X = [[1], [2], [3]]. Evaluate it: {code}\n\nModel predictions: {output}. Expected: {EXPECTED_OUTPUT}"
            feedback = query_gpt(feedback_prompt)
            st.markdown("---")
            st.markdown("**Zoe’s Feedback:**")
            st.markdown(feedback)

elif mode == "View My Progress":
    st.subheader("Topics You’ve Explored")
    for topic, data in memory["topics"].items():
        st.markdown(f"- **{topic}**: Explained {data['explained']} time(s)")
    st.subheader("Quizzes Attempted")
    for topic, attempts in memory["quizzes"].items():
        st.markdown(f"- **{topic}**: {len(attempts)} attempt(s)")

st.markdown("---")
st.markdown("Zoe v0.4 | Visuals, Grading, and Memory | Built with GPT-4, Streamlit")
