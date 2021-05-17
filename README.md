# BestBuy Bot

This bot allows a user to buy a single item quickly from bestbuy.com using selenium.

## Installation

Use pip to install requirements.txt.

```bash
pip install -r requirements.txt
```

## Usage

Run the script with

```bash
python bot.py
```

Don't forget to update config.ini with your information.

* Card number `4485285007878617` satisfies Luhn's algorithm for testing without actually buying.
* Keep same format for expiration month and year.

## TODO

- [ ] Add support for queue system (GPUs)
- [ ] Automatically buy item given notification (new GPUs)
- [ ] Choose store to pick up at (default: closest store)

## License

[MIT](https://choosealicense.com/licenses/mit/)

