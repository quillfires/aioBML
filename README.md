This is an asynchronous Python wrapper around the Bank of Maldives API. 

# How it works

Its a simple asynchronous Python wrapper around the BML API. Currently you can use this library to get the transaction history of all your Bank of Maldives accounts, details of all you BML accounts & contacts and add & remove contacts. If you want to check for new transactions; save the transactions to a db, check, alert and add any transactions that's not currently saved to the db *check the basic example below*.

# Async BML API
[![Python Version](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://www.python.org)  [![aiobml · PyPI](https://img.shields.io/pypi/v/aiobml.svg?color=4CBB17)](https://pypi.python.org/pypi/aiobml/)  [![PyPI - Status](https://img.shields.io/pypi/status/aiobml)](https://pypi.python.org/pypi/aiobml/)  [![Maintenance](https://img.shields.io/maintenance/yes/2021)](https://pypi.python.org/pypi/aiobml/)  [![LICENSE](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[![ViewCount](https://views.whatilearened.today/views/github/quillfires/aioBML.svg)](https://views.whatilearened.today/views/github/quillfires/aioBML.svg)  [![GitHub forks](https://img.shields.io/github/forks/quillfires/aioBML)](https://github.com/quillfires/aioBML/network)  [![GitHub stars](https://img.shields.io/github/stars/quillfires/aioBML.svg?color=ffd40c)](https://github.com/quillfires/aioBML/stargazers)  [![PyPI - Downloads](https://img.shields.io/pypi/dm/aiobml?color=orange&label=PIP%20-%20Installs)](https://pypi.python.org/pypi/aiobml/) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/quillfires/aioBML/issues)  [![GitHub issues](https://img.shields.io/github/issues/quillfires/aioBML.svg?color=808080)](https://github.com/quillfires/aioBML/issues)  

This library is not fully completed yet. As of now it can be used to get the transactions done within the last 24 - 48 hours, get all the information about your Accounts and your contacts and add & remove contacts. *scroll to the end to see the to do list of this library*

# setup
You must have python 3 installed

### using PIP

```$ pip install -U aiobml```

### From Source

```$ git clone https://github.com/quillfires/aioBML.git```

```$ cd aioBML```

```$ python setup.py install```

# Basic Example

```python
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
```

# Changlog
[See the change log here](https://github.com/quillfires/aioBML/blob/development/CHANGELOG.md)

## Todo

- [x] Get todays history
- [x] Get Account details
- [x] Get contacts
- [x] Add contacts
- [x] Delete contacts
- [ ] Get history from a date range
- [ ] Make Transfer to a given account number
- [ ] Make transfers to contacts.