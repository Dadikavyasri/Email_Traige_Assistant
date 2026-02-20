from flask import Flask, render_template, request
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk

app = Flask(__name__)

LANGUAGE = "english"
SENTENCES_COUNT = 2


# -----------------------------
# Email Categorization
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
# Email Thread Summarization
# -----------------------------
def summarize_email(text):
    if len(text.split()) < 20:
        return text  # If email is short, no need to summarize

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    summary = summarizer(parser.document, SENTENCES_COUNT)
    return " ".join(str(sentence) for sentence in summary)


# -----------------------------
# Smart Auto Reply Generator
# -----------------------------
def generate_reply(category, sentiment):
    if category == "Work":
        return "Thank you for the update. I will review the details and respond shortly."
    elif category == "Spam":
        return "This appears to be promotional content. No response required."
    elif category == "Personal":
        return "Thank you for sharing! I appreciate the update."
    elif sentiment.startswith("Negative"):
        return "I understand the concern raised. I will address this matter as soon as possible."
    else:
        return "Thank you for your email. I will get back to you soon."


@app.route("/", methods=["GET", "POST"])
def home():
    category = None
    sentiment = None
    priority = None
    reply = None
    summary = None

    if request.method == "POST":
        email_text = request.form["email"]

        category = categorize_email(email_text)
        sentiment = get_sentiment(email_text)
        priority = get_priority(category, sentiment)
        summary = summarize_email(email_text)
        reply = generate_reply(category, sentiment)

    return render_template(
        "index.html",
        category=category,
        sentiment=sentiment,
        priority=priority,
        reply=reply,
        summary=summary
    )


if __name__ == "__main__":
    nltk.download("punkt")
    app.run(debug=True)