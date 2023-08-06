# whop-python-sdk

## Installation
```
pip install whop
```

## Usage
```
from whop.whop import Whop

bearer = "<Bearer Token>"
client = Whop(bearer)

# Create a password protected link for your product.
client.create_link(
    product_id=123,
    password="secretpassword"
    stock=10
)

# Retrieve all links.
resp = client.get_links()
print(resp)
```