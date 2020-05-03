import discord
from discord.ext import commands
import json

with open('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

class Commands(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def kick(self,ctx,member : discord.Member,*,reason=None):
        """剔除用戶""" 
        if ctx.channel.id != (int(jdata['CMDChannel'])):
            await ctx.send('請於指令區使用此指令')
            return
        else:
            pass
        channel = self.bot.get_channel(int(jdata['CMDChannel']))
        await member.kick(reason=reason)
        await channel.send(f'{member.mention} 被隔離了')


    @commands.command()
    async def ban(self,ctx,member : discord.Member,*,reason=None):
        """封鎖用戶"""
        if ctx.channel.id != (int(jdata['CMDChannel'])):
            await ctx.send('請於指令區使用此指令')
            return
        else:
            pass
        channel = self.bot.get_channel(int(jdata['CMDChannel']))
        await member.ban(reason=reason)
        await channel.send(f'{member.mention} 化成了灰燼')

    @commands.command()
    async def unban(self,ctx,*,member):
        """解除封鎖用戶"""
        if ctx.channel.id != (int(jdata['CMDChannel'])):
            await ctx.send('請於指令區使用此指令')
            return
        else:
            pass
        channel = self.bot.get_channel(int(jdata['CMDChannel']))

        banned_users = await ctx.guild.bans()
        member_name,member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name,user.discriminator) == (member_name,member_discriminator):
                await ctx.guild.unban(user)
                await channel.send(f'{user.mention} 被復活了')
                return

    @commands.command()
    async def ping(self,ctx):
        """查看機器人延遲"""
        await ctx.send(f'機器人延遲 : {round(self.bot.latency*1000)} 毫秒')

    @commands.command()
    async def clear(self,ctx,amount=None):
        """清除訊息"""
        await ctx.channel.purge(limit=None, check=lambda msg: not msg.pinned)

    @commands.command()
    async def repeat(self,ctx,*,message):
        """重述訊息"""
        await ctx.message.delete()
        await ctx.send(message)

def setup(bot):
    bot.add_cog(Commands(bot))