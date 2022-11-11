-- Create regular Postgres table to hold timeseries data
create table stocks_real_time (
	time TIMESTAMPTZ not null,
	symbol TEXT not null,
	price DOUBLE precision null,
	day_volume INT null
);

-- Create Hyper Table in TimescaleDB
select create_hypertable('stocks_real_time', 'time');

-- Create index
create index ix_symbol_time on stocks_real_time (symbol, time DESC);

-- Create reference table
create table company (
	symbol text not null,
	name text not null
);
