/***************************
Author: eeysirhc
Date written: 2022-02-09
Last updated: 2022-03-18
Objective: pull all liquidity pair pricing over time
***************************/

CREATE OR REPLACE VIEW price_data AS

with data_pools as 
(select pool_state_id, pool_id, x_id, x_amount, y_id, y_amount, gindex 
from pools),

data_time as 
(select pool_id, pool_state_id, p2pk, to_timestamp(timestamp/1000) as timestamp, 'deposit' as segment
from deposits 
union all 
select pool_id, pool_state_id, p2pk, to_timestamp(timestamp/1000) as timestamp, 'redeem' as segment
from redeems
union all 
select pool_id, pool_state_id, p2pk, to_timestamp(timestamp/1000) as timestamp, 'swap' as segment 
from swaps)

select dp.pool_state_id, 
dp.pool_id, 
dp.x_id, 
a_x.ticker as x_ticker, 
dp.x_amount/power(10,a_x.decimals) as x_amount,
dp.y_id, 
a_y.ticker as y_ticker, 
dp.y_amount/power(10,a_y.decimals) as y_amount,
a_y.ticker || '/' || a_x.ticker as yx_ticker,
(dp.y_amount/POWER(10,a_y.decimals))/(dp.x_amount/POWER(10,a_x.decimals)) as yx_price,
a_x.ticker || '/' || a_y.ticker as xy_ticker,
(dp.x_amount/POWER(10,a_x.decimals))/(dp.y_amount/POWER(10,a_y.decimals)) as xy_price,
dp.gindex, 
dt.timestamp,
dt.segment,
dt.p2pk as address 
from data_pools dp 
join data_time dt on dt.pool_id = dp.pool_id and dt.pool_state_id = dp.pool_state_id 
LEFT JOIN assets a_x ON a_x.id = dp.x_id
LEFT JOIN assets a_y ON a_y.id = dp.y_id

/* erg/sigusd: remove bug data */
WHERE gindex NOT IN (12981672,12979979) 

/* remove outdated tickers */
AND a_x.ticker NOT IN ('WT_ERG', 'WT_ADA', 'xyzpad')
AND a_y.ticker NOT IN ('WT_ERG', 'WT_ADA', 'xyzpad')


;

