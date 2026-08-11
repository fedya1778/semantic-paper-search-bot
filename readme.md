# Semantic Paper Search Bot

A Telegram bot that searches scientific papers by **meaning** using BERT embeddings, not just keywords.

## Features

- **Semantic Search**: Uses BERT to understand query meaning, not just keywords
- **Multilingual**: Supports Russian and English
- **Fast**: ~100ms per search query
- **10k+ Papers**: Indexed scientific papers from arXiv
- **Telegram Integration**: Easy-to-use Telegram bot interface

## Tech Stack

- **Backend**: Python, Telegram Bot API
- **NLP**: BERT (sentence-transformers), cosine similarity
- **Data**: 10k scientific papers from HuggingFace Datasets
- **Vectors**: 384-dimensional normalized embeddings

## Installation

1. Clone repository
```bash
git clone https://github.com/yourusername/semantic-paper-search-bot.git
cd semantic-paper-search-bot
```

2. Create virtual environment
```bash
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create .env file
```bash
TELEGRAM_TOKEN=your_token_here
```

Get token from @BotFather in Telegram

5. Download dataset (first time only)
```bash
python download_dataset.py
```

6. Run bot
```bash
python bot.py
```

## Usage

In Telegram, send messages to your bot:

- `/start` - Start the bot
- `/help` - Get help
- `/search <query>` - Search for papers
- Just type text - it will search automatically
