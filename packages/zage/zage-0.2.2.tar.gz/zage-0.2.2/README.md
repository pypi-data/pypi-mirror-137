# Official Zage Bindings for Python

A Python library for Zage's API.

## Installation

You can install this package using pip:

```sh
python -m pip install zage
```

## Usage

This library must be initialized by specifying your credentials for the desired environment (sandbox or prod).

This is as simple as setting `zage.public_key` and `zage.private_key` to the requisite values before making an API call:

```python
import zage

zage.public_key = "test_..."
zage.secret_key = "test_..."

# create a payment token
payment_token = zage.Payments.create_token(
    amount=1000, # in cents
    webhook="https://zage.app/on_success",
    metadata={},
)

print(payment_token)

```
