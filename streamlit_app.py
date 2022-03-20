##############################
# Author: eeysirhc
# Date written: 2022-02-09
# Last updated: 2022-02-23
# Objective: bare bones streamlit app to visualize ErgoDEX liquidity pair prices
##############################

import streamlit as st
import pandas as pd
import altair as alt 


st.write(
"""
# ErgoDEX: token prices
""")

# LOAD DATA
token_prices = pd.read_csv("price-data.csv")
token_prices = token_prices[['timestamp', 'yx_ticker', 'yx_price', 'xy_ticker', 'xy_price']]

# RESHAPE DATA
token_prices_yx = token_prices[['timestamp', 'yx_ticker', 'yx_price']]
token_prices_yx = token_prices_yx.rename(columns={'yx_ticker': 'ticker', 'yx_price': 'price'})
token_prices_xy = token_prices[['timestamp', 'xy_ticker', 'xy_price']]
token_prices_xy = token_prices_xy.rename(columns={'xy_ticker': 'ticker', 'xy_price': 'price'})

token_final = pd.concat([token_prices_yx, token_prices_xy], axis=0)
token_final['timestamp'] = pd.to_datetime(token_final['timestamp'])


## CREATE LIST OF TICKER SELECTION
ticker_selector = token_final.sort_values(by='ticker')
ticker_selector = ticker_selector[ticker_selector['ticker'].notnull()]
ticker_selector = ticker_selector.ticker.unique()

user_selection = st.selectbox("", ticker_selector)

## GRAB MOST RECENT PRICE POINT
token_selection = token_final[token_final['ticker'] == user_selection]
token_selection = token_selection.sort_values('timestamp', ascending=True)
price_pair = token_selection['price'].iloc[-1]
price_pair = round(price_pair, 5)


# PLOT CONFIG
base = alt.Chart(token_selection).encode(
	alt.X('timestamp', axis=alt.Axis(title='Date')),
	alt.Y('price', axis=alt.Axis(title='Price')),
	tooltip=['timestamp', 'price'])

line = base.mark_line()
points = base.mark_point(filled=True, size=10)
chart = (line + points).interactive()

## PRICE
st.write('### Price: ', price_pair)

## FINAL GRAPH
st.altair_chart(chart, use_container_width=True)

try:
	with open("last_updated.txt", "r") as f:
		st.write("Last updated: " + f.read())
except:
	print("Last updated time file missing")

st.write(
"""
## To-Do
* Toggle to flip y-axis for certain pairs
* [ERGO Seed Phrase #8](https://www.reddit.com/r/ergonauts/comments/t2n8yj/the_15_days_of_ergo_seed_phrases/): "Don't _____ Be Happy"
""")





