def russian_roulette_game(members):
    victim = random.choice(members)
    return victim

class BotCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(ctx):
        await ctx.send('Hello!')

    @commands.command(name='beer_me')
    async def beer_me(ctx):
        member = ctx.author.name
        await ctx.send(f'*Pours a frosty cold beer and slides it over to {member}.*')

    @commands.command(name='dice_game')
    async def roll_dice(ctx):
        #player turn
        die_one = random.randint(1, 6)
        die_two = random.randint(1, 6)
        dice_roll = die_one + die_two
        await ctx.send(f"You rolled a {dice_roll}!")
        #bot turn
        await ctx.send("Now it's my turn...")
        bot_one = random.randint(1,6)
        bot_two = random.randint(1,6)
        bot_roll = bot_one + bot_two
        await ctx.send(f"I rolled a {bot_roll}")
        #who win
        if(dice_roll > bot_roll):
            await ctx.send("Rats! You win.")
        elif(dice_roll < bot_roll):
            await ctx.send("You lose. GG.")
        else:
            await ctx.send("A draw!")

    @commands.command(name='roll_dice')
    async def roll_dice(ctx):
        die_one = random.randint(1, 6)
        die_two = random.randint(1, 6)
        dice_roll = die_one + die_two
        await ctx.send(f"You rolled a {dice_roll}!")

    @commands.command(name='russian_roulette')
    async def russian_roulette(ctx):
        members = ctx.author.voice.channel.members
        victim = russian_roulette_game(members)
        await ctx.send(f'*The gun points to {victim.name}* Goodbye!')
        await ctx.send('*BANG!*')
        #await victim.move_to(None, reason='Lost in Russian Roulette')
        await victim.edit(voice_channel=None, reason='Lost in Russian Roulette. Get out.')

    @commands.command(name='play_music')
    async def play_music(ctx, url: str):
        channel = ctx.author.voice.channel
        voice_channel = get(bot.voice_clients, guild=ctx.guild)

        if voice_channel and voice_channel.is_connected():
            await voice_channel.move_to(channel)
        else:
            voice_channel = await channel.connect()

        with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info['formats'][0]['url']
            voice_channel.play(discord.FFmpegPCMAudio(URL))

    @commands.command(name='stop_music')
    async def stop_music(ctx):
        voice_channel = get(bot.voice_clients, guild=ctx.guild)
        if voice_channel and voice_channel.is_playing():
            voice_channel.stop()

    @commands.command(name='log_off')
    async def fuck_off(ctx):
        await ctx.send('Will do, sir. Logging off...')
        await bot.close()

def setup(bot):
    bot.add_cog(BotCommands(bot))