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

from aiobml import asyncBML

loop = asyncio.get_event_loop()
bank = asyncBML(username="your_user_name",password="your_password")

async def main():
    await bank.start()

@bank.event('new_transaction')
async def on_new_transaction(transaction):
    print(transaction)
    # on app reboot, event will trigger for all the transactions within 24 hours
    # Use a db to avoid being notified of the same transaction.
    # check if transaction is in your db
    # if not, save to db and alert about the transaction

async def contacts():
    data = await bank.get_contacts()
    print(data)
    # show all the contacts you have saved

async def accounts():
    data = await bank.get_accounts()
    print(data)
    # show all the accounts you have in Bank of Maldives

async def add_cont(account, name):
    added_acc = await bank.add_contact(account, name)
    print(added_acc)
    # adds the account your contact list
    # throws DuplicateContent error if it is already in the contact list

async def delete_cont(account):
    await bank.delete_contact(account)
    # deletes the first match from your contact list
    # account can be the account number or the saved name

if __name__ == '__main__':
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(bank.close())
