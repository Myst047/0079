import discord
import sqlite3
import config
import random
from discord.ext import commands


bot = commands.Bot(command_prefix='...',intents=discord.Intents.all())

conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT,
                    quote_text TEXT
                  )''')
conn.commit()

BOT_OWNER_ID = '1119262835499872257'

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    # Get the channel ID where you want to send the message
    channel_id = 1209877265031102484 # Replace YOUR_CHANNEL_ID with the actual channel ID
    
    # Fetch the channel object
    channel = bot.get_channel(channel_id)
    
    if channel:
        # Send a message in the specified channel
        await channel.send("I'm online and ready to assist!")
    else:
        print(f"Channel with ID {channel_id} not found.")

@bot.event
async def on_command_error(ctx, error):
    # Send the error message to the channel where the command was used
    await ctx.send(f'An error occurred: {error}')


@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)  # Convert to milliseconds and round to 2 decimal places
    await ctx.send(f'Ping! Latency: {latency}ms')

@bot.command()
async def purge(ctx, amount: int):
    # Check if the user has permissions to manage messages
    if ctx.author.guild_permissions.manage_messages:
        # Delete the specified number of messages
        await ctx.channel.purge(limit=amount + 1)  # Add 1 to include the command message
        await ctx.send(f'{amount} messages deleted.', delete_after=5)  # Send a confirmation message
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def propose(ctx, *, message):
    # Get the user mentioned in the message
    mentioned_user = ctx.message.mentions[0] if ctx.message.mentions else None
    
    if mentioned_user:
        proposal_message = f"Hey {mentioned_user.mention}, {ctx.author.name} has a message for you: {message}"
        await ctx.send(proposal_message)
    else:
        await ctx.send("Please mention the person you want to propose to.")

@bot.event
async def on_member_join(member):
    # Check if the member who joined is the specific user
    if member.id == 927875265273679913:  # Replace SPECIFIC_USER_ID with the actual user ID
        # Get the channel where you want to send the message
        channel = bot.get_channel(1208348111743746080)  # Replace CHANNEL_ID with the actual channel ID
        
        if channel:
            # Send a welcome message to the channel
            await channel.send(f'Welcome {member.mention} to the server! Every moment with you feels like a dream come true. Will you make my dreams a reality and be mine forever?')
        else:
            print(f"Channel with ID {CHANNEL_ID} not found.")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked.')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} has been banned.')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{user.mention} has been unbanned.')
            return

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f'{amount} messages have been cleared.', delete_after=5)

@bot.command()
async def mute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        await ctx.guild.create_role(name="Muted")
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role)
    await ctx.send(f'{member.mention} has been muted.')

@bot.command()
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f'{member.mention} has been unmuted.')
    else:
        await ctx.send(f'{member.mention} is not muted.')

@bot.command()
async def eval(ctx, *, code: str):
    if ctx.author.id != 1119262835499872257:  # Replace YOUR_ID with your own Discord user ID
        return

    try:
        result = eval(code)
        await ctx.send(result)
    except Exception as e:
        await ctx.send(f'An error occurred: {e}')

@bot.command()
async def rps(ctx, choice: str):
    import random
    choices = ["rock", "paper", "scissors"]
    bot_choice = random.choice(choices)
    if choice.lower() not in choices:
        return await ctx.send("Invalid choice. Please choose rock, paper, or scissors.")
    if choice.lower() == bot_choice:
        await ctx.send(f"It's a tie! I also chose {bot_choice}.")
    elif (choice.lower() == "rock" and bot_choice == "scissors") or (choice.lower() == "paper" and bot_choice == "rock") or (choice.lower() == "scissors" and bot_choice == "paper"):
        await ctx.send(f"Congratulations! You won! I chose {bot_choice}.")
    else:
        await ctx.send(f"Oops! You lost! I chose {bot_choice}.")

@bot.command()
async def hack(ctx, target: discord.Member):
    # Simulate a hacking scenario
    await ctx.send(f"Hacking into {target.name}'s account...")

    # Show fake progress
    for i in range(1, 6):
        await ctx.send(f"Progress: {i * 20}%")
    
    # Display fake results
    await ctx.send(f"Hack successful! {target.name}'s account compromised. 🎉")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def nuke(ctx):
    # Confirm with the user before proceeding
    await ctx.send("Are you sure you want to nuke the server? This action is irreversible. (yes/no)")
    try:
        # Wait for user confirmation
        response = await bot.wait_for("message", timeout=30.0, check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        if response.content.lower() == "yes":
            # Delete all channels
            for channel in ctx.guild.channels:
                await channel.delete()
            # Create new channels
            # Add your channel creation logic here
            await ctx.send("Server has been nuked! New channels have been created.")
        else:
            await ctx.send("Nuke cancelled.")
    except asyncio.TimeoutError:
        await ctx.send("Nuke cancelled due to timeout.")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def anti_nuke(ctx):
    # Fetch audit logs to check for recent channel deletions
    async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.channel_delete, limit=10):
        if entry.action == discord.AuditLogAction.channel_delete:
            channel = entry.target
            channel_name = channel.name if isinstance(channel, discord.TextChannel) else f'Unknown Channel (ID: {channel.id})'
            await ctx.send(f"Channel '{channel_name}' was deleted by {entry.user} at {entry.created_at}. Restoring...")
            try:
                # Restore the deleted channel
                restored_channel = await channel.restore(reason="Anti-nuke command triggered")
                await ctx.send(f"Channel '{restored_channel.name}' has been restored.")
            except discord.Forbidden:
                await ctx.send("I do not have permission to restore channels.")

@bot.command()
async def k(ctx, user: discord.Member):
    # Check if the command was used in a guild
    if ctx.guild is None:
        return await ctx.send("This command can only be used in a server.")

    # Check if the bot has permission to attach files
    if not ctx.guild.me.guild_permissions.attach_files:
        return await ctx.send("I don't have permission to attach files.")

    # Define the GIF URL
    gif_url = "https://media1.tenor.com/images/2a02cb00b419b34f77a7d5362ab94d58/tenor.gif?itemid=14740327"

    # Construct the message
    message = f"{ctx.author.mention} kisses {user.mention} 💋"

    # Send the message with the attached GIF
    await ctx.send(message, file=discord.File("kiss.gif", filename="kiss.gif"))

#### QUOTE BOT ####
        
@bot.command()
async def addquote(ctx, *, quote):
    user_id = str(ctx.author.id)
    cursor.execute("INSERT INTO quotes (user_id, quote_text) VALUES (?, ?)", (user_id, quote))
    conn.commit()
    await ctx.send('Quote added successfully!')

@bot.command()
async def quote(ctx, user: discord.User):
    if not args: 
        user_id = str(message.user.id)
    else:
        user_id = str(user.id)
    cursor.execute("SELECT quote_text FROM quotes WHERE user_id=?", (user_id,))
    quotes = cursor.fetchall()
    if quotes:
        quote = random.choice(quotes)[0]
        await ctx.send(f'Quotes from {user.name}: {quote}')
    else:
        await ctx.send('No quotes available for this user.')

@bot.command()
async def allquotes(ctx):
    cursor.execute("SELECT user_id, quote_text FROM quotes")
    quotes = cursor.fetchall()
    if quotes:
        quote_dict = {}
        for user_id, quote_text in quotes:
            if user_id not in quote_dict:
                quote_dict[user_id] = []
            quote_dict[user_id].append(quote_text)
        for user_id, quotes in quote_dict.items():
            user = bot.get_user(int(user_id))
            quote_str = '\n'.join(quotes)
            await ctx.send(f'Quotes from {user.name}:\n{quote_str}')
    else:
        await ctx.send('No quotes available.')

@bot.command()
async def daq(ctx):
    # Check if the command invoker is the bot owner
    if str(ctx.author.id) == BOT_OWNER_ID:
        cursor.execute("DELETE FROM quotes")
        conn.commit()
        await ctx.send('All quotes deleted successfully!')
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def deletequote(ctx, quote_id: int):
    user_id = str(ctx.author.id)
    cursor.execute("SELECT user_id FROM quotes WHERE id=?", (quote_id,))
    user = cursor.fetchone()
    if user:
        # Check if the user trying to delete the quote is the owner of the quote
        if user_id == user[0]:
            cursor.execute("DELETE FROM quotes WHERE id=?", (quote_id,))
            conn.commit()
            await ctx.send('Quote deleted successfully!')
        else:
            await ctx.send("You don't have permission to delete this quote.")
    else:
        await ctx.send('Quote not found.')

conn.close()

#### PET BOT #####
pets = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def adopt(ctx, pet_name):
    if pet_name not in pets:
        pets[pet_name] = {'owner_id': ctx.author.id, 'hunger': 50, 'happiness': 50, 'health': 100}
        await ctx.send(f'Congratulations, you have adopted a pet named {pet_name}!')
    else:
        await ctx.send('Sorry, that pet name is already taken.')

@bot.command()
async def feed(ctx, pet_name):
    if pet_name in pets:
        pets[pet_name]['hunger'] -= random.randint(5, 15)
        await ctx.send(f'{pet_name} has been fed.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def play(ctx, pet_name):
    if pet_name in pets:
        pets[pet_name]['happiness'] += random.randint(5, 15)
        await ctx.send(f'{pet_name} is happy after playing.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def stats(ctx, pet_name):
    if pet_name in pets:
        stats_message = f"Stats for {pet_name}:\n"
        for stat, value in pets[pet_name].items():
            if stat != 'owner_id':
                stats_message += f"{stat.capitalize()}: {value}\n"
        await ctx.send(stats_message)
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def mypets(ctx):
    user_pets = [pet_name for pet_name, pet_data in pets.items() if pet_data['owner_id'] == ctx.author.id]
    if user_pets:
        pets_list = ', '.join(user_pets)
        await ctx.send(f'Your pets: {pets_list}')
    else:
        await ctx.send('You don\'t have any pets.')

@bot.command()
async def rename(ctx, old_name, new_name):
    if old_name in pets:
        pets[new_name] = pets.pop(old_name)
        await ctx.send(f'{old_name} has been renamed to {new_name}.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def heal(ctx, pet_name):
    if pet_name in pets:
        pets[pet_name]['health'] = 100
        await ctx.send(f'{pet_name} has been healed.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def remove(ctx, pet_name):
    if pet_name in pets:
        pets.pop(pet_name)
        await ctx.send(f'{pet_name} has been removed.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')

@bot.command()
async def revive(ctx, pet_name):
    if pet_name in pets:
        if pets[pet_name]['health'] <= 0:
            pets[pet_name]['health'] = 50
            pets[pet_name]['hunger'] = 50
            pets[pet_name]['happiness'] = 50
            await ctx.send(f'{pet_name} has been revived with reduced stats.')
        else:
            await ctx.send(f'{pet_name} is already alive.')
    else:
        await ctx.send('Sorry, you don\'t have a pet with that name.')
        
#### Calculator ####
@bot.command()
async def calculator(ctx):
    # Create an embed with buttons for numbers and operations
    embed = discord.Embed(title="Calculator", description="React with the corresponding emoji to select a number or operation")
    embed.add_field(name="1️⃣", value="1", inline=True)
    embed.add_field(name="2️⃣", value="2", inline=True)
    embed.add_field(name="3️⃣", value="3", inline=True)
    embed.add_field(name="4️⃣", value="4", inline=True)
    embed.add_field(name="5️⃣", value="5", inline=True)
    embed.add_field(name="6️⃣", value="6", inline=True)
    embed.add_field(name="7️⃣", value="7", inline=True)
    embed.add_field(name="8️⃣", value="8", inline=True)
    embed.add_field(name="9️⃣", value="9", inline=True)
    embed.add_field(name="0️⃣", value="0", inline=True)
    embed.add_field(name=".", value=".", inline=True)
    embed.add_field(name="Clear", value="Clear", inline=True)
    embed.add_field(name="End", value="End", inline=True)

    # Send the embedded message with buttons
    msg = await ctx.send(embed=embed)

    # Add reactions to the message
    reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "0️⃣", ".", "🔴", "⏹️"]
    for reaction in reactions:
        await msg.add_reaction(reaction)

    # Define check function to filter reactions
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in reactions

    # Initialize an empty expression string
    expression = ""

    # Wait for reactions and construct the expression
    while True:
        reaction, user = await bot.wait_for("reaction_add", check=check)
        emoji = str(reaction.emoji)

        if emoji == "⏹️":  # End the calculator
            break
        elif emoji == "🔴":  # Clear the expression
            expression = ""
        else:
            expression += emoji.replace("️⃣", "")  # Add number or decimal point to the expression

    await ctx.send(f"Expression: {expression}")  # Send the final expression


bot.run(config.BOT_TOKEN)