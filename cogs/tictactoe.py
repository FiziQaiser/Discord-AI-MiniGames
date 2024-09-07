import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import numpy as np

# Define custom emojis for Tic-Tac-Toe symbols
DASH_EMOJI = "<:dash:1280895467562995804>"
CIRCLE_EMOJI = "<:circle:1280884553233334395>"
CROSS_EMOJI = "<:cross:1280884530558795786>"

# Function to create an empty Tic-Tac-Toe board
def create_board():
    return np.zeros((3, 3), dtype=int)

# Function to check if the board is full (i.e., no more moves are possible)
def is_board_full(board):
    return np.all(board != 0)

# Function to evaluate the current board state
# Returns 1 if player 1 (cross) wins, 2 if player 2 (circle) wins, -1 for a tie, and 0 for an ongoing game
def evaluate(board):
    for player in [1, 2]:
        if np.any(np.all(board == player, axis=0)) or \
           np.any(np.all(board == player, axis=1)) or \
           np.all(np.diag(board) == player) or \
           np.all(np.diag(np.fliplr(board)) == player):
            return player
    if is_board_full(board):
        return -1
    return 0

# Minimax algorithm with alpha-beta pruning to determine the best move for the AI
# The algorithm evaluates possible moves and chooses the optimal one for the AI
def minimax(board, depth, maximizing_player, alpha, beta):
    winner = evaluate(board)
    if winner != 0:
        if winner == -1:    # If it's a tie
            return 0
        elif maximizing_player:
            return winner * (depth + 1)
        else:
            return winner * (depth + 1)

    if maximizing_player:
        max_eval = -np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 2
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = 0             # undo move to evaluate other board places
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)    # Alpha Beta Pruning
                    if beta <= alpha:
                        break
                if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = np.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = 0         # undo move to evaluate other board places
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)  # Alpha Beta Pruning
                    if beta <= alpha:
                        break
                if beta <= alpha:
                        break
        return min_eval

# Function to find the best possible move for the AI using the minimax algorithm
def find_best_move(board):
    best_val = -np.inf
    best_move = None
    alpha = -np.inf
    beta = np.inf
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = 2
                move_val = minimax(board, 0, False, alpha, beta)
                board[i][j] = 0
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)
    return best_move

# Button class for each Tic-Tac-Toe cell
# Inherits from discord.ui.Button and handles the interaction for a specific cell
class TicTacToeButton(Button):
    def __init__(self, row: int, col: int):
        super().__init__(emoji=DASH_EMOJI, style=discord.ButtonStyle.secondary, row=row)
        self.row = row
        self.col = col

    # Callback method for when a button is clicked
    async def callback(self, interaction: discord.Interaction):
        view: TicTacToeView = self.view
        if view.current_turn != interaction.user and not view.is_ai_turn:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)
            return

        # Update button to the current player's emoji and disable it
        self.emoji = view.current_emoji_turn
        self.style = discord.ButtonStyle.danger if view.current_emoji_turn == CROSS_EMOJI else discord.ButtonStyle.success
        self.disabled = True
        view.board[self.row][self.col] = 1 if view.current_emoji_turn == CROSS_EMOJI else 2
        await interaction.response.edit_message(view=view)

        # Check for a win or a draw
        if view.check_winner():
            await interaction.followup.send(f"{interaction.user.name} wins!")
            view.disable_all_buttons()
            await interaction.edit_original_response(view=view)
        elif view.is_draw():
            await interaction.followup.send("It's a draw!")
            view.disable_all_buttons()
            await interaction.edit_original_response(view=view)
        else:
            # Alternate the turn to the other player and change the emoji
            view.current_turn = view.player2 if view.current_turn == view.player1 else view.player1
            view.current_emoji_turn = CIRCLE_EMOJI if view.current_emoji_turn == CROSS_EMOJI else CROSS_EMOJI

            # If the AI is playing, make the AI move
            if view.is_ai_turn:
                await view.make_ai_move(interaction)

# View class to manage the Tic-Tac-Toe game board and player turns
# Inherits from discord.ui.View and manages the overall game state
class TicTacToeView(View):
    def __init__(self, player1: discord.User, player2: discord.User, is_ai=False):
        super().__init__(timeout=300)
        self.player1 = player1
        self.player2 = player2
        self.is_ai_turn = is_ai
        self.current_turn = player1
        self.current_emoji_turn = CROSS_EMOJI
        self.board = create_board()

        # Add buttons to the view, representing the Tic-Tac-Toe grid
        for row in range(3):
            for col in range(3):
                button = TicTacToeButton(row=row, col=col)
                self.add_item(button)

    # Check if there's a winner based on the current board state
    def check_winner(self):
        winner = evaluate(self.board)
        return winner != 0

    # Check if the game is a draw (i.e., no more moves possible and no winner)
    def is_draw(self):
        return is_board_full(self.board)

    # Disable all buttons in the view after the game ends
    def disable_all_buttons(self):
        for item in self.children:
            item.disabled = True

    # AI makes its move based on the best possible outcome using minimax
    async def make_ai_move(self, interaction: discord.Interaction):
        best_move = find_best_move(self.board)
        if best_move:
            row, col = best_move
            button = self.children[row * 3 + col]
            button.emoji = CIRCLE_EMOJI
            button.style = discord.ButtonStyle.success
            button.disabled = True
            self.board[row][col] = 2
            await interaction.edit_original_response(view=self)

            if self.check_winner():
                await interaction.followup.send(f"Miini-Games wins!")
                self.disable_all_buttons()
                await interaction.edit_original_response(view=self)
            elif self.is_draw():
                await interaction.followup.send("It's a draw!")
                self.disable_all_buttons()
                await interaction.edit_original_response(view=self)
            else:
                self.current_turn = self.player1
                self.current_emoji_turn = CROSS_EMOJI

# TicTacToe Cog to manage the Tic-Tac-Toe commands
class TicTacToe(commands.GroupCog, group_name='tictactoe'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Command to start a Tic-Tac-Toe game
    @app_commands.command(description="Play Tic-Tac-Toe.")
    @app_commands.describe(opponent="Opponent of the game")
    async def play(self, interaction: discord.Interaction, opponent: discord.User = None):
        if opponent is None:
            opponent = self.bot.user  # Bot will be the default opponent
            is_ai = True
        else:
            is_ai = False

        # Initialize the TicTacToeView with players and start the game
        view = TicTacToeView(player1=interaction.user, player2=opponent, is_ai=is_ai)
        await interaction.response.send_message(f"The following is the game between {interaction.user.name} and {opponent.name}", view=view)

# Function to set up the TicTacToe Cog in the bot
async def setup(bot):
    await bot.add_cog(TicTacToe(bot))
