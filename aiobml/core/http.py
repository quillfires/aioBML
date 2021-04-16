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
import aiohttp

from .errors import *


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
                    dash = await self._session.get(f"{self.base_url}dashboard")
                    if dash.status == 200:
                        data = await dash.json(encoding="utf-8")
                        self.accounts = [{k:v for (k,v) in x.items()} for x in data['payload']['dashboard']]
                        self.acc_populate = False
                        return True
                    else:
                        print("Can't retrieve the accounts")
                        return False
                else:
                    return True
            print("Can't login...")
            return False

    async def hrequest(self, method, url):
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

    async def crequest(self, method, url):
        data = await self._request(method, url)
        if data:
            if (data["message"] == "Please login") or (data["message"] == "Required to set Profile"):
                print("Session expired..")
                login = await self.login()
                if login:
                    data = await self._request(method, url)
                    if data:
                        if data["message"] == "Success":
                            contacts = [{k:v for (k,v) in x.items() if k not in ['avatar', 'favorite', 'swift', 'correspondent_swift', 
                            'address', 'city', 'state', 'postcode', 'country', 'contact_type', 'merchant', 'created_at', 'updated_at', 
                            'deleted_at', 'bpay_vendor', 'domestic_bank_code', 'service_number', 'mobile_number', 'status', 'inputter', 
                            'owner', 'vendor', 'removable']} for x in data['payload']]
                            return contacts
                    else:
                        raise ClientError("ERROR: Unable to fetch contacts.")
                else:
                    raise HTTPException("Failed to login... Try again later.")
            if data["message"] == "Success":
                contacts = [{k:v for (k,v) in x.items() if k not in ['avatar', 'favorite', 'swift', 'correspondent_swift', 
                'address', 'city', 'state', 'postcode', 'country', 'contact_type', 'merchant', 'created_at', 'updated_at', 
                'deleted_at', 'bpay_vendor', 'domestic_bank_code', 'service_number', 'mobile_number', 'status', 'inputter', 
                'owner', 'vendor', 'removable']} for x in data['payload']]
                return contacts
        else:
            raise ClientError("ERROR: Unable to fetch contacts.")

    async def _request(self, method, url):
        async with self._session.request(method, f'{self.base_url}{url}') as resp:
            data = await resp.json(encoding="utf-8")
            return data

    async def close(self):
        await self._session.close()

    async def get_all_accounts(self):
        if self.acc_populate:
            await self.login()
        accounts = [{k:v for (k,v) in x.items() if k not in ['customer', 'account_type', 'product_code', 
        'product_group', 'primary_supplementary', 'secondary_customer', 'statecode', 'statuscode', 'actions', 
        'id', 'contact_type', 'success']} for x in self.accounts]
        if accounts:
            return accounts
        else:
            return None

    async def get_contacts(self):
        if self.acc_populate:
            await self.login()
        contacts = await self.crequest('GET', 'contacts')
        return contacts

    async def add_contact(self, foo:str=None, bar:str=None):
        if (not foo) or (not bar):
            raise MissingRequiredFields('Account number and Name is Required.')
        try:
            int(foo)
            account = foo
            alias = bar
        except:
            account = bar
            alias = foo
        if len(account) != 13:
            raise InvalidContent('Please Enter a valid account number.')
        duplicate = next((contact for contact in await self.get_contacts() if contact['account'] == account), None)
        if duplicate:
            raise DuplicateContent(f'The account {account} is already saved under the alias {duplicate["name"]}')
        data = {"contact_type": "IAT", "account": account, "alias": alias}
        async with self._session.post(f'{self.base_url}contacts', data=data) as r:
            r = await r.json(encoding="utf-8")
            if r["message"] == "Success":
                return r["payload"]
            else:
                raise ClientError("ERROR: Unable to fetch contacts. Try again later.")

    async def delete_contact(self, account=None):
        to_delete = None
        if not account:
            raise MissingRequiredFields("Contact's account (name or number or id) is a required argument")
        try:
            account = int(account)
            if len(str(account)) == 13:
                delete = next((contact for contact in await self.get_contacts() if contact['account'] == account), None)
                if delete:
                    to_delete = delete["id"]
            else:
                delete = next((contact for contact in await self.get_contacts() if contact['id'] == account), None)
                if delete:
                    to_delete = delete["id"]
        except:
            delete = next((contact for contact in await self.get_contacts() if contact['alias'] == account), None)
            if delete:
                to_delete = delete["id"]
        if to_delete is None:
            raise InvalidContent('Account not found in your contact list.')
        else:
            data = {"_method": "delete"}
            async with self._session.post(f'{self.base_url}contacts/{to_delete}', data=data) as r:
                r = await r.json(encoding="utf-8")
                if r["message"] == "Success":
                    return r["payload"]
                else:
                    raise ClientError("ERROR: Unable to delete the contact. Try again later.")


    async def get_history(self):
        history = {}
        if self.acc_populate:
            await self.login()
        for x in self.accounts:
            transactions = await self.hrequest('GET', f'account/{x["id"]}/history/today')
            if transactions and (len(transactions) > 0):
                history[x["account"]] = [
                    {"date": tr["narrative2"], "sender": tr["narrative3"], "amount": tr["amount"], "minus": tr["minus"], 
                    "balance": tr["balance"], "description": tr["description"]} for tr in transactions]
        if history == {}:
            return None
        else:
            return history
