# Currency Exchange Rate Utility

This console utility retrieves the exchange rates of EUR and USD from PrivatBank's public API for the past specified days. The API archive stores data for the last 4 years.

## Usage

To run the utility, execute the following command in your terminal:

```bash
python3 main.py <number_of_days>
```
Replace <number_of_days> with the desired number of days to retrieve exchange rates (not exceeding 10 days).

### Example

```bash
python3 main.py 2
```
## Result

The program will display the exchange rates of EUR and USD for the specified number of days in the following format:

```bash
[
  {
    '03.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  },
  {
    '02.11.2022': {
      'EUR': {
        'sale': 39.4,
        'purchase': 38.4
      },
      'USD': {
        'sale': 39.9,
        'purchase': 39.4
      }
    }
  }
]
```
## Additional Features

Additional Currencies: You can specify additional currencies using command-line parameters to include them in the program's response.
### Example:
```bash
python3 main.py 2 UAH
```

WebSocket Chat Integration: The utility includes a WebSocket chat with the ability to input the "exchange" command. It displays the current currency exchange rates in the chat.
### Example:
```bash
exchange
```
Extended Exchange Command: You can use the extended "exchange" command to view currency exchange rates in the chat for the last few days.
### Example:
```bash
exchange 2
```
Logging to File: The utility logs the execution of the "exchange" command in the chat to a file using aiofile and aiopath.
### Example:
```bash
exchange
```
Log File: exchange_log.txt
For any issues or errors, the utility provides appropriate error handling for network requests.
