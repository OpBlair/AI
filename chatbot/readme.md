# 🤖 Rule-Based CLI Chatbot (Friday v1.0)

A personalized, command-line interface (CLI) chatbot built with Python. This version uses an **advanced rule-based system** that leverages **Natural Language Processing (NLP)** techniques like **Lemmatization** for smart pattern matching and includes contextual features like time-aware greetings.

---

### ✨ Features

* **Contextual Greetings:** Greets the user based on the time of day (Good morning/afternoon/evening) using Python's `datetime`.
* **Personalization:** The bot has a defined name (`Friday`) and handles identity questions.
* **Smart Matching (Lemmatization):** Uses NLTK to reduce words to their base form (lemma), enabling a single pattern (e.g., "thank") to match many variations (e.g., "thanking," "thanked").
* **Time Retrieval:** Provides the current local time upon request.
* **Stable Fallback:** Provides helpful responses for unrecognized input, ensuring the bot never crashes.

---

### 🚀 Getting Started

Follow these steps to set up and run the chatbot on your local machine.

#### 1. Prerequisites

You must have **Python 3.x** installed. Using a virtual environment is highly recommended.

```bash
# Create and activate a virtual environment
python3 -m venv myenv
source myenv/bin/activate
```
Here is the full content:

#### 2\. Installation

Install the required Python packages (listed in your `requirements.txt` file):

```bash
pip install -r requirements.txt
```

#### 3\. NLTK Data Download (Crucial Step)

The bot relies on NLTK for text processing. You need to download the necessary data models **once** by running these commands in your Python interpreter:

```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('wordnet')
>>> exit()
```

#### 4\. File Structure

Ensure your project directory contains these core files:

```
.
├── chatbot.py (or try1.py)  # The main Python logic (Brain)
└── intents.json             # The knowledge base (Rules/Data)
```

-----

### 💬 Usage

Run the main Python script from your terminal:

```bash
python3 chatbot.py
```

The bot will start, and you can begin chatting:

| Input Example | Expected Output |
| :--- | :--- |
| `hello` | `Good morning/afternoon/evening!` (Contextual) |
| `what is your name` | `I am Friday, a simple rule-based chatbot.` |
| `i am thankful to you` | `No problem!` (Matches due to Lemmatization) |
| `what is the time` | `The current time is HH:MM PM.` |
| `exit` | `Chatbot: Goodbye!` |

-----

### ⚙️ Customization

  * **Change the Name:** Modify the global `BOT_NAME` variable near the top of the `chatbot.py` script.
  * **Add New Topics/Rules:** To teach the bot new things, add new JSON objects (Intents) to the `intents.json` file. Remember to use **base words** (lemmas) for your patterns for the best results.

-----

### 🧑‍💻 Future Development

This project provides a strong base for further development, including:

  * **ML Upgrade:** Replacing keyword matching with a **TF-IDF Vectorizer and Classification Model** to allow the bot to understand generalized sentences it hasn't seen before.
  * **Integration:** Connecting the bot to external APIs (e.g., weather or news).

-----

### 📄 License

This project is open-source and available under the [License Name, e.g., MIT License].
