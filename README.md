This is an asynchronous Python Bank of Maldives API wrapper. This repo is an async version built using [bml_notifier](https://github.com/Dharisd/bml_notifier) as a reference. 

# How it works

Its a simple asynchronous Python API wrapper that returns the transaction history of all your accounts from the Bank of Maldives web API. If you want to check for new transactions, save the transactions to a db, check and add any transactions that's not currently saved to the db.

# setup
You must have python 3 installed

### using PIP

```$ pip install -U aiobml```

### From Source

```$ git clone https://github.com/quillfires/aiobml.git```

```$ cd aiobml```

```$ python setup.py install```

### Basic Example

```python
import asyncio

from client import asyncBML

loop = asyncio.get_event_loop()
myaccount = asyncBML(username="your user name",password="your password")

async def main():
    while True:
        data = await myaccount.get_history()
        for accounts in data:
            for transaction in accounts:
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
        loop.run_until_complete(myaccount.close())
```