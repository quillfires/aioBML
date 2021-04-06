# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project mostly adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html);

# v0.1.2

### Internal

- Extra details of the accounts loaded into memory.
  - These details will be used in the future to do transactions using this library.
  - Everything else still works the same.

- `get_accounts` coroutine added to get the details of all your accounts.

# v0.1.1

### Internal

- `http session` now more gracefully handles expired sessions.
  - No longer raises `HTTPException` exception when session is expired.
