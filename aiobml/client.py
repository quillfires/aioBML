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
__version__ = "1.0.1"
import asyncio
from asyncio import ensure_future, Future, iscoroutine
from collections import defaultdict, OrderedDict
from threading import Lock
import logging
import sys

from .core.http import HTTPSession
from .core.errors import *
logging.basicConfig(level=logging.INFO)

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        logging.error("Windows Proactor Event Loop Policy not found", exc_info=True)

class asyncBML():
    def __init__(self, *, loop=None, username=None, password=None):
        loop = loop or asyncio.get_event_loop()
        self.logger = logging.getLogger('aiobml')
        self.logger.setLevel(logging.INFO)
        self.http = HTTPSession(loop=loop, username=username, password=password, logger=self.logger)
        self.username = ''.join(chr(ord(c) + ord(self.http.vathuodi[i % len(self.http.vathuodi)]) - ord('0')) for i, c in enumerate(username))
        self.password = ''.join(chr(ord(c) + ord(self.http.vathuodi[i % len(self.http.vathuodi)]) - ord('0')) for i, c in enumerate(password))
        self._events = defaultdict(OrderedDict)
        self.transactions = []
        self._loop = loop
        self._lock = Lock()
        self.logger.info(" █████╗ ██╗ ██████╗ ██████╗ ███╗   ███╗██╗     ")
        self.logger.info("██╔══██╗██║██╔═══██╗██╔══██╗████╗ ████║██║     ")
        self.logger.info("███████║██║██║   ██║██████╔╝██╔████╔██║██║     ")
        self.logger.info("██╔══██║██║██║   ██║██╔══██╗██║╚██╔╝██║██║     ")
        self.logger.info("██║  ██║██║╚██████╔╝██████╔╝██║ ╚═╝ ██║███████╗")
        self.logger.info("╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝")
        self.logger.info('an asynchronous Python wrapper around the Bank of Maldives API')   
        self.logger.info("Author: Ali Fayaz (Quill) (quillfires)")
        self.logger.info("Version: v%s", __version__)
        self.logger.info('copyright (c) 2020-present Ali Fayaz (Quill) (quillfires)')
        self.logger.info('Starting BML client...')   


    async def close(self):
        """|coro|
        Clear the session

        """
        await self.http.close()

    async def get_accounts(self):
        """|coro|

        Method which retrieves all the accounts.

        Returns
        ---------
        list: accounts
            a list of disctionary objects containing all the accounts.
            [{account1}, {account2}, {account3}]
        """
        data = await self.http.get_all_accounts()
        return data

    def event(self, event, f=None):
        """Registers the function ``f`` to the event name ``event``.
        If ``f`` isn't provided, this method returns a function that
        takes ``f`` as a callback; in other words, you can use this method
        as a decorator, like so:
            @bank.event('new_transaction')
            async def data_handler(data):
                print(data)
        In both the decorated and undecorated forms, the event handler is
        returned. The upshot of this is that you can call decorated handlers
        directly

        Note
        --------
        Will fire all the transactions within 24 hrs at the app reboot.
        Use a db to make sure that you arnt notified of the same transaction.
        """
        def _on(f):
            self._add_event_handler(event, f, f)
            return f
        if f is None:
            return _on
        else:
            return _on(f)

    def _add_event_handler(self, event, k, v):
        self.emit('new_listener', event, k)
        with self._lock:
            self._events[event][k] = v

    def _emit_handle_potential_error(self, event, error):
        if event == 'error':
            if error:
                self.logger.error(error)
                raise error
            else:
                self.logger.error('Unknown error')
                raise ClientError("Uncaught, unspecified 'error' event.")

    def _call_handlers(self, event, args, kwargs):
        handled = False
        with self._lock:
            funcs = list(self._events[event].values())
        for f in funcs:
            self._emit_run(f, args, kwargs)
            handled = True
        return handled

    def emit(self, event, *args, **kwargs):
        handled = self._call_handlers(event, args, kwargs)
        if not handled:
            self._emit_handle_potential_error(event, args[0] if args else None)
        return handled

    def _emit_run(self, f, args, kwargs):
        try:
            coro = f(*args, **kwargs)
        except Exception as exc:
            self.emit('error', exc)
        else:
            if iscoroutine(coro):
                if self._loop:
                    f = ensure_future(coro, loop=self._loop)
                else:
                    f = ensure_future(coro)
            elif isinstance(coro, Future):
                f = coro
            else:
                f = None

            if f:
                @f.add_done_callback
                def _callback(f):
                    if f.cancelled():
                        return

                    exc = f.exception()
                    if exc:
                        self.emit('error', exc)

    async def get_contacts(self):
        """|coro|

        Method which retrieves all the contacts.

        Returns
        ---------
        list: contacts
            a list of disctionary objects containing all the details for each contacts.
            [{contact1}, {contact2}, {contact3}]

        Raises
        --------
        ClientError
            Bad request while fetching contacts.
        HTTPException
            Failed to login.
        """
        data = await self.http.get_contacts()
        return data
    
    async def add_contact(self, name=None, account=None):
        """|coro|

        Method to add a contact.

        Returns
        ---------
        dict: contact
            a dictionary object of the added contact
            {contact}

        Raises
        --------
        MissingRequiredFields
            Missing a required field (account number or name).
        InvalidContent
            Invalid account number.
        ClientError
            Bad request while fetching contacts.
        HTTPException
            Failed to login.
        DuplicateContent
            Account number is already saved in your contacts.
            Along with the error message it will print 
            the name of the duplicate.
        """
        data = await self.http.add_contact(name, account)
        return data

    async def delete_contact(self, account=None):
        """|coro|

        Method to delete a contact.

        Returns
        ---------
        str: notice
            'Contact removed successfully'

        Raises
        --------
        MissingRequiredFields
            Missing the contact details (account number or name or id).
        InvalidContent
            Contact is not found in your list of contacts.
        ClientError
            Bad request while deleting contact.
        HTTPException
            Failed to login.
        """
        data = await self.http.delete_contact(account)
        return data

    async def get_history(self) -> dict:
        """|coro|

        Method which retrieves the account history.

        Returns
        ---------
        dict: transactions
            Dictionary object containing transactions relating to each account.
            {account1:{[{transaction1},{transaction2}]},account2:{[{transaction1},{transaction2}]},}

            transaction:
            {'date': 'date', 'sender': 'sender', 'amount': 'amount', 'minus': True/False, 'balance': 'uncleared amount', 
            'description': 'Type of transaction'}

        Raises
        --------
        HTTPException
            Bad request while fetching transactions.
        """
        data = await self.http.get_history()
        return data

    async def start(self):
        """|coro|
        An asynchronous call which starts the BML event loop.
        listen for new transactions using a decorator like:
        @aiobmlclient.event('new_transaction')
            async def data_handler(data):
                print(data)

        Note
        --------
        Will fire all the transactions within last 24hrs at the app reboot.
        Use a db to make sure that you arnt notified of the same transaction.
        """
        self.logger.info('Listenig for new transactions...')
        while True:
            try:
                history = await self.http.get_history()
                if history:
                    for accounts in history:
                        for transaction in history[accounts]:
                            transaction.pop('balance')
                            if (transaction not in self.transactions):
                                self.emit('new_transaction', transaction)
                                self.transactions.append(transaction)
                
            except (Unauthorized, KeyboardInterrupt, SystemExit) as e:
                self.logger.info('Stopping services...')
                await self.http.close()
                if isinstance(e, Unauthorized):
                    self.logger.error('Confirm your credentials and try again.')
                self.logger.info('Exiting...')
                return sys.exit(1)
            await asyncio.sleep(30)
