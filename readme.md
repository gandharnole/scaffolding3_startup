# 📘 Gutenberg Text Cleaner

A Flask-based web application that cleans and analyzes raw text from **Project Gutenberg URLs**.  
It preprocesses the text using custom NLP utilities, computes descriptive statistics, and generates summaries — all via a simple web interface.

---

## 🚀 Features

- 🧹 **Text Cleaning**: Removes Gutenberg headers, special characters, and extra whitespace.  
- 📊 **Statistical Analysis**: Provides character, word, sentence counts, and averages.  
- 🧠 **Text Summarization**: Generates a concise 3-sentence summary.  
- 🌐 **Web Interface**: Accepts a URL input and displays results interactively.  
- ⚙️ **REST API** Endpoints:
  - `POST /api/clean` — Fetch, clean, and analyze text from a Gutenberg URL  
  - `POST /api/analyze` — Analyze text directly from input  

---

## 🧩 Project Structure

├── app.py
├── starter_preprocess.py
├── templates/
│ └── index.html
├── requirements.txt
└── README.md

yaml
Copy code

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/gutenberg-text-cleaner.git
cd gutenberg-text-cleaner
2️⃣ Create and Activate Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate      # (Linux/Mac)
venv\Scripts\activate         # (Windows)
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run the Flask Application
bash
Copy code
python app.py
Then open your browser at 👉 http://localhost:5000

🧠 Example Test URLs
You can test using these Project Gutenberg text URLs:

Book	URL
Pride and Prejudice	https://www.gutenberg.org/files/1342/1342-0.txt
Frankenstein	https://www.gutenberg.org/files/84/84-0.txt
Alice in Wonderland	https://www.gutenberg.org/files/11/11-0.txt
Moby Dick	https://www.gutenberg.org/files/2701/2701-0.txt

🧪 API Examples
/api/clean
Request:

json
Copy code
{
  "url": "https://www.gutenberg.org/files/1342/1342-0.txt"
}
Response:

json
Copy code
{
  "success": true,
  "cleaned_text": "...",
  "statistics": {
    "characters": 702461,
    "words": 127521,
    "sentences": 7356,
    "avg_word_length": 4.5,
    "avg_sentence_length": 17.3
  },
  "summary": "Illustration George Allen Publisher..."
}
🖥️ Web Interface Preview
Input Form
A clean and minimal interface to enter a Project Gutenberg URL and trigger analysis.

Analysis Results
Displays:

✅ Cleaned text (first 500 characters)

✅ Summary (first 3 sentences)

✅ Character, word, and sentence counts

✅ Average word and sentence length


🩺 Health Check Endpoint
You can verify the app is running by visiting:

bash
Copy code
GET http://localhost:5000/health
Response:

json
Copy code
{"status": "healthy", "message": "Text preprocessing service is running"}
📚 Submission Details
Course: Basics of AI – Fall 2025

Assignment: Scaffolding Assignment 3

Due Date: October 27, 2025

Deliverables:

✅ Working Flask App (app.py)

✅ HTML Interface (templates/index.html)

✅ Preprocessor Script (starter_preprocess.py)

✅ requirements.txt

✅ README.md with screenshots and setup steps

🧑‍💻 Author
Gandhar Sidhaye
Department of Electronics Engineering
University at Buffalo

🪪 License
This project is for academic purposes only (Assignment Submission – Basics of AI).

