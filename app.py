from flask import Flask, render_template, request, jsonify, session
from datetime import datetime

app = Flask(__name__)

app.secret_key = "context-aware-ai-secret-key"


@app.route("/")
def home():

    chat_history = session.get("chat_history", [])

    memory = {
        "name": session.get("user_name", ""),
        "learning_topic": session.get("learning_topic", ""),
        "favorite_subject": session.get("favorite_subject", ""),
        "career_goal": session.get("career_goal", ""),
        "skill": session.get("skill", "")
    }

    return render_template(
        "index.html",
        chat_history=chat_history,
        memory=memory
    )


@app.route("/clear-memory", methods=["POST"])
def clear_memory():

    session.clear()

    return jsonify({
        "result": "All saved context and chat history have been cleared."
    })


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "result": "Please enter a message.",
            "memory": {}
        })

    # Get saved memory

    user_name = session.get("user_name", "")
    learning_topic = session.get("learning_topic", "")
    favorite_subject = session.get("favorite_subject", "")
    career_goal = session.get("career_goal", "")
    skill = session.get("skill", "")

    chat_history = session.get("chat_history", [])

    lower_text = text.lower()


    # =================================
    # SMART MEMORY
    # =================================

    if lower_text.startswith("my name is "):

        user_name = text[11:].strip()

        session["user_name"] = user_name

        result = f"Nice to meet you, {user_name}!"


    elif lower_text.startswith("i'm learning "):

        learning_topic = text[13:].strip()

        session["learning_topic"] = learning_topic

        result = (
            f"Great! I'll remember that you are learning "
            f"{learning_topic}."
        )


    elif lower_text.startswith("i am learning "):

        learning_topic = text[14:].strip()

        session["learning_topic"] = learning_topic

        result = (
            f"Great! I'll remember that you are learning "
            f"{learning_topic}."
        )


    elif lower_text.startswith("i study "):

        learning_topic = text[8:].strip()

        session["learning_topic"] = learning_topic

        result = (
            f"Got it! I'll remember that you study "
            f"{learning_topic}."
        )


    elif lower_text.startswith("my favorite subject is "):

        favorite_subject = text[23:].strip()

        session["favorite_subject"] = favorite_subject

        result = (
            f"Got it! Your favorite subject is "
            f"{favorite_subject}."
        )


    elif lower_text.startswith("i like studying "):

        favorite_subject = text[16:].strip()

        session["favorite_subject"] = favorite_subject

        result = (
            f"Nice! I'll remember that you like studying "
            f"{favorite_subject}."
        )


    elif lower_text.startswith("my career goal is "):

        career_goal = text[18:].strip()

        session["career_goal"] = career_goal

        result = (
            f"Great! I'll remember your career goal: "
            f"{career_goal}."
        )


    elif lower_text.startswith("i want to become "):

        career_goal = text[17:].strip()

        session["career_goal"] = career_goal

        result = (
            f"Great! I'll remember that you want to become "
            f"{career_goal}."
        )


    elif lower_text.startswith("i want to be "):

        career_goal = text[13:].strip()

        session["career_goal"] = career_goal

        result = (
            f"Great! I'll remember your career goal: "
            f"{career_goal}."
        )


    elif lower_text.startswith("my skill is "):

        skill = text[12:].strip()

        session["skill"] = skill

        result = (
            f"Great! I'll remember that you know "
            f"{skill}."
        )


    elif lower_text.startswith("i know "):

        skill = text[7:].strip()

        session["skill"] = skill

        result = (
            f"Nice! I'll remember that you know "
            f"{skill}."
        )


    # =================================
    # MEMORY QUESTIONS
    # =================================

    elif "what is my name" in lower_text:

        if user_name:
            result = f"Your name is {user_name}."
        else:
            result = "I don't know your name yet."


    elif "what am i learning" in lower_text:

        if learning_topic:
            result = f"You are learning {learning_topic}."
        else:
            result = (
                "You haven't told me what you are learning yet."
            )


    elif "what is my favorite subject" in lower_text:

        if favorite_subject:
            result = (
                f"Your favorite subject is "
                f"{favorite_subject}."
            )
        else:
            result = (
                "You haven't told me your favorite subject yet."
            )


    elif "what is my career goal" in lower_text:

        if career_goal:
            result = (
                f"Your career goal is "
                f"{career_goal}."
            )
        else:
            result = (
                "You haven't told me your career goal yet."
            )


    elif (
        "what is my skill" in lower_text
        or "what skill do i have" in lower_text
    ):

        if skill:
            result = f"Your skill is {skill}."
        else:
            result = (
                "You haven't told me your skill yet."
            )


    # =================================
    # ABOUT USER
    # =================================

    elif "tell me about myself" in lower_text:

        details = []

        if user_name:
            details.append(
                f"Your name is {user_name}"
            )

        if learning_topic:
            details.append(
                f"you are learning {learning_topic}"
            )

        if favorite_subject:
            details.append(
                f"your favorite subject is {favorite_subject}"
            )

        if career_goal:
            details.append(
                f"your career goal is {career_goal}"
            )

        if skill:
            details.append(
                f"your skill is {skill}"
            )

        if details:

            result = (
                "I remember that "
                + ", ".join(details)
                + "."
            )

        else:

            result = (
                "I don't have any information about you yet."
            )


    # =================================
    # SMART LEARNING RECOMMENDATION
    # =================================

    elif "what should i learn next" in lower_text:

        if learning_topic and career_goal:

            if "ai" in career_goal.lower() or "machine learning" in career_goal.lower():

                result = (
                    f"Since you are learning {learning_topic} "
                    f"and your career goal is {career_goal}, "
                    "I suggest focusing on Data Structures, "
                    "NumPy, Pandas, Machine Learning, "
                    "Deep Learning and practical AI projects."
                )

            elif "web" in career_goal.lower():

                result = (
                    f"Since you are learning {learning_topic} "
                    f"and your career goal is {career_goal}, "
                    "I suggest focusing on HTML, CSS, JavaScript, "
                    "React, APIs and full-stack projects."
                )

            else:

                result = (
                    f"Since you are learning {learning_topic} "
                    f"and your career goal is {career_goal}, "
                    "I suggest building practical projects, "
                    "learning Data Structures and improving "
                    "your problem-solving skills."
                )


        elif learning_topic:

            if learning_topic.lower() == "python":

                result = (
                    "Since you are learning Python, "
                    "your next steps can be Functions, "
                    "Object-Oriented Programming, "
                    "Data Structures, NumPy, Pandas "
                    "and Machine Learning."
                )

            elif learning_topic.lower() == "java":

                result = (
                    "Since you are learning Java, "
                    "your next steps can be OOP, "
                    "Collections, Exception Handling, "
                    "Data Structures and Java projects."
                )

            else:

                result = (
                    f"Since you are learning {learning_topic}, "
                    "focus on fundamentals, Data Structures, "
                    "problem-solving and practical projects."
                )


        else:

            result = (
                "Tell me what you are currently learning "
                "and I can suggest what to learn next."
            )


    # =================================
    # CONTEXT BASED QUESTIONS
    # =================================

    elif "suggest a project" in lower_text:

        if learning_topic and career_goal:

            result = (
                f"Based on your learning topic "
                f"{learning_topic} and career goal "
                f"{career_goal}, try building a practical "
                "project that combines your current skills "
                "with your career goal."
            )

        elif learning_topic:

            result = (
                f"Since you are learning {learning_topic}, "
                "try building a project using that technology."
            )

        else:

            result = (
                "Tell me what you are learning first, "
                "then I can suggest a project."
            )


    # =================================
    # GREETING
    # =================================

    elif lower_text in ["hello", "hi", "hey"]:

        if user_name:

            result = (
                f"Hello {user_name}! "
                "How can I help you?"
            )

        else:

            result = "Hello! How can I help you?"


    # =================================
    # BASIC KNOWLEDGE
    # =================================

    elif "python" in lower_text:

        result = (
            "Python is a beginner-friendly programming "
            "language used in AI, Machine Learning, "
            "web development and automation."
        )


    elif "machine learning" in lower_text:

        result = (
            "Machine Learning is a part of AI where "
            "computers learn patterns from data and "
            "make predictions."
        )


    else:

        result = (
            f"I understood your message: '{text}'. "
            "Tell me more!"
        )


    # =================================
    # TIMESTAMP
    # =================================

    timestamp = datetime.now().strftime("%I:%M %p")


    # =================================
    # SAVE CHAT
    # =================================

    chat_history.append({
        "user": text,
        "ai": result,
        "time": timestamp
    })

    session["chat_history"] = chat_history[-20:]


    # =================================
    # UPDATED MEMORY
    # =================================

    memory = {
        "name": user_name,
        "learning_topic": learning_topic,
        "favorite_subject": favorite_subject,
        "career_goal": career_goal,
        "skill": skill
    }


    return jsonify({
        "result": result,
        "memory": memory,
        "time": timestamp
    })


if __name__ == "__main__":

    app.run(debug=True)