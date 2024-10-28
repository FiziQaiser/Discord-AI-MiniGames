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

**Discord-AI-MiniGames** is a Discord bot that brings classic games with a twist of advanced AI. This repository currently features Tic-Tac-Toe and Connect 4, allowing players to challenge computer opponents or friends in games that use optimal strategies. Built with `discord.py`, this bot offers intelligent gameplay and a fun experience.

## Features

- **Play with Friends or Against AI:** Enjoy Tic-Tac-Toe and Connect 4 with other users or challenge the bot, which uses advanced AI for strategic gameplay.
- **Tic-Tac-Toe with Alpha-Beta Pruning Minimax Algorithm:** The bot leverages Alpha-Beta Pruning with the Minimax algorithm to deliver a competitive Tic-Tac-Toe experience.
- **Connect 4 with Alpha-Beta Pruning Minimax Algorithm:** Challenge the bot in Connect 4, where it applies optimal decision-making through Alpha-Beta Pruning to create a challenging experience.
- **Discord Integration:** Seamlessly integrates with Discord using `discord.py` for smooth and interactive gameplay.
- **Game Expansion:** The bot’s design supports the addition of new games and AI-based features, enabling ongoing enhancements.


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

##### 2. `/connect4 play`
- **Description:** Start a game of Connect 4 against the bot or an opponent.
- **Usage:** `/connect4 play [opponent]`

## Contributing

Contributions are welcomed from the community. If you'd like to contribute, please fork the repository and submit a pull request with your changes. Make sure to follow the project's coding standards and conventions.

---

This README now includes a section for the Connect 4 command, and the updated features section reflects the addition of Connect 4.