import aiohttp
import asyncio

from .errors import HTTPException, Unauthorized


class HTTPSession:

    def __init__(self, loop, **attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        self.base_url = 'https://www.bankofmaldives.com.mv/internetbanking/api/'
        if username and password:
            self.login_params = {"username": username, "password": password}
        else:
            self.login_params = None
        self.accounts = []
        self.acc_populate = True
        if not self.login_params:
            raise Unauthorized('A username and password is needed to use this API.')
        jar = aiohttp.CookieJar(unsafe=True)
        header = {
            'Accept': '/',
            'Connection': 'keep-alive',
            'User-Agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
                'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')
        }
        self._session = aiohttp.ClientSession(loop=loop, cookie_jar=jar, headers=header)

    async def login(self):
        if not self.login_params:
            raise HTTPException("Unable to login, username and/or password not given")

        print("Login in using username and password...")
        await self._session.post(f"{self.base_url}login", data=self.login_params)
        async with self._session.get(f"{self.base_url}profile") as profile:
            if profile.status == 200:
                if self.acc_populate:
                    async with self._session.get(f"{self.base_url}dashboard") as dash:
                        if dash.status == 200:
                            data = await dash.json(encoding="utf-8")
                            self.accounts = [{x['id']: x['account']} for x in data['payload']['dashboard']]
                            self.acc_populate = False
                            return True
                        else:
                            print("Can't retrieve the accounts")
                            return False
                else:
                    return True
            print("Can't login...")
            return False

    async def request(self, method, url):
        data = await self._request(method, url)
        if data:
            if (data["message"] == "Please login") or (data["message"] == "Required to set Profile"):
                print("Session expired..")
                login = await self.login()
                if login:
                    data = await self._request(method, url)
                    if data:
                        if data["message"] == "Success":
                            transactions = data["payload"]["history"]
                            return transactions
                    else:
                        print("No history found.")
                        return None
                else:
                    print("Failed to login... Trying again..")
                    return None
            if data["message"] == "Success":
                transactions = data["payload"]["history"]
                return transactions
        else:
            print("No history found.")
            return None

    async def _request(self, method, url):
        async with self._session.request(method, f'{self.base_url}{url}') as resp:
            data = await resp.json(encoding="utf-8")
            return data

    async def close(self):
        await self._session.close()

    async def get_history(self):
        history = {}
        if self.acc_populate:
            await self.login()
        for x in self.accounts:
            for v in x:
                transactions = await self.request('GET', f'account/{v}/history/today')
                if transactions and (len(transactions) > 0):
                    history[x[v]] = [
                        {"date": tr["narrative2"], "sender": tr["narrative3"], "amount": tr["amount"], "minus": tr["minus"], "balance": tr["balance"], "description": tr["description"]} for tr in transactions]
        if history == {}:
            return None
        else:
            return history
