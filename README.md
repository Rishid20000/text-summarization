📝 Smart Text Summarizer

🌐 Live Demo → [Smart Text Summarizer on Render](https://text-summarization-dgfr.onrender.com/)

Smart Text Summarizer is a Flask-based web application that transforms long text into concise, meaningful summaries using AI-powered Hugging Face models. The app provides a clean, responsive UI and supports customizable summary lengths, making it ideal for students, researchers, writers, and anyone who needs quick summaries from large text blocks.

🚀 Features

⚡ Quick Summarization – Get results instantly.

🤖 AI-Powered – Uses Hugging Face’s distilbart-cnn-12-6 transformer model for high-quality summaries.

🎛 Customizable Length – Adjust how detailed or concise the summary should be.

🌙 Responsive UI – Built with HTML/CSS, styled for modern look.

🖥 Deploy-Ready – Easily deployed on Render with Gunicorn & environment variables.

🛠️ Tech Stack
Backend

Python → Core programming language.

Flask → Lightweight web framework for handling routes and rendering templates.

Requests → Makes HTTP requests to Hugging Face inference API.

Tenacity → Retry logic for handling model load delays and transient failures.

Gunicorn → WSGI HTTP server used for production deployment on Render.

AI/ML

Hugging Face Transformers → Model inference via Hugging Face API.

Model: sshleifer/distilbart-cnn-12-6

A distilled version of bart-large-cnn, optimized for summarization.

Faster and lighter (good for free-tier hosting).

Frontend

HTML + Jinja2 → Templates for rendering dynamic content.

CSS (custom) → Styling for dark mode & modern UI.

Hosting

Render → Free-tier cloud hosting for web apps.

Hugging Face API token is securely stored as an environment variable (HF_API_TOKEN).

📂 Project Structure
text-summarizer/
│── app.py              # Flask backend
│── requirements.txt    # Python dependencies
│── Procfile            # Render deployment instruction
│── runtime.txt         # Python version specification
│── templates/
│    └── index.html     # Frontend HTML template
│── static/
     └── style.css      # Custom CSS styles

⚙️ Installation (Local Setup)

Clone the repository

git clone https://github.com/your-username/text-summarizer.git
cd text-summarizer


Create virtual environment

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows


Install dependencies

pip install -r requirements.txt


Set Hugging Face token
Create .env file:

HF_API_TOKEN=your_huggingface_token


Run the app

python app.py


Visit: http://127.0.0.1:5000

🌐 Deployment on Render

Push project to GitHub.

On Render dashboard:

New → Web Service

Connect GitHub repo.

Build Command → pip install -r requirements.txt

Start Command → gunicorn app:app

Add Environment Variable:

HF_API_TOKEN=your_huggingface_token


Deploy 🎉 → Your app will be live at:

https://your-app-name.onrender.com/

📖 Why These Technologies?

Flask → Lightweight and simple for API-driven web apps.

Gunicorn → Production-ready server (better than Flask’s dev server).

Hugging Face API → Provides state-of-the-art NLP models without needing heavy GPU hosting.

DistilBART → Fast, efficient summarization model suitable for free-tier hosting.

Render → Free, reliable, and beginner-friendly alternative to Heroku/PythonAnywhere.

🧑‍💻 Contributing

Fork the repo

Create a new branch (feature-xyz)

Commit changes

Push to branch

Open a Pull Request

