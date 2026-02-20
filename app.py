from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

# -----------------------------
# Email Categorization Function
# -----------------------------
def categorize_email(text):
    text = text.lower()

    if any(word in text for word in ["meeting", "project", "deadline", "client"]):
        return "Work"
    elif any(word in text for word in ["offer", "winner", "lottery", "free", "money"]):
        return "Spam"
    elif any(word in text for word in ["family", "party", "birthday", "friends"]):
        return "Personal"
    else:
        return "Important"


# -----------------------------
# Sentiment Analysis
# -----------------------------
def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative ⚠"
    else:
        return "Neutral 😐"


# -----------------------------
# Priority Calculation
# -----------------------------
def get_priority(category, sentiment):
    if category == "Spam":
        return "Low 🟢"
    elif sentiment.startswith("Negative"):
        return "High 🔴"
    elif category == "Work":
        return "High 🔴"
    else:
        return "Medium 🟡"


# -----------------------------
# Auto Reply Generator
# -----------------------------
def generate_reply(category):
    replies = {
        "Work": "Thank you for your email. I will review the details and get back to you shortly.",
        "Spam": "This message appears to be promotional or spam. No action will be taken.",
        "Personal": "Thank you! Looking forward to it 😊",
        "Important": "Thank you for reaching out. I will respond soon."
    }
    return replies.get(category)


@app.route("/", methods=["GET", "POST"])
def home():
    category = None
    sentiment = None
    priority = None
    reply = None

    if request.method == "POST":
        email_text = request.form["email"]
        category = categorize_email(email_text)
        sentiment = get_sentiment(email_text)
        priority = get_priority(category, sentiment)
        reply = generate_reply(category)

    return render_template(
        "index.html",
        category=category,
        sentiment=sentiment,
        priority=priority,
        reply=reply
    )


if __name__ == "__main__":
    app.run(debug=True)