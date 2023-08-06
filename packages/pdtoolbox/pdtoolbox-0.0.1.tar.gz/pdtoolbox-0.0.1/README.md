# tradingtools
Basic trading tools used repeatedly in algo trading applications. Setting as a package enables imports to be performed.

`pip install git+https://github.com/pedrostanton/toolbox.git`

## functions
| Function                  | Description                                                                                  |
|---------------------------|----------------------------------------------------------------------------------------------|
| min_increments            | function to get and return the number of decimal places a product quotes at or base min size |
|get_min_increments         | function to get and return all the minimum increasements for all products on an exchange     |
|exchange_connections       | function to get and return authorised client logins for trading exchanges|

## classes
| Class    | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| Consumer | class to connect to rabbit mq and start consuming from an exchange or queue |



