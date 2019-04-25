# Real-Time Stock Ticker

Implementation of a live stock ticker which generates random stock prices.
An event driven architecture is used, which means that data is communicated from the back-end to the front-end as soon as an event occurs.
This event can either be a change in stock prices, or the detection of a V-pattern (an increase followed by a decrease) for any given stock.
Pattern detection is signalled by a flashing blue dot appearing next to the stock symbol.
Weather data is also displayed, however, this data comes from reading a JSON file.

## Installation

- Clone the repository and create a virtual environment using 'requirements.txt'.
- Run `python app.py`.
- In the browser, go to `localhost:5000`


## Output

![](https://i.imgur.com/W2BgCFA.gif)


#### Code Details

- Development stack:
  - Backend     : Python (3.7), Flask, SocketIO
  - Frontend    : HTML, CSS, JavaScript (with jQuery)