import asyncio
from .aiobmlcore.http import HTTPSession


class asyncBML():
    def __init__(self, *, loop=None, username=None, password=None):
        loop = loop or asyncio.get_event_loop()
        self.http = HTTPSession(loop=loop, username=username, password=password)

    async def close(self):
        await self.http.close()

    async def get_history(self) -> dict:
        """|coro|

        Method which retrieves the account history.

        Returns
        ---------
        dict: transactions
            Dictionary object containing transactions relating to each account.
            {account1:{[transaction1,transaction2]},account2:{[transaction1,transaction2]},}

        Raises
        --------
        HTTPException
            Bad request while fetching transactions.
        """
        data = await self.http.get_history()
        return data
