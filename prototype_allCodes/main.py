from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
import random
import csv
import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

GROQ_API_KEY = "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"
BOT_TOKEN = "7697386023:AAFCqReAinQB_rXG0ckVgu_8DPWbHhhXG-k"

ANSWER_QUESTION = 0

ALL_GRAMMAR_QUESTIONS = []
ALL_READING_QUESTIONS = []

CURRENT_QUESTIONS = []
CURRENT_INDEX = 0
INCORRECT_ANSWERS = []


with open("grammar_questions.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ALL_GRAMMAR_QUESTIONS.append({
            "type": "grammar",
            "text": row["Question"],
            "choices": [row["Option A"], row["Option B"], row["Option C"], row["Option D"]],
            "answer": row["Correct Answer"]
        })


with open("topik_reading_questions.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        ALL_READING_QUESTIONS.append({
            "type": "reading",
            "text": row["Text"],
            "choices": [row["Option A"], row["Option B"], row["Option C"], row["Option D"]],
            "answer": row["CorrectAnswer"]
        })

def get_grammar_explanation(question, user_answer, correct_answer):
    prompt = f"""
You're a Korean language teacher helping a student understand their grammar mistake.

Question: {question}
Student's Answer: {user_answer}
Correct Answer: {correct_answer}

Please briefly explain why the correct answer is correct and what grammar rule it follows. Keep it short and clear.
"""

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
        )
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Groq API error:", e)
        return "⚠️ Unable to fetch explanation. Please try again later."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_INDEX, CURRENT_QUESTIONS, INCORRECT_ANSWERS

    CURRENT_INDEX = 0
    INCORRECT_ANSWERS = []

    selected_grammar = random.sample(ALL_GRAMMAR_QUESTIONS, 5)
    selected_reading = random.sample(ALL_READING_QUESTIONS, 5)
    CURRENT_QUESTIONS = selected_grammar + selected_reading

    await update.message.reply_text("🦔Welcome to Hogi!\nLet's get started with the first 5 questions, which are based on TOPIK II Question Types 1 and 2 — fill-in-the-blank grammar questions.\nAfter that, you'll tackle the next 5 questions, modeled after TOPIK II Question Types 11 and 12 — reading, comprehension, and analysis.")
    await send_question(update)
    return ANSWER_QUESTION

async def send_question(update: Update):
    global CURRENT_INDEX, CURRENT_QUESTIONS

    if CURRENT_INDEX < len(CURRENT_QUESTIONS):
        q = CURRENT_QUESTIONS[CURRENT_INDEX]
        question_text = q["text"]
        choices = q["choices"].copy()
        random.shuffle(choices)

        q["shuffled_choices"] = choices  
        formatted_choices = "\n".join([f"{i+1}. {choice}" for i, choice in enumerate(choices)])

        keyboard = ReplyKeyboardMarkup(
            [["1", "2"], ["3", "4"]],
            one_time_keyboard=True,
            resize_keyboard=True
        )

        if q["type"] == "grammar":
            await update.message.reply_text(
                f"🔤 Question 1-2 Type {CURRENT_INDEX+1}/10:\n\n{question_text}\n\n{formatted_choices}",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                f"📘 Question 11-12 Type{CURRENT_INDEX+1}/10:\n\n{question_text}\n\n{formatted_choices}",
                reply_markup=keyboard
            )
    else:
        await update.message.reply_text("📚 Review time for incorrect answers!" if INCORRECT_ANSWERS else "🎉 Perfect score! Well done!", reply_markup=ReplyKeyboardRemove())
        if INCORRECT_ANSWERS:
            await review_incorrect(update)

async def answer_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CURRENT_INDEX, CURRENT_QUESTIONS, INCORRECT_ANSWERS

    user_input = update.message.text.strip()
    q = CURRENT_QUESTIONS[CURRENT_INDEX]

    try:
        index = int(user_input) - 1
        if index < 0 or index > 3:
            raise ValueError()

        selected = q["shuffled_choices"][index]
        correct = q["answer"]

        is_correct = False
        if q["type"] == "grammar":
            is_correct = selected == correct
        elif q["type"] == "reading":
            correct_index = int(correct) - 1
            correct_choice = q["choices"][correct_index]
            is_correct = selected == correct_choice

        if is_correct:
            await update.message.reply_text("✅ Correct!")
        else:
            await update.message.reply_text(f"❌ Incorrect. Correct answer: {correct if q['type']=='grammar' else correct_choice}")

            if q["type"] == "grammar":
                explanation = get_grammar_explanation(q["text"], selected, correct)
                await update.message.reply_text(f"📘 Explanation:\n{explanation}")

            INCORRECT_ANSWERS.append(q)

        CURRENT_INDEX += 1
        await send_question(update)

    except (ValueError, IndexError):
        await update.message.reply_text("⚠️ Please tap one of the buttons (1 to 4).")


async def review_incorrect(update: Update):
    for q in INCORRECT_ANSWERS:
        question_text = q["text"]
        formatted_choices = "\n".join([f"{i+1}. {c}" for i, c in enumerate(q["choices"])])
        await update.message.reply_text(f"{question_text}\n\n{formatted_choices}")
    await update.message.reply_text("✅ Review complete! Thanks for studying with Hogi 🦔")

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ANSWER_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer_question)]
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
