-- select all stocks traded in last 7 days
SELECT * FROM stocks_real_time srt
WHERE time > (now() - INTERVAL '7 days');

-- select top 10 lastest stocks traded order by hightest price
SELECT * FROM stocks_real_time srt
ORDER BY time DESC, price DESC
LIMIT 10;

-- average trading price of stock for last 5 days
SELECT c.name, avg(price) AVG_PRICE
FROM stocks_real_time srt
	JOIN company c 
		ON srt.symbol  = c.symbol 
WHERE c.name like 'App%' and time > (now() - INTERVAL '5 days')
GROUP BY c.name ;

-- first and last price for last 5 days
select symbol, first (price, time) FIRST_PRICE, last (price, time) LAST_PRICE
FROM stocks_real_time srt
WHERE time > (now() - INTERVAL '5 days')
GROUP BY symbol ;


-- time bucket
SELECT
	time_bucket('1 day', time) AS trading_day,
    symbol,
	first(price, time) AS opening_price,
	last(price, time) AS closing_price,
	min(price) AS lowest_price,
	max(price) AS highest_price,
	avg(day_volume) average_volume
FROM stocks_real_time srt
WHERE time > (now() - INTERVAL '2 weeks') 
		and symbol in  ('AAPL', 'AMZN', 'GOOG', 'NVDA')
GROUP BY trading_day, symbol
ORDER BY trading_day, symbol;

