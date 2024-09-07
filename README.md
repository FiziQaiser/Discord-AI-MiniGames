# Discord-AI-MiniGames

![Bot Status](https://img.shields.io/badge/status-online-brightgreen)
![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![Discord.py](https://img.shields.io/badge/discord.py-Enabled-green)

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)

## Introduction

**Discord-AI-MiniGames** is a Discord bot that brings classic games with a twist of advanced AI. This repository features a Tic-Tac-Toe game where players can challenge a computer opponent that uses the Alpha-Beta Pruning Minimax algorithm for optimal gameplay. Built with `discord.py`, this bot showcases intelligent gameplay and strategic depth, making classic games more exciting and interactive.

## Features

- **Alpha-Beta Pruning Minimax Algorithm:** Optimizes decision-making in Tic-Tac-Toe for challenging gameplay.
- **Discord Integration:** Seamlessly integrates with Discord using `discord.py`.
- **Game Expansion:** Framework designed for easy addition of new games with similar AI techniques.

## Setup

### Prerequisites

- Python 3.11+
- pip (Python package installer)
- Create a Discord Bot and get its token (you can get this from the [Discord Developer Portal](https://discord.com/developers/applications))

### Creating a Discord Bot

To use this bot in your Discord server, you'll first need to create a Discord bot through the Discord Developer Portal. Follow these steps to get started:

#### Step 1: Create a New Application

1. **Go to the [Discord Developer Portal](https://discord.com/developers/applications)**.
2. Click on the "New Application" button.
3. Enter a name for your application (e.g., "AI MiniGames Bot") and click "Create".

#### Step 2: Configure Bot Permissions
1. Select the "Bot" tab from the menu.
2. In the left-hand menu, select **OAuth2**.
3. Under **Scopes**, select `bot` and `applications.commands`.
4. Under **Bot Permissions**, select:
   - `Send Messages`
   - `Read Message History`
   - `Use Slash Commands`
   - `View Channels`

5. Copy the OAuth2 URL, open it in a new browser tab, and follow the prompts to invite the bot to your server.

#### Step 3: Retrieve Your Bot Token

1. In the **Bot** section, under "Token", click "Reset Token" to generate a new token.
2. Copy the token to a secure location; this token is your bot's password and should be kept secret.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/Discord-AI-MiniGames.git
    cd Discord-AI-MiniGames
    ```

2. **Create a Python 3.11 virtual environment**:

    ```bash
    python3.11 -m venv venv
    ```

3. **Activate the virtual environment**:

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

4. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up the environment variables**:

    Rename the `example.env` file to `.env` and fill in the following variables:

    ```env
    TOKEN=your_discord_bot_token
    ```

6. **Run the bot**:

    ```bash
    python main.py
    ```

## Commands

##### 1. `/tictactoe play`
- **Description:** Start a game of Tic-Tac-Toe against the bot or an opponent.
- **Usage:** `/tictactoe play [opponent]`


## Contributing

Contributions are welcomed from the community. If you'd like to contribute, please fork the repository and submit a pull request with your changes. Make sure to follow the project's coding standards and conventions.

---

Feel free to customize the description, commands, and settings to better match your project's details!
