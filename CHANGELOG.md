# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project mostly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html);

# v0.1.3

## Added

- New feature: `get_contacts` coroutine added
  - Will return a list of all your contacts.
- New feature: `add_contact` coroutine added
  - add a new account to your contact list.
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
