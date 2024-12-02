from docx import Document

from loader import db


# 2. Word fayldan ma'lumotlarni o'qish va qayta ishlash funksiyasi
def extract_and_save_from_word(file_path: str, question_id: int):
    doc = Document(file_path)
    
    question = None
    answers = []
    correct_answer = None

    for para in doc.paragraphs:
        text = para.text.strip()

        # Savolni aniqlash
        if text.startswith("#"):
            # Oldingi savolni bazaga saqlash
            if question and answers and correct_answer:
                db.save_to_database(question_id, question, answers, correct_answer)

            # Yangi savolni boshlash
            question = text[1:].strip()
            answers = []
            correct_answer = None

        # Javoblarni aniqlash
        elif text.startswith(("+", "A", "B", "C", "D")):
            if text.startswith("+"):
                correct_answer = text[1:].strip()
                answers.append(correct_answer)
            else:
                answers.append(text.strip())

    if question and answers and correct_answer:
        db.save_to_database(question_id, question, answers, correct_answer)