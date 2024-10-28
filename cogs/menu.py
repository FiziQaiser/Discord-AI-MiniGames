import discord
from discord.ext import commands  # for slash commands
from discord import app_commands  # for slash commands
from discord.ui import Select, View

@app_commands.guild_only()
class Menu(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(description="Get list of commands.")
    async def help(self, interaction: discord.Interaction):
        try:
            supportButton = discord.ui.Button(label="Support Server", url='https://discord.gg/kTavknSvrZ')

            select = Select(placeholder="Select a Category for a Specific Module", options=[
                discord.SelectOption(
                    label="Main Menu",
                    emoji="🏠",
                    description="Get to Main Menu"),
                discord.SelectOption(
                    label="Tic-Tac-Toe",
                    emoji="❌",
                    description="Get All Tic-Tac-Toe Commands"),
                discord.SelectOption(
                    label="Connect4",
                    emoji="🔴",
                    description="Get All Connect4 Commands")
            ])

            embed = discord.Embed(
                title=f"⚙  Mini Games Help Desk", color=0x3dbbe3,
                description= 
                '''Click on the Dropdown to see each command within a Specific Category.

        **» List of Categories**
        ```❌ Tic-Tac-Toe
🔴 Connect4
    ```
    Seeking further assistance? Join our Support Discord Server for prompt and reliable help from our expert team and friendly community.''')
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1187679514684293181/1280874097672458371/pfp.png?ex=66d9aa76&is=66d858f6&hm=00be07ed9ec7a9a8a66a2a25ed84b28ceb9cc15a56e091e03cd942758ef8ba16&')
            embed.set_footer(text='Made with love by fizzy.py', icon_url='https://cdn.discordapp.com/attachments/1187679514684293181/1280874097672458371/pfp.png?ex=66d9aa76&is=66d858f6&hm=00be07ed9ec7a9a8a66a2a25ed84b28ceb9cc15a56e091e03cd942758ef8ba16&')

            async def my_callback(interaction):
                if select.values[0] == "Main Menu":
                    await interaction.response.edit_message(embed=embed, view=view)

                elif select.values[0] == "Tic-Tac-Toe":
                    await interaction.response.edit_message(embed=
                                            discord.Embed(title="❌ Tic-Tac-Toe Commands", color=0x3dbbe3,
                                            description=
                                            '''**» List of Commands**
    <**/tictactoe play**> : Play Tic-Tac-Toe.''').set_footer(
                                                            text='Made with love by fizzy.py', 
                                                            icon_url='https://cdn.discordapp.com/attachments/1187679514684293181/1280874097672458371/pfp.png?ex=66d9aa76&is=66d858f6&hm=00be07ed9ec7a9a8a66a2a25ed84b28ceb9cc15a56e091e03cd942758ef8ba16&'
                                                            ), view=view)
                
                elif select.values[0] == "Connect4":
                    await interaction.response.edit_message(embed=
                                            discord.Embed(title="🔴 Connect4 Commands", color=0x3dbbe3,
                                            description=
                                            '''**» List of Commands**
    <**/connect4 play**> : Play Connect4.''').set_footer(
                                                            text='Made with love by fizzy.py', 
                                                            icon_url='https://cdn.discordapp.com/attachments/1187679514684293181/1280874097672458371/pfp.png?ex=66d9aa76&is=66d858f6&hm=00be07ed9ec7a9a8a66a2a25ed84b28ceb9cc15a56e091e03cd942758ef8ba16&'
                                                            ), view=view)

            select.callback = my_callback
            view = View(timeout=300)
            view.add_item(select)
            view.add_item(supportButton)
            await interaction.response.send_message(embed=embed, view=view)
        except Exception as e:
            print(f"Error in help command: {e}")

async def setup(bot):
    await bot.add_cog(Menu(bot))
