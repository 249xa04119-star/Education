import streamlit as st
import pandas as pd
from database import init_db, save_result, get_all_results
from utils import generate_explanation, generate_adaptive_questions, generate_pdf

init_db()

st.set_page_config(page_title="AI Inclusive Learning System", layout="wide")
st.title("🎓 AI-Powered Concept Gap Detection System")

role = st.sidebar.selectbox("Login As", ["Student", "Teacher"])
username = st.sidebar.text_input("Enter Username")

questions = [
    {"question": "Solve: 2x + 5 = 15", "answer": "5", "topic": "Algebra"},
    {"question": "Area of circle formula?", "answer": "pi r^2", "topic": "Geometry"},
    {"question": "Solve: 3x = 12", "answer": "4", "topic": "Algebra"},
    {"question": "90 degrees is called?", "answer": "right angle", "topic": "Geometry"},
]

# ================= STUDENT =================

if role == "Student" and username:

    st.header("📘 Take Quiz")

    student_answers = []
    for i, q in enumerate(questions):
        ans = st.text_input(f"Q{i+1}: {q['question']}")
        student_answers.append(ans)

    language = st.selectbox("Choose Explanation Language", ["English", "Telugu"])

    if st.button("Submit Quiz"):

        results = []

        for i in range(len(questions)):
            correct = student_answers[i].strip().lower() == questions[i]["answer"].lower()
            results.append({
                "Topic": questions[i]["topic"],
                "Correct": correct
            })

        df = pd.DataFrame(results)
        topic_accuracy = df.groupby("Topic")["Correct"].mean()

        st.subheader("📊 Performance Analysis")
        st.dataframe(topic_accuracy)

        overall_score = topic_accuracy.mean()

        if overall_score < 0.4:
            st.error("⚠️ High Academic Risk")
        elif overall_score < 0.6:
            st.warning("⚠️ Moderate Academic Risk")
        else:
            st.success("✅ Low Academic Risk")

        weak_topics = topic_accuracy[topic_accuracy < 0.5].index.tolist()

        if weak_topics:
            for topic in weak_topics:
                st.subheader(f"📘 AI Explanation for {topic}")
                explanation = generate_explanation(topic, language)
                st.write(explanation)

                st.subheader("📝 Adaptive Practice Questions")
                adaptive_q = generate_adaptive_questions(topic)
                st.write(adaptive_q)

        for topic, acc in topic_accuracy.items():
            save_result(username, topic, acc)

        pdf_file = generate_pdf(username, topic_accuracy)

        with open(pdf_file, "rb") as f:
            st.download_button("📄 Download Performance Report", f, file_name=pdf_file)

# ================= TEACHER =================

if role == "Teacher":

    st.header("👩‍🏫 Teacher Dashboard")

    data = get_all_results()

    if data:
        df = pd.DataFrame(data, columns=["Username", "Topic", "Accuracy", "Timestamp"])
        st.dataframe(df)

        st.subheader("📊 Concept Heatmap")
        heatmap = df.groupby("Topic")["Accuracy"].mean()
        st.bar_chart(heatmap)

        st.subheader("🏫 School Analytics")
        overall_avg = df["Accuracy"].mean()
        st.metric("Overall School Performance", f"{round(overall_avg*100,2)}%")

        strongest = df.groupby("Topic")["Accuracy"].mean().idxmax()
        weakest = df.groupby("Topic")["Accuracy"].mean().idxmin()

        st.success(f"Strongest Topic: {strongest}")
        st.error(f"Weakest Topic: {weakest}")

    else:
        st.info("No student data available yet.")
