import discord
from discord.ext import commands
import random
import json

with open('setting.json',mode='r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

errortxt = ('格式不正確或未使用有效的正整數 ',
            '正確的格式是：\n`/mw <列> <行數> <炸彈>`\n\n',
            '如果你什麼都不打 將會隨機生成地圖')
errortxt = ''.join(errortxt)

class Minigames(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def guess(self,context):
        """猜數字遊戲"""
        
        if context.channel.id != (int(jdata['GuessChannel'])):
            await context.send('請於小遊戲分類中的猜數字頻道使用此指令')
            return
        else:
            pass

        answer = random.randint(1, 100)
        chance = 6
        stop = 0

        channel = self.bot.get_channel(int(jdata['GuessChannel']))

        await channel.send('在 1 ~ 100 中猜數字 總共有 {} 次機會'.format(chance+1))

        def check(message):
            
            try:
                int(message.content)
                return True
            except ValueError:
                return False

        if context.author == self.bot.user:
            return

        for guess in range(0,7):
            msg = await self.bot.wait_for('message', check=check)
            attempt = int(msg.content)

            if attempt == answer:
                await channel.send('恭喜你猜對了 !')
                break

            elif chance == stop :
                await channel.send('太可惜了 你沒猜到 答案是 {}'.format(answer))
                break

            elif attempt > answer:
                await channel.send('再低一點 你還有 {} 次機會'.format(chance))
                chance = chance-1
                

            elif attempt < answer:
                await channel.send('再高一點 你還有 {} 次機會'.format(chance))
                chance = chance-1

    @commands.command()
    async def ms(self, ctx, columns = None, rows = None, bombs = None):
        """踩地雷"""

        if ctx.channel.id != (int(jdata['MineSweeperChannel'])):
            await ctx.send('請於小遊戲分類中的踩地雷頻道使用此指令')
            return
        else:
            pass

        channel = self.bot.get_channel(int(jdata['MineSweeperChannel']))

        if columns is None or rows is None and bombs is None:
            if columns is not None or rows is not None or bombs is not None:
                await channel.send(errortxt)
                return
            else:
                columns = random.randint(4,13)
                rows = random.randint(4,13)
                bombs = columns * rows - 1
                bombs = bombs / 2.5
                bombs = round(random.randint(5, round(bombs)))
        try:
            columns = int(columns)
            rows = int(rows)
            bombs = int(bombs)
        except ValueError:
            await channel.send(errortxt)
            return
        if columns > 13 or rows > 13:
            await channel.send('由於Discord的限制，列和行的限制為13 ...')
            return
        if columns < 1 or rows < 1 or bombs < 1:
            await channel.send('提供的數字不能為零或負...')
            return
        if bombs + 1 > columns * rows:
            await channel.send(':boom:**BOOM**, 太多炸彈了 你可能會繞行地球100圈 試著填少一點')
            return
        
        grid = [[0 for num in range (columns)] for num in range(rows)]

        loop_count = 0
        while loop_count < bombs:

            x = random.randint(0, columns - 1)
            y = random.randint(0, rows - 1)

            if grid[y][x] == 0:
                grid[y][x] = 'B'
                loop_count = loop_count + 1

            if grid[y][x] == 'B':
                pass

        pos_x = 0
        pos_y = 0
        while pos_x * pos_y < columns * rows and pos_y < rows:

            adj_sum = 0

            for (adj_y, adj_x) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:

                try:
                    if grid[adj_y + pos_y][adj_x + pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:

                        adj_sum = adj_sum + 1
                except Exception as error:
                  
                    pass

            if grid[pos_y][pos_x] != 'B':
                grid[pos_y][pos_x] = adj_sum

            if pos_x == columns - 1:
                pos_x = 0
                pos_y = pos_y + 1
            else:
                pos_x = pos_x + 1

        string_builder = []
        for the_rows in grid:
            string_builder.append(''.join(map(str, the_rows)))
        string_builder = '\n'.join(string_builder)

        string_builder = string_builder.replace('0', '||:zero:||')
        string_builder = string_builder.replace('1', '||:one:||')
        string_builder = string_builder.replace('2', '||:two:||')
        string_builder = string_builder.replace('3', '||:three:||')
        string_builder = string_builder.replace('4', '||:four:||')
        string_builder = string_builder.replace('5', '||:five:||')
        string_builder = string_builder.replace('6', '||:six:||')
        string_builder = string_builder.replace('7', '||:seven:||')
        string_builder = string_builder.replace('8', '||:eight:||')
        final = string_builder.replace('B', '||:bomb:||')

        percentage = columns * rows
        percentage = bombs / percentage
        percentage = 100 * percentage
        percentage = round(percentage, 2)

        embed = discord.Embed(title='\U0001F642 Minesweeper \U0001F635', color=0xC0C0C0)
        embed.add_field(name='Columns:', value=columns, inline=True)
        embed.add_field(name='Rows:', value=rows, inline=True)
        embed.add_field(name='Total Spaces:', value=columns * rows, inline=True)
        embed.add_field(name='\U0001F4A3 Count:', value=bombs, inline=True)
        embed.add_field(name='\U0001F4A3 Percentage:', value=f'{percentage}%', inline=True)
        embed.add_field(name='Requested by:', value=ctx.author.display_name, inline=True)
        await channel.send(content=f'\U0000FEFF\n{final}', embed=embed)

    @ms.error
    async def minesweeper_error(self, ctx, error):
        await ctx.send(errortxt)
        return            

def setup(bot):
    bot.add_cog(Minigames(bot))