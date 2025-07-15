# 🧠 Reddit User Persona Extractor

## 🚩 Problem Statement

Understanding user behavior and interests from online interactions can provide deep insights for research, marketing, and digital profiling. Reddit, being one of the most content-rich discussion platforms, holds immense potential for user behavior analysis. However, manually creating personas from user posts/comments is time-consuming, subjective, and lacks scalability.

## 📜 Description

The **Reddit User Persona Extractor** is a Python-based tool that automatically generates a structured, professional user persona by analyzing the posts and comments of any public Reddit user. It uses the Reddit API (PRAW) to collect real user data and a free Large Language Model (LLM) via OpenRouter to synthesize the data into meaningful insights. This project avoids fictional generation and bases every attribute of the persona strictly on actual Reddit content, with citations.

## 🔧 Working

### 1. Input
- Accepts a Reddit profile URL as input (e.g., https://www.reddit.com/user/kojied/).

### 2. Username Extraction
- The tool extracts the username from the given profile URL.

### 3. Data Collection (Reddit API)
- Uses Reddit API (via PRAW) and credentials stored in the `.env` file to authenticate.
- Fetches up to 50 latest submissions (posts) and 100 latest comments of the user.

### 4. Data Formatting
- Each post and comment is formatted into a structured block.
- Example format:


### 5. Persona Generation (LLM via OpenRouter)
- The formatted data is passed as prompt content to a free model (e.g., `mistralai/mistral-7b-instruct`) through the OpenRouter API.
- The prompt instructs the LLM to generate:
- Reddit Username
- Age Range (if inferable)
- Occupation (if mentioned)
- Interests
- Tech-savviness
- Political Leaning (if evident)
- Communication Style
- Motivations, Goals, Frustrations, and Personality Traits
- Citations from posts or comments to justify each insight

### 6. Output
- The generated persona is saved in the `output/` folder as a `.txt` file:


## 🧪 Result

Sample output based on real data:

- User Persona for u/BhupeshV:
- Username: u/BhupeshV
- Age Range: 25–35 (Comment #3)
- Occupation: Software Developer (Post #2)
- Interests: AI, Web Development, Chatbots (Post #1, Comment #5)
- Communication Style: Direct and technical (Comment #2)
- Tech-savviness: High – active in tech subreddits and uses APIs (Post #3, Comment #4)
- Motivations: Learning new tools, contributing to open-source (Comment #1)
- Frustrations: Poor documentation and lack of response from APIs (Comment #7)


## ✅ Features

- ✅ Fetches real Reddit content (no fabrication)
- ✅ Automatically generates a detailed, structured user persona
- ✅ Supports OpenRouter free models like Mistral 7B
- ✅ Uses environment variables for secure credentials
- ✅ Clean text output with citation-based persona attributes

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/reddit-user-persona-extractor.git
cd reddit-user-persona-extractor
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create a .env file with:

```bash
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Run the script

```bash
python main.py
```

## 📌 Conclusion

This tool is designed to transform Reddit profile data into structured user personas for research, product development, UX design, and digital marketing. It emphasizes accuracy and reliability by using real user-generated content from Reddit, rather than fictional samples. The use of OpenRouter allows integration with powerful open-source LLMs at no cost, making it ideal for students, researchers, and developers.

## 🧾 License
This project is licensed under the MIT License. You are free to modify, distribute, or enhance the code for personal or commercial purposes.

## Feedback / Contributions

Have suggestions or improvements? Open an issue or submit a pull request. Let's build better tools together !
