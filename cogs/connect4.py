import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Button, View
import random
import math

def create_board():
    # Initialize a 6x7 Connect 4 grid with empty slots
    return [["⚫" for _ in range(7)] for _ in range(6)]

def board_to_string(board, last_move_col=None):
    # Convert the board to a string, with an indicator for the last move
    top_row = "".join("⬇️" if col == last_move_col else "▪️" for col in range(7))
    column_emojis = "\n1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
    board_str = "\n".join("".join(row) for row in reversed(board))
    return f"{top_row}\n{board_str}\n{column_emojis}"

def is_valid_move(board, col):
    # Check if a column has space for another move
    return board[5][col] == "⚫"

def make_move(board, col, player_emoji):
    # Place the player's token in the lowest available row in the column
    for row in range(6):
        if board[row][col] == "⚫":
            board[row][col] = player_emoji
            break

def check_winner(board, player_emoji):
    # Check all directions to see if the player has four in a row
    def check_line(start_row, start_col, delta_row, delta_col):
        # Helper function to check a line of four in any direction
        for i in range(4):
            row = start_row + i * delta_row
            col = start_col + i * delta_col
            if not (0 <= row < 6 and 0 <= col < 7) or board[row][col] != player_emoji:
                return False
        return True

    # Scan the board in all directions for a winning line
    for row in range(6):
        for col in range(7):
            if (check_line(row, col, 0, 1) or  # Horizontal
                check_line(row, col, 1, 0) or  # Vertical
                check_line(row, col, 1, 1) or  # Diagonal down-right
                check_line(row, col, -1, 1)):  # Diagonal up-right
                return True
    return False

def get_valid_moves(board):
    # Return list of columns that still have space for moves
    return [col for col in range(7) if is_valid_move(board, col)]

def is_terminal_node(board):
    # Check if the game is over (win or full board)
    return check_winner(board, "🔴") or check_winner(board, "🟡") or len(get_valid_moves(board)) == 0

def minimax(board, depth, alpha, beta, maximizing_player, player_emoji):
    # Recursive minimax with alpha-beta pruning for AI move calculation
    opponent_emoji = "🔴" if player_emoji == "🟡" else "🟡"
    valid_moves = get_valid_moves(board)
    is_terminal = is_terminal_node(board)

    # End recursion if terminal state or depth limit is reached
    if depth == 0 or is_terminal:
        if check_winner(board, player_emoji):
            return (None, 1000000)
        elif check_winner(board, opponent_emoji):
            return (None, -1000000)
        else:
            return (None, 0)

    # Choose best move for maximizing or minimizing player
    if maximizing_player:
        max_eval = -math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            make_move(temp_board, col, player_emoji)
            eval = minimax(temp_board, depth - 1, alpha, beta, False, player_emoji)[1]
            if eval > max_eval:
                max_eval = eval
                best_col = col
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_col, max_eval
    else:
        min_eval = math.inf
        best_col = random.choice(valid_moves)
        for col in valid_moves:
            temp_board = [row[:] for row in board]
            make_move(temp_board, col, opponent_emoji)
            eval = minimax(temp_board, depth - 1, alpha, beta, True, player_emoji)[1]
            if eval < min_eval:
                min_eval = eval
                best_col = col
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_col, min_eval

