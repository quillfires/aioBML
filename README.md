[![Python Version](https://img.shields.io/badge/Python-3.7%20%7C%203.8%20%7C%203.9-blue.svg)](https://www.python.org)  [![LICENSE](https://img.shields.io/github/license/quillfires/aioBML.svg)](LICENSE)  [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/quillfires/aioBML/issues)

This is an asynchronous Python wrapper around the Bank of Maldives API. This repo is an async version built using [bml_notifier](https://github.com/Dharisd/bml_notifier) and [bml-transactions](https://github.com/baraveli/bml-transactions) as a reference. 

# How it works

Its a simple asynchronous Python API wrapper that returns the transaction history of all your accounts from the Bank of Maldives web API. If you want to check for new transactions, save the transactions to a db, check and add any transactions that's not currently saved to the db.

# setup
You must have python 3 installed

### using PIP

```$ pip install -U aiobml```

### From Source

```$ git clone https://github.com/quillfires/aioBML.git```

```$ cd aiobml```

```$ python setup.py install```

### Basic Example

```python
import asyncio

from aiobml import asyncBML

loop = asyncio.get_event_loop()
bank = asyncBML(username="your_user_name",password="your_password")

async def main():
    while True:
        history = await bank.get_history()
        if history:
            for accounts in history:
                for transaction in history[accounts]:
                    print(transaction)
                    #check if it is in your db
                    # if not, save to db and alert about the transaction
        await asyncio.sleep(30) #30 seconds later check again


if __name__ == '__main__':
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.run_until_complete(bank.close())
```
