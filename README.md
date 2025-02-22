Discern Bot - Fake News Detection Bot
Discern Bot is a Telegram bot designed to help users discern between fake and real news. It fetches news articles based on user preferences and uses a machine learning model to classify the news as "real" or "fake." The bot also provides a confidence score for each prediction.

Features
1.News Categories: Users can select their preferred news categories (e.g., Politics, Sports, Technology).

2.Fake News Detection: The bot uses the dhruvpal/fake-news-bert model to classify news titles as "real" or "fake."

3.Tailored News: Fetches top news articles based on the user's selected categories.

4.Poll-Based Preferences: Users can select their preferred news categories through an interactive poll.

5.User Data Management: Saves user preferences and subscription status in a JSON file.

6.Clear Data Command: Allows users to clear their saved preferences.

Prerequisites
1.Before running the bot, ensure you have the following:

2.Python 3.8 or higher: Install Python from python.org.

3.Telegram Bot Token: Obtain a bot token from BotFather.

4.NewsAPI Key: Sign up for a free API key at NewsAPI.

5.Transformers Library: Install the transformers library for fake news detection.


Clone the repository:
git clone https://github.com/temiladedell/discern-bot.git
cd discern-bot

Install the required Python packages:
1.pip install python-telegram-bot
2.pip install transformers
3.pip install request



Add your Telegram bot token and NewsAPI key:

1.TELEGRAM_API=your_telegram_bot_token
2.NEWS_API_KEY=your_newsapi_key

Usage Commands
1./start: Start the bot and subscribe to news updates. The bot will send a poll to select preferred news categories.

2./news: Fetch the latest news articles based on your selected categories.

3./cleardata: Clear your saved preferences and subscription data.



How It Works
1.User Preferences: The bot saves user preferences (selected news categories) in a JSON file (user_telegram_data.json).

2.News Fetching: It uses the NewsAPI to fetch top headlines based on the user's selected categories.

3.Fake News Detection: The bot uses the dhruvpal/fake-news-bert model to classify news titles as "real" or "fake" and provides a confidence score.

4.Poll Integration: Users can update their preferences by interacting with the poll sent by the bot.


Acknowledgments:
1.NewsAPI for providing news data

2.Hugging Face Transformers for the fake news detection model.

3.python-telegram-bot for the Telegram bot framework.
