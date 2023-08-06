## Introduction
A GPG based file lock.

## Usage

### Install

`pip install gpglock`

### Setup

1. `gpginit target_dir`
2. Add files which need to be locked into the `.gpglock` in `target_dir`

### Lock/Unlock
- `gpglock target_dir`
- `gpgunlock target_dir`

If `target_dir` is not provided, the current working directory will be used. 

## GPG Configuration
- Make sure the key is imported correctly.
- Make sure the key is trusted, otherwise you might see `Invalid Recipient` error.
- Run `gpg --list-secret-keys` to check the keys.
