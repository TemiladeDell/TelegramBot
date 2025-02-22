from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, ApplicationBuilder, PollAnswerHandler
import json
import os
import datetime
import requests
from transformers import pipeline

pipe = pipeline("text-classification", model="dhruvpal/fake-news-bert")

options = ["Politics", "Sports", "Technology", "Science", 
           "Health", "Business", "Entertainment", "World News",
           "Education", "Environment"]
file_path = "user_telegram_data.json"

telegram_api = "7826508264:AAFZCabtF19UQoOfK1YaU3xLmT2v9AQcSTk"
news_api_key = "1b755480df7948fa96ba7f7989e32ab7"
newsapi_url = "https://newsapi.org/v2/top-headlines"

async def gettingNews(update: Update, context: CallbackContext):
    user_chat_id = str(update.message.chat_id)
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as user_data_file:
                user_loaded_data = json.load(user_data_file)
            
            if user_chat_id in user_loaded_data:
                category_list = user_loaded_data[user_chat_id].get("news_preference", [])
                if not category_list:
                    await update.message.reply_text("You have not selected any news categories yet.")
                    return

                for category in category_list:
                    params = {
                        "category": category,
                        "apiKey": news_api_key
                    }
                    
                    response = requests.get(url=newsapi_url, params=params)
                    data = response.json()
                    
                    if data.get("status") == "ok":
                        articles = data.get("articles", [])
                        if articles:
                            await update.message.reply_text(f"Top 5 news in {category}:")
                            for article in articles[:5]:
                                await update.message.reply_text(f"{article['title']}\n{article['url']}")
                                result = pipe(article['title'])
                                label = result[0]['label']
                                score = result[0]['score']
                                
                                if label == "LABEL_0":
                                    label_text = "real"
                                elif label == "LABEL_1":
                                    label_text = "fake"
                                else:
                                    label_text = "unknown"
                                    
                                await update.message.reply_text(f"Fake news detection: {label_text} (confidence: {score:.2f})")
                        else:
                            await update.message.reply_text(f"No news found for {category}.")
                    else:
                        await update.message.reply_text(f"Failed to fetch news for {category}.")
            else:
                await update.message.reply_text("You are not subscribed. Use /start to subscribe.")
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("An error occurred while fetching news.")

def gettingCurrentDate():
    return datetime.datetime.now().strftime("%Y-%m-%d")

async def handle_poll_answer(update: Update, context: CallbackContext):
    user_id = str(update.poll_answer.user.id)
    selected_option_ids = update.poll_answer.option_ids

    try:
        with open(file_path, "r") as file:
            user_data = json.load(file)

        if user_id not in user_data:
            user_data[user_id] = {"subscribed": True, "news_preference": []}

        user_preference = user_data[user_id]["news_preference"]

        for option_id in selected_option_ids:
            selected_category = options[option_id]
            if selected_category not in user_preference:
                user_preference.append(selected_category)

        with open(file_path, "w") as file:
            json.dump(user_data, file, indent=4)

        await context.bot.send_message(
            chat_id=user_id,
            text="Your news preferences have been updated. Fetching news tailored to you..."
        )

        # Trigger the /news command directly
        await context.bot.send_message(chat_id=user_id, text="/news")

    except Exception as e:
        print("Error:", e)
        await context.bot.send_message(
            chat_id=user_id,
            text="An error occurred while updating your preferences."
        )

async def greetUser(update: Update, context: CallbackContext):
    user_first_name = update.message.from_user.first_name
    user_chat_id = str(update.message.chat_id)
    await update.message.reply_text(f"Welcome {user_first_name} to Discern Bot! This bot helps discern between fake and real news.")

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as user_data_file:
                user_loaded_data = json.load(user_data_file)
        else:
            user_loaded_data = {}

        if user_chat_id in user_loaded_data:
            await update.message.reply_text("You are already subscribed.")
        else:
            user_loaded_data[user_chat_id] = {
                "subscribed": True,
                "joined_at": gettingCurrentDate(),
                "news_preference": []
            }
            with open(file_path, "w") as user_data_file:
                json.dump(user_loaded_data, user_data_file, indent=4)

            await context.bot.send_poll(
                chat_id=user_chat_id,
                question="What type of news do you prefer?",
                options=options,
                is_anonymous=False,
                allows_multiple_answers=True
            )
    except Exception as e:
        print("Error:", e)

async def clearData(update: Update, context: CallbackContext):
    try:
        if os.path.exists(file_path):
            with open(file_path, "w") as file:
                json.dump({}, file)
            await update.message.reply_text("All user data has been cleared.")
        else:
            await update.message.reply_text("No data file found to clear.")
    except Exception as e:
        print("Error:", e)
        await update.message.reply_text("An error occurred while clearing the data.")

def main():
    app = ApplicationBuilder().token(telegram_api).build()

    app.add_handler(CommandHandler("start", greetUser))
    app.add_handler(CommandHandler("news", gettingNews))
    app.add_handler(CommandHandler("cleardata", clearData))
    app.add_handler(PollAnswerHandler(handle_poll_answer))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()