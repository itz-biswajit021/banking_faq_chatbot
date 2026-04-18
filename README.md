# 🏦 Hybrid Banking FAQ Chatbot using NLP & Machine Learning

An intelligent banking chatbot that combines **Machine Learning-based
Intent Classification** and **FAQ Similarity Matching** to provide
accurate, fast, and reliable responses to user queries.

------------------------------------------------------------------------

## 🚀 Project Overview

Modern banking platforms often overwhelm users with large FAQ sections
and static help pages. This project solves that problem by building a
**hybrid conversational chatbot** that:

-   Understands natural language queries
-   Retrieves relevant answers instantly
-   Reduces dependency on manual search or customer support

------------------------------------------------------------------------

## 💡 Key Features

-   🤖 **Hybrid NLP Model**
    -   Intent Classification (ML Model)
    -   FAQ Similarity Matching (TF-IDF + Cosine Similarity)
-   🎯 **Smart Decision Engine**
    -   Chooses best response using confidence & similarity thresholds
-   💬 **Modern Chat Interface**
    -   Animated chat UI
    -   Typing indicators
-   🔊 **Voice Features**
    -   Speech-to-text input
    -   Text-to-speech responses
-   ⚡ **Auto-Reply Suggestions**
    -   Smart suggestion chips for quick follow-ups
-   🛡️ **Fallback Mechanism**
    -   Prevents incorrect or misleading responses

------------------------------------------------------------------------

## 🧠 System Architecture

User Input\
↓\
Frontend (HTML, CSS, JS)\
↓\
Flask Backend API\
↓\
NLP Processing Layer\
├── TF-IDF Vectorization\
├── Intent Classification Model\
└── FAQ Similarity Engine\
↓\
Hybrid Decision Engine\
↓\
Response Generator\
↓\
Frontend Display + Suggestions

------------------------------------------------------------------------

## 🛠️ Tech Stack

### Backend

-   Python
-   Flask
-   TensorFlow / Keras
-   Scikit-learn
-   Pandas, NumPy

### Frontend

-   HTML5
-   CSS3
-   JavaScript (ES6)
-   Web Speech API (Voice features)

------------------------------------------------------------------------

## 📂 Project Structure

ai_banking_bot/\
│\
├── backend/\
│ ├── app.py\
│ ├── model/\
│ │ ├── chatbot_model.h5\
│ │ ├── tokenizer.pkl\
│ │ ├── label_encoder.pkl\
│ │\
│ ├── data/\
│ │ ├── bank_faq_intents.json\
│ │ ├── BankFAQs.csv\
│\
├── frontend/\
│ ├── welcome.html\
│ ├── index.html\
│ ├── style.css\
│ ├── script.js\
│\
└── README.md

------------------------------------------------------------------------

## ⚙️ How It Works

1.  User enters a query\
2.  Query is converted into TF-IDF vector\
3.  System performs:
    -   Intent Prediction (ML Model)\
    -   FAQ Similarity Matching\
4.  Hybrid Decision Logic selects best response:
    -   High similarity → FAQ answer\
    -   High confidence → Intent response\
    -   Low confidence → Safe fallback\
5.  Response is displayed with suggestions

------------------------------------------------------------------------

## 📊 Algorithms Used

-   TF-IDF Vectorization\
-   Cosine Similarity\
-   Neural Network (Intent Classification)\
-   Threshold-based Decision Logic

------------------------------------------------------------------------

## 📌 Functional Features

-   Text-based query input\
-   Voice input support\
-   Real-time response generation\
-   Suggestion-based navigation\
-   Chat history clear option

------------------------------------------------------------------------

## ⚡ Performance

-   Response time: \< 1.5 seconds\
-   Accuracy: \~80%+ (for known intents)\
-   Lightweight & fast execution

------------------------------------------------------------------------

## ❗ Limitations

-   No real-time banking transactions\
-   No authentication system\
-   Dataset-dependent responses\
-   Limited contextual understanding\
-   No multilingual support

------------------------------------------------------------------------

## 🔮 Future Scope

-   Integration with BERT / LLM models\
-   Real banking API integration\
-   Multilingual chatbot support\
-   Personalized user experience\
-   Mobile app deployment

------------------------------------------------------------------------

## 🎓 Use Cases

-   Banking customer support\
-   FAQ automation systems\
-   Educational NLP projects\
-   Conversational AI prototypes

------------------------------------------------------------------------

## 🙌 Author

**Biswajit Mahapatra**\
B.Tech CSE (AI & ML)

------------------------------------------------------------------------

## ⭐ If you like this project

Give it a ⭐ on GitHub and share your feedback!