class Connect4View(View):
    def __init__(self, player1, player2, is_ai=False):
        super().__init__(timeout=300)
        self.player1 = player1
        self.player2 = player2
        self.is_ai = is_ai
        self.current_turn = player1
        self.player_emojis = {player1: "🔴", player2: "🟡"}
        self.board = create_board()
        self.last_move_col = None
        self.message = None

        # Add buttons for each column and a forfeit button
        for i in range(7):
            button = Button(label=str(i + 1), style=discord.ButtonStyle.blurple, custom_id=str(i))
            button.callback = self.make_move_callback(i)
            self.add_item(button)

        forfeit_button = Button(label="Forfeit", style=discord.ButtonStyle.danger)
        forfeit_button.callback = self.forfeit_game
        self.add_item(forfeit_button)

    async def forfeit_game(self, interaction: discord.Interaction):
        # Handle player forfeit and declare the opponent as the winner
        winner = self.player2 if interaction.user == self.player1 else self.player1
        embed = discord.Embed(
            title=f"{self.player1.name} vs {self.player2.name}",
            description=f"{board_to_string(self.board, self.last_move_col)}\n\n**{winner.mention} wins the game by forfeit!**",
            color=discord.Color.red() if winner == self.player1 else discord.Color.yellow()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        self.stop()

    def make_move_callback(self, col):
        # Handle player moves and update the board
        async def callback(interaction: discord.Interaction):
            player_emoji = self.player_emojis[self.current_turn]

            if interaction.user != self.current_turn:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
                return

            if not is_valid_move(self.board, col):
                await interaction.response.send_message("This column is full. Choose another one.", ephemeral=True)
                return

            make_move(self.board, col, player_emoji)
            self.last_move_col = col

            # Update board and check for a winning move
            if check_winner(self.board, player_emoji):
                embed = discord.Embed(
                    title=f"{self.player1.name} vs {self.player2.name}",
                    description=f"{board_to_string(self.board, self.last_move_col)}\n\n**Winner:** {self.current_turn.mention}",
                    color=discord.Color.red() if self.current_turn == self.player1 else discord.Color.yellow()
                )
                await interaction.response.edit_message(embed=embed, view=None)
                self.stop()
            else:
                # Switch turn and update display
                self.current_turn = self.player2 if self.current_turn == self.player1 else self.player1
                current_color = discord.Color.red() if self.current_turn == self.player1 else discord.Color.yellow()
                embed = discord.Embed(
                    title=f"{self.player1.name} vs {self.player2.name}",
                    description=f"{board_to_string(self.board, self.last_move_col)}\n\n**Current turn:** {self.current_turn.mention}",
                    color=current_color
                )
                await interaction.response.edit_message(embed=embed, view=self)

                # If AI is active, make AI move
                if self.is_ai and self.current_turn == self.player2:
                    await self.make_ai_move(interaction)
        return callback

    async def make_ai_move(self, interaction: discord.Interaction):
        # AI makes a move, updates the board, and checks for win
        ai_emoji = self.player_emojis[self.player2]
        col, _ = minimax(self.board, 4, -math.inf, math.inf, True, ai_emoji)
        make_move(self.board, col, ai_emoji)
        self.last_move_col = col

        if check_winner(self.board, ai_emoji):
            embed = discord.Embed(
                title=f"{self.player1.name} vs {self.player2.name}",
                description=f"{board_to_string(self.board, self.last_move_col)}\n\n**Winner:** {self.player2.mention}",
                color=discord.Color.yellow()
            )
            await interaction.edit_original_response(embed=embed, view=None)
            self.stop()
        else:
            # Switch turn to human player
            self.current_turn = self.player1
            embed = discord.Embed(
                title=f"{self.player1.name} vs {self.player2.name}",
                description=f"{board_to_string(self.board, self.last_move_col)}\n\n**Current turn:** {self.current_turn.mention}",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=embed, view=self)

class Connect4(commands.GroupCog, group_name='connect4'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Command to start a new Connect 4 game
    @app_commands.command(description="Play Connect 4.")
    @app_commands.describe(opponent="Opponent of the game")
    async def play(self, interaction: discord.Interaction, opponent: discord.User = None):
        # Initialize opponent as AI if not specified or if player chooses themselves or the bot
        if opponent is None or opponent == interaction.user or opponent == self.bot.user:
            opponent = self.bot.user
            is_ai = True
        else:
            is_ai = False

        # Initialize the game view and embed
        view = Connect4View(player1=interaction.user, player2=opponent, is_ai=is_ai)
        embed = discord.Embed(
            title=f"{interaction.user.name} vs {opponent.name}",
            description=f"{board_to_string(view.board)}\n\n**Current turn:** {view.current_turn.mention}",
            color=discord.Color.red()
        )

        await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response()

# Function to set up the Connect 4 Cog in the bot
async def setup(bot):
    await bot.add_cog(Connect4(bot))
