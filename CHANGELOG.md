# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project mostly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html);

# v1.0.2
- No breaking changes

### Internal
- Adjusted `delay cut_off`
- Bug fix on `cleanup`

# v1.0.1
- No breaking changes

### Internal
- `transaction['date']` is now a timezone aware datetime object.
- encrypted password and username
- handles the internal eventloop crashes.
- `backing off` implemented: detects if you log in from another device and backs off.
- logging implemented
- prevents account locking up by stoping the services when credentials are wrong


# v1.0.0

## Added

- New feature: `event` added
  - use decorators
  ```py
  @bank.event('new_transaction')
	async def on_new_transaction(transaction):
    print(transaction)
  ```
  to be notified of the transactions.

- No breaking changes

# v0.1.5

### Internal
- `add_account` bug fix.
- errors module moved so it can be expected easily`aiobml.core.errors.Exception`.
  - These details can be used for error handlers and try / excepts for example:
  - `except aiobml.core.errors.HTTPException:`

# v0.1.4

## Added

- New feature: `get_contacts` coroutine added
  - Will return a list of all your contacts.
- New feature: `add_contact` coroutine added
  - add a new account to your contact list.

# v0.1.3

## Added

- New feature: `delete_contact` coroutine added
  - delete a contact from your contact list.

# v0.1.2

## Added

- `get_accounts` coroutine added to get the details of all your accounts.

### Internal

- Extra details of the accounts loaded into memory.
  - These details will be used in the future to do transactions using this library.
  - Everything else still works the same.

# v0.1.1

### Internal

- `http session` now more gracefully handles expired sessions.
  - No longer raises `HTTPException` exception when session is expired.
