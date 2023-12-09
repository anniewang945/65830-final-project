create table gated_station_entries
(
    service_date  TEXT,
    time          TEXT,
    station_id    TEXT,
    line_id       TEXT,
    gated_entries REAL,
    primary key (service_date, time, station_id, line_id)
);

create table lines
(
    line_id   TEXT
        primary key,
    line_name TEXT
);

create table rail_ridership
(
    season              TEXT,
    line_id             TEXT,
    direction           INTEGER,
    time_period_id      TEXT,
    station_id          TEXT,
    total_ons           INTEGER,
    total_offs          INTEGER,
    number_service_days INTEGER,
    average_ons         INTEGER,
    average_offs        INTEGER,
    average_flow        INTEGER,
    primary key (season, line_id, direction, time_period_id, station_id)
);

create table routes
(
    route_id         INTEGER
        primary key,
    line_id          TEXT,
    first_station_id TEXT,
    last_station_id  TEXT,
    direction        INTEGER,
    direction_desc   TEXT,
    route_name       TEXT
);

create table sqlite_master
(
    type     TEXT,
    name     TEXT,
    tbl_name TEXT,
    rootpage INT,
    sql      TEXT
);

create table station_orders
(
    route_id                         INTEGER,
    station_id                       TEXT,
    stop_order                       INTEGER,
    distance_from_last_station_miles REAL,
    primary key (route_id, station_id)
);

create table stations
(
    station_id   TEXT
        primary key,
    station_name TEXT
);

create table time_periods
(
    time_period_id    TEXT
        primary key,
    day_type          TEXT,
    time_period       TEXT,
    period_start_time TEXT,
    period_end_time   TEXT
);

