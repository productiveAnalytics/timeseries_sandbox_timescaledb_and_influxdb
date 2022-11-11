-- continuous aggregagted materialized view
CREATE MATERIALIZED VIEW stocks_candlestick_daily
WITH (timescaledb.continuous) 
AS
SELECT
	time_bucket('1 day', time) AS trading_day,
    symbol,
	first(price, time) AS opening_price,
	last(price, time) AS closing_price,
	min(price) AS lowest_price,
	max(price) AS highest_price,
	avg(day_volume) average_volume
FROM stocks_real_time srt
GROUP BY trading_day, symbol;

-- query the materialized view
SELECT * FROM stocks_candlestick_daily
WHERE symbol in  ('AAPL', 'AMZN', 'GOOG', 'NVDA')
ORDER BY trading_day, symbol;

-- Setup automatic schedule for Continuous Aggregate
SELECT add_continuous_aggregate_policy(
	'stocks_candlestick_daily',
	start_offset => INTERVAL '3 days',			-- for last 3 days
	end_offset => INTERVAL '1 hour',			-- 1 hour from now
	schedule_interval => INTERVAL '1 days'		-- daily
);


-- ONETIME refresh
CALL refresh_continuous_aggregate(
	'stocks_candlestick_daily',
	now() - INTERVAL '1 week',
	now()
);
