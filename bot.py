import discord
import json
import os
from discord.ext import commands

with open('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online,activity=discord.Game('Kagamine Rin'))
    print('>> Bot is ready ! <<')

@bot.command()
async def load(ctx,extension):
    """載入插件"""

    if ctx.channel.id != (int(jdata['CMDChannel'])):
        await ctx.send('請於指令區使用此指令')
        return
    else:
        pass

    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} 載入完成')

@bot.command()
async def reload(ctx,extension):
    """重新載入插件"""

    if ctx.channel.id != (int(jdata['CMDChannel'])):
        await ctx.send('請於指令區使用此指令')
        return
    else:
        pass

    bot.reload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} 已重新載入')

@bot.command()
async def unload(ctx,extension):
    """卸載插件"""

    if ctx.channel.id != (int(jdata['CMDChannel'])):
        await ctx.send('請於指令區使用此指令')
        return
    else:
        pass

    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'{extension} 卸載完成')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(jdata['TOKEN'])