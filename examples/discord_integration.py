"""
MIT License
Copyright (c) 2021 Ali Fayaz (Quill) (quillfires)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from discord.ext import commands
from aiobml import asyncBML
from random import choice
from discord import Embed
from datetime import datetime
import asyncio


class BML(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.bank = asyncBML(username="ur_user_name", password="ur_pass")
        bot.loop.create_task(self.start())
        self.bank.event("new_transaction")(self.on_new_transaction)

    # Check if the transection is new
    async def check_if_new(self, transaction):
        db_data = self.db.find(transaction) # check the db
        if len([r for r in await db_data.to_list(length=None)]) > 0:
            return False
        return True

    async def start(self):
        await self.bot.wait_until_ready()
        self.me = self.bot.get_user(475785856137953280)
        await self.bank.start()

    async def on_new_transaction(self, transaction):
        is_new = await self.check_if_new(transaction)
        if is_new:
            # insert into db
            await self.db.insert_one(transaction)
            # send me the transaction
            await self.me.send(f"**New transaction**\n{transaction['description']} of MVR {transaction['amount']} {'to' if transaction['minus'] else 'from'} {transaction['date'] if transaction['sender']=='' else transaction['sender']}")

    @commands.command()
    @commands.check(commands.is_owner())
    @commands.guild_only()
    async def contacts(self, ctx):
        """
        Get the contact details from your bml account
        """
        contacts = await self.bank.get_contacts()
        e = Embed(title = f"**BML Contacts**", color = 0xff0000)
        line = ""
        for x in contacts:
            line += f"**Name:** {x['name']}\n**Alias:** {x['name']}\n**Account number:** {x['account']}\n"
        e.description = line
        e.timestamp = datetime.now()
        await ctx.send(embed=e)

    @commands.command()
    @commands.check(commands.is_owner())
    @commands.guild_only()
    async def accounts(self, ctx):
        """
        Get all your account details.
        """
        contacts = await self.bank.get_accounts()
        e = Embed(title = f"**BML Accounts**", color = 0xff0000)
        line = ""
        for x in contacts:
            line += f"**{x['product']}**\n**Currency:** {x['currency']}\n**Account number:** {x['account']}\n"
            try:
                line += f"**Balance:** {x['availableBalance']}\n"
            except:
                pass
            try:
                line += f"**Balance:** {x['cardBalance']['CurrentBalance']}\n"
            except:
                pass
        e.description = line
        e.timestamp = datetime.now()
        await ctx.send(embed=e)

    @commands.command()
    @commands.check(commands.is_owner())
    @commands.guild_only()
    async def addcont(self, ctx, account, name):
        """
        Add an account to your contacts.
        """
        try:
            contact = await self.bank.add_contact(account, name)
            e = Embed(title = f"**Contact Added**", color = 0x00ff00)
            e.description = f"{contact['name']}'s account {contact['account']} successfully added under the alias {name}"
        except Exception as error:
            e = Embed(title = f"**Failed**", color = 0xff0000)
            e.description = error
        e.timestamp = datetime.now()
        await ctx.send(embed=e)

    @commands.command()
    @commands.check(commands.is_owner())
    @commands.guild_only()
    async def delcont(self, ctx, account):
        """
        Delete an account from your contacts.
        """
        e = Embed(title = f"**Contact Removed**", color = 0x00ff00)
        try:
            contact = await self.bank.delete_contact(account)
            e.description = contact
        except Exception as error:
            e.title = "**Failed**"
            e.color = 0xff0000
            e.description = error
        e.timestamp = datetime.now()
        await ctx.send(embed=e)

                               
def setup(bot):
    bot.add_cog(BML(bot))
