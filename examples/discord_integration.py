from discord.ext import commands
from aiobml import asyncBML
from random import choice
import asyncio


class BML(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.bank = asyncBML(username="ur_user_name", password="ur_pass", loop=bot.loop)
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

def setup(bot):
    bot.add_cog(BML(bot))
