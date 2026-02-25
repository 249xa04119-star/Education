import os
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_explanation(topic, language="English"):
    if language == "Telugu":
        prompt = f"Explain {topic} in simple Telugu for a 10th class rural student with one example."
    else:
        prompt = f"Explain {topic} simply for a 10th class student with one example."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def generate_adaptive_questions(topic):
    prompt = f"Generate 3 simple practice questions for {topic} for a 10th class student."

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def generate_pdf(username, performance):
    filename = f"{username}_report.pdf"
    doc = SimpleDocTemplate(filename)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Performance Report for {username}", styles['Heading1']))
    elements.append(Spacer(1, 0.5 * inch))

    for topic, acc in performance.items():
        elements.append(Paragraph(f"{topic}: {round(acc*100,2)}%", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return filename
