import discord
from discord.ext import commands
import json

with open('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Events(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        channel = self.bot.get_channel(int(jdata['MainChannel']))
        role = discord.utils.get(member.guild.roles,name="成員")
        await member.add_roles(role)
        await channel.send(f'歡迎新成員 {member} 加入了我們')

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        channel = self.bot.get_channel(int(jdata['MainChannel']))
        await channel.send(f'看來 {member} 不要我們了')

def setup(bot):
    bot.add_cog(Events(bot))