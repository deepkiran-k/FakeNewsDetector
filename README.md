# 📰 FakeNewsDetector

FakeNewsDetector is your go-to web-based tool to uncover the truth behind news articles. With cutting-edge technology, it evaluates the credibility of news stories, helping you stay informed and free from misinformation. Powered by state-of-the-art Large Language Models (LLMs) and web scraping magic, FakeNewsDetector is here to make fact-checking simple, efficient, and reliable.

---

## 📋 Table of Contents
- [✨ Features](#-features)
- [⚙️ Technologies Used](#️-technologies-used)
- [🚀 Setup and Installation](#-setup-and-installation)
- [🛠️ Usage](#️-usage)
- [📂 Folder Structure](#-folder-structure)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👤 Author](#-author)

---

## ✨ Features
- **🌐 Web Interface**: A sleek and intuitive interface to input URLs or raw text.
- **🔍 Fact-Checking**: Harnesses the Groq API and Google Custom Search Engine to analyze the credibility of news articles.
- **📊 Analytics Dashboard**: View trends, verdict distributions, and statistics on false claims.
- **💾 Database Integration**: Save and retrieve search results with MySQL.
- **🔗 REST API Support**: Access data programmatically with JSON endpoints.

---

## ⚙️ Technologies Used
- **Frontend**: HTML, CSS, JavaScript.
- **Backend**: Python (Flask framework).
- **Database**: MySQL.
- **APIs**:
  - 🌐 Google Custom Search Engine (CSE) API
  - 🤖 Groq API for LLM-based analysis
- **Libraries**:
  - 🥣 BeautifulSoup for web scraping
  - 🔄 Flask-CORS for cross-origin request handling

---

## 🚀 Setup and Installation

### Prerequisites
- 🐍 Python 3.8 or higher
- 🛢️ MySQL Server
- 🔑 API credentials for Google CSE and Groq API

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/deepkiran-k/FakeNewsDetector.git
   cd FakeNewsDetector
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials**:
   - Add your API keys and database details in the `creds.json` file:
     ```json
     {
         "groq_api_key": "your_groq_api_key",
         "google_api_key": "your_google_api_key",
         "google_cse_id": "your_google_cse_id",
         "dbhost": "host_name",
         "dbuser": "username",
         "dbname": "database_name"
     }
     ```

4. **Initialize the database**:
   - Create a MySQL database and run the relevant schema (schema details not included).

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

---

## 🛠️ Usage
### Web Interface
1. Navigate to the home page.
2. Enter a news URL or paste raw text.
3. Receive an in-depth analysis report, including:
   - **Verdict**: True, False, or Inconclusive.
   - **Explanation**: Logical breakdown of the verdict.
   - **Relevant Links**: Trusted sources to verify the claim.

### Dashboard
- Explore trends and statistics on false claims and fact-checked articles.

---

## 📂 Folder Structure
```
FakeNewsDetector/
│
├── app.py               # Main Flask application
├── creds.json           # API credentials (local file)
├── db_connect.py        # Database connection and query logic
├── input.py             # Input processing and web scraping
├── llm_call.py          # LLM-based analysis logic
├── main.py              # Command-line interface for testing
│
├── static/              # Static files (CSS, JavaScript, images)
├── templates/           # HTML templates
│
└── requirements.txt     # Python dependencies
```

---

## 🤝 Contributing
Contributions are welcome! Here's how you can help:
1. **Fork the repository**.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature-name
   ```
3. **Commit your changes** and push to your forked repository.
4. **Open a pull request** to the `main` branch.

---

## 📜 License
This project is currently unlicensed. For usage terms, please contact the author.

---

## 👤 Author
Created with ❤️ by [deepkiran-k](https://github.com/deepkiran-k). If you have any questions or feedback, feel free to reach out!
