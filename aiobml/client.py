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
import asyncio
from .aiobmlcore.http import HTTPSession


class asyncBML():
    def __init__(self, *, loop=None, username=None, password=None):
        loop = loop or asyncio.get_event_loop()
        self.http = HTTPSession(loop=loop, username=username, password=password)

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
