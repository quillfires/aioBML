"""
MIT License

Copyright (c) 2021-present Ali Fayaz (Quill) (quillfires)

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
import random
import string
import datetime
import time
import asyncio

from .errors import *


class HTTPSession:

    def __init__(self, loop, **attrs):
        self.vathuodi = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
        username = attrs.get('username', None)
        password = attrs.get('password', None)
        self.logger = attrs.get('logger', None)
        self.base_url = 'https://www.bankofmaldives.com.mv/internetbanking/api/'
        if username and password:
            self.login_params = {"username": ''.join(chr(ord(c) + ord(self.vathuodi[i % len(self.vathuodi)]) - ord('0')) for i, c in enumerate(username)), "password": ''.join(chr(ord(c) + ord(self.vathuodi[i % len(self.vathuodi)]) - ord('0')) for i, c in enumerate(password))}
        else:
            self.login_params = None
        self.accounts = []
        self.contacts = None
        self.acc_populate = True
        if not self.login_params:
            self.logger.error("Unable to login, username and/or password not given")
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
        self.back_off = type('Back_off',(), {'__init__': self.back_off_init, 'delay': self.delay})()

    
    def back_off_init(self, begin=30, *, vary=False):
        self._begin = begin
        self._try = 0
        self._cut_off = 10
        self._reset_time = begin * 2 ** 11
        self._last_active = time.monotonic()
        bucket = random.Random()
        bucket.seed()
        self.duration = bucket.randrange if vary else bucket.uniform

    
    def delay(self):
        now = time.monotonic()
        duratino = now - self._last_active
        self._last_active = now
        if duratino > self._reset_time:
            self._try = 0
        self._try = min(self._try + 1, self._cut_off)
        return self.duration(40, self._begin * 2 ** self._try)


    async def login(self):
        if not self.login_params:
            self.logger.error("Unable to login, username and/or password missing")
            raise Unauthorized("Unable to login, username and/or password missing")
        self.logger.info("Logging in...")
        await self._session.post(f"{self.base_url}login", data={"username": ''.join(chr(ord(c) - ord(self.vathuodi[i % len(self.vathuodi)]) + ord('0')) for i, c in enumerate(self.login_params['username'])), 
        "password": ''.join(chr(ord(c) - ord(self.vathuodi[i % len(self.vathuodi)]) + ord('0')) for i, c in enumerate(self.login_params['password']))})
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
                        self.logger.error("Unable to login, unable to get account details")
                        return False
                else:
                    return True
            self.logger.error("Unable to login")
            self.logger.warning("Invalid username and/or password...")
            self.logger.warning("or Bank of Maldives has locked and changed your password... (happens when too many attempts were made with wrong password)")
            self.logger.warning("In which case reset your password by login in via browser to Bank of Maldives Internet banking website to continue using this API")
            raise Unauthorized("Invalid username and/or password...")


    async def hrequest(self, method, url):
        data = await self._request(method, url)
        if data:
            if (data["message"] == "Please login") or (data["message"] == "Required to set Profile"):
                retry = self.back_off.delay()
                self.logger.info(f"Login detected, backing off... restarting in {retry} seconds...")
                await asyncio.sleep(retry)
                login = await self.login()
                if login:
                    await self.hrequest(method, url)
                else:
                    self.logger.error("Unable to login... Trying again...")
                    return None
            if data["message"] == "Success":
                transactions = data["payload"]["history"]
                return transactions
        else:
            self.logger.error("Unable to retrieve transactions")
            return None


    async def crequest(self, method, url):
        data = await self._request(method, url)
        if data:
            if (data["message"] == "Please login") or (data["message"] == "Required to set Profile"):
                retry = self.back_off.delay()
                self.logger.info(f"Login detected, backing off... retrying in {retry} seconds...")
                await asyncio.sleep(retry)
                login = await self.login()
                if login:
                    await self.crequest(method, url)
                else:
                    self.logger.error("Unable to login... Try again later...")
                    raise HTTPException("Failed to login... Try again later.")
            if data["message"] == "Success":
                self.contacts = [{k:v for (k,v) in x.items()} for x in data['payload']]
                return self.contacts
        else:
            self.logger.error("Unable to retrieve contacts")
            raise ClientError("ERROR: Unable to fetch contacts.")


    async def _request(self, method, url):
        async with self._session.request(method, f'{self.base_url}{url}') as resp:
            data = await resp.json(encoding="utf-8")
            return data


    async def close(self):
        self.logger.info("Closing session...")
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
        if not self.contacts:
            contacts = await self.crequest('GET', 'contacts')
        else:
            contacts = self.contacts
        contacts = [{k:v for (k,v) in x.items() if k not in ['avatar', 'favorite', 'swift', 'correspondent_swift', 
                    'address', 'city', 'state', 'postcode', 'country', 'contact_type', 'merchant', 'created_at', 'updated_at', 
                    'deleted_at', 'bpay_vendor', 'domestic_bank_code', 'service_number', 'mobile_number', 'status', 'inputter', 
                    'owner', 'vendor', 'removable']} for x in contacts]
        return contacts


    async def add_contact(self, foo:str=None, bar:str=None):
        if (not foo) or (not bar):
            self.logger.error("Unable to add contact, missing required fields")
            raise MissingRequiredFields('Account number and Name is Required.')
        try:
            int(foo)
            account = foo
            alias = bar
        except:
            account = bar
            alias = foo
        if len(account) != 13:
            self.logger.error("Unable to add contact, invalid account number")
            raise InvalidContent('Please Enter a valid account number.')
        duplicate = next((contact for contact in await self.get_contacts() if contact['account'] == account), None)
        if duplicate:
            self.logger.error(f"Unable to add contact, duplicate {account} number")
            raise DuplicateContent(f'The account {account} is already saved under the alias {duplicate["alias"]}')
        data = {"contact_type": "IAT", "account": account, "alias": alias}
        async with self._session.post(f'{self.base_url}contacts', data=data) as r:
            r = await r.json(encoding="utf-8")
            if r["message"] == "Success":
                return r["payload"]
            else:
                self.logger.error(f"Unable to add contact, {r['message']}")
                raise ClientError("ERROR: Unable to add contact. Try again later.")


    async def delete_contact(self, account=None):
        to_delete = None
        if not account:
            self.logger.error("Unable to delete contact, missing required fields")
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
            self.logger.error(f"Unable to delete contact, {account} not found")
            raise InvalidContent('Account not found in your contact list.')
        else:
            data = {"_method": "delete"}
            async with self._session.post(f'{self.base_url}contacts/{to_delete}', data=data) as r:
                r = await r.json(encoding="utf-8")
                if r["message"] == "Success":
                    return r["payload"]
                else:
                    self.logger.error(f"Unable to delete contact, {r['message']}")
                    raise ClientError("ERROR: Unable to delete the contact. Try again later.")


    async def get_history(self):
        history = {}
        if self.acc_populate:
            await self.login()
        for x in self.accounts:
            transactions = await self.hrequest('GET', f'account/{x["id"]}/history/today')
            if transactions and (len(transactions) > 0):
                def clean_up(transactions):
                    for transaction in transactions:
                        transaction['sender'] =  transaction["narrative3"]
                        transaction['receiver'] = transaction["account"]
                        if transaction['sender'] == '':
                            transaction['sender'] = transaction['account']
                            transaction['receiver'] = transaction['bookingDate']
                        transaction['date'] = datetime.datetime.now(datetime.timezone.utc)
                    return transactions
                history[x["account"]] =[{k:v for (k,v) in tr.items()} for tr in clean_up(transactions)]
        if history == {}:
            return None
        else:
            return history
