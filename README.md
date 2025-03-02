# Price Monitoring Web Scraper with Telegram Bot

This is a simple scraper that monitors product prices on a website (in this case, BackMarket) and sends Telegram notifications when the price of a product drops below a defined threshold.

## Requirements

Ensure you have the following tools installed:
- Python 3.x
- pip (Python package installer)

## Installation

1. **Clone the repository**:

   If you haven't already, clone the repository to your computer:

   ```bash
   git clone <REPOSITORY_URL>
   cd <REPOSITORY_NAME>
   
2. **Create a virtual environment (optional but recommended)**:
 
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Linux/macOS
   venv\Scripts\activate      # on Windows
   
3. **Install the required packages**:

 - Once you're in your virtual environment (if created), install the necessary packages using pip:

   ```bash
   pip install -r requirements.txt

4. Create a .env file:

- In the same directory as your project, create a file named .env and add the following environment variables:

  ```bash
  TELEGRAM_BOT_TOKEN=your_telegram_bot_token
  CHAT_ID_FILE=chat_ids.txt
- TELEGRAM_BOT_TOKEN: Insert your Telegram bot token which you get from BotFather.
- CHAT_ID_FILE: This is the file where the chat IDs of registered users will be stored. It can be a simple text file named chat_ids.txt.

5. Create the chat ID storage file:

- Create an empty file named chat_ids.txt (or the name you chose in the .env file) in the same directory as the project. This file will hold the chat IDs of users who register to receive notifications.

  ```bash
  touch chat_ids.txt
  
6. Usage
- Start the Telegram bot:
  Run the following command to start the Telegram bot:

  ```bash
  python <python_file_name>.py
- Register Users:
  To register and start receiving notifications about price changes, send the /start command to the bot on Telegram. Once registered, you will receive notifications when the price of a monitored product drops below the target price.

## Launch Price Monitoring:
After registration, send the /launch command to start monitoring the prices. The bot will periodically check the prices of products defined in the file and send notifications on Telegram if the price of a product drops below the target price.

## Automatic Monitoring:
The script will automatically monitor the products listed in the PRODUCTS_TO_MONITOR dictionary and send a notification for each product that meets the price criterion (if the price drops below the target value).

## How It Works
- Web Scraping: Uses Selenium to perform web scraping to fetch the product prices from the BackMarket website.
- Telegram Bot: Uses the python-telegram-bot library to send Telegram notifications when a product's price drops below the target price.
- User Registration: Users register using the /start command and receive notifications when the prices of monitored products change.
## Code Structure
- main.py: Contains the main logic of the bot and price monitoring.
- .env: Configuration file for environment variables (such as the Telegram bot token).
- chat_ids.txt: Text file that stores the chat IDs of registered users.
## Required Packages
- To run this project, make sure you have the following Python packages installed:

1 selenium: For web scraping.
2 webdriver-manager: For managing Chrome drivers.
3 selenium-stealth: To prevent detection of automated traffic.
4 requests: For sending Telegram messages.
5 python-telegram-bot: For interacting with the Telegram API.
6 python-dotenv: For managing environment variables in the .env file.
7 undetected-chromedriver: To run Chrome in undetectable mode.

7. Install all dependencies with:

    ```bash
    pip install -r requirements.txt
    Contributing
= If you want to contribute to this project, please open a pull request with your changes.

8. License
This project is licensed under the MIT License. See the LICENSE file for details.
