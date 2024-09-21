from pyrogram import Client, filters
import requests
import random
from BrandrdXMusic import app

# Truth or Dare API URLs
truth_api_url = "https://api.truthordarebot.xyz/v1/truth"
dare_api_url = "https://api.truthordarebot.xyz/v1/dare"


@app.on_message(filters.command("truth"))
def get_truth(client, message):
    try:
        # Make a GET request to the Truth API
        response = requests.get(truth_api_url)
        if response.status_code == 200:
            truth_question = response.json()["question"]
            message.reply_text(f"Truth question:\n\n{truth_question}")
        else:
            message.reply_text("Failed to fetch a truth question. Please try again later.")
    except Exception as e:
        message.reply_text("An error occurred while fetching a truth question. Please try again later.")

@app.on_message(filters.command("dare"))
def get_dare(client, message):
    try:
        # Make a GET request to the Dare API
        response = requests.get(dare_api_url)
        if response.status_code == 200:
            dare_question = response.json()["question"]
            message.reply_text(f"Dare question:\n\n{dare_question}")
        else:
            message.reply_text("Failed to fetch a dare question. Please try again later.")
    except Exception as e:
        message.reply_text("An error occurred while fetching a dare question. Please try again later.")
