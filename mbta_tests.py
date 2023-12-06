system_knowledge = """Given the following SQL tables, your job is to write queries given a user’s request.
CREATE TABLE routes (
  route_id INTEGER,
  line_id TEXT,
  first_station_id TEXT,
  last_station_id TEXT,
  direction INTEGER,
  direction_desc TEXT,
  route_name TEXT,
  PRIMARY KEY (route_id)
);
CREATE TABLE gated_station_entries (
  service_date TEXT,
  time TEXT,
  station_id TEXT,
  line_id TEXT,
  gated_entries REAL,
  PRIMARY KEY (service_date, time, station_id, line_id)
);
CREATE TABLE lines (
  line_id TEXT,
  line_name TEXT,
  PRIMARY KEY (line_id)
);
CREATE TABLE stations (
  station_id TEXT,
  station_name TEXT,
  PRIMARY KEY (station_id)
);
CREATE TABLE station_orders (
  route_id INTEGER,
  station_id TEXT,
  stop_order INTEGER,
  distance_from_last_station_miles REAL,
  PRIMARY KEY (route_id, station_id)
);
CREATE TABLE rail_ridership (
  season TEXT,
  line_id TEXT,
  direction INTEGER,
  time_period_id TEXT,
  station_id TEXT,
  total_ons INTEGER,
  total_offs INTEGER,
  number_service_days INTEGER,
  average_ons INTEGER,
  average_offs INTEGER,
  average_flow INTEGER,
  PRIMARY KEY (season, line_id, direction, time_period_id, station_id)
);
CREATE TABLE time_periods (
  time_period_id TEXT,
  day_type TEXT,
  time_period TEXT,
  period_start_time TEXT,
  period_end_time TEXT,
  PRIMARY KEY (time_period_id)
);
"""

with open("queries.txt", "r") as f:
    user_prompts = f.read().split("```")

target_queries = []

# Q1
target_queries.append(
    """SELECT station_id, route_id, distance_from_last_station_miles
FROM station_orders
WHERE distance_from_last_station_miles >= 1
ORDER BY distance_from_last_station_miles DESC, route_id, station_id;"""
)

# Q2
target_queries.append(
    """SELECT line_name, direction_desc, x.station_name, y.station_name
FROM routes JOIN lines ON routes.line_id = lines.line_id
JOIN stations x
ON x.station_id = first_station_id
JOIN stations y
ON y.station_id = last_station_id
ORDER BY line_name, direction_desc, x.station_name, y.station_name;"""
)

# Q3
target_queries.append(
    """WITH tp_ids AS (
    SELECT time_period_id FROM time_periods
    WHERE day_type = 'weekday' AND period_start_time = '16:00:00'
    AND period_end_time = '18:29:59'
),
mit_station_ids AS (
    SELECT station_id FROM stations
    WHERE station_name = 'Kendall/MIT'
)
SELECT season, line_id, direction, total_ons
FROM rail_ridership
JOIN tp_ids
ON rail_ridership.time_period_id = tp_ids.time_period_id
JOIN mit_station_ids
ON rail_ridership.station_id = mit_station_ids.station_id
WHERE line_id = 'red'
ORDER BY season, direction;"""
)

# Q4
target_queries.append(
    """WITH no_green_routes AS (
    SELECT route_id, direction, route_name
    FROM routes
    WHERE line_id <> 'green'
)
SELECT station_orders.route_id, direction, route_name,
       COUNT(station_id), SUM(distance_from_last_station_miles)
FROM station_orders JOIN no_green_routes
ON station_orders.route_id = no_green_routes.route_id
GROUP BY station_orders.route_id
ORDER BY COUNT(station_id) DESC,
         SUM(distance_from_last_station_miles) DESC;"""
)

# Q5
target_queries.append(
    """SELECT station_name, season, AVG(number_service_days)
FROM rail_ridership JOIN stations
ON rail_ridership.station_id = stations.station_id
GROUP BY rail_ridership.station_id, season
ORDER BY AVG(number_service_days) DESC, season, station_name;"""
)

# Q6
target_queries.append(
    """WITH station_total_entries AS (
    SELECT station_id, SUM(gated_entries) AS total_entries
    FROM gated_station_entries
    WHERE service_date LIKE '2021-06-%'
    OR service_date LIKE '2021-07-%'
    OR service_date LIKE '2021-08-%'
    GROUP BY station_id
),
station_max_entries AS (
    SELECT MAX(total_entries) AS max_entries
    FROM station_total_entries
)
SELECT station_name, total_entries
FROM station_total_entries
JOIN station_max_entries
ON total_entries = max_entries
JOIN stations
ON station_total_entries.station_id = stations.station_id;"""
)

# Q7
target_queries.append(
    """SELECT day_type, period_start_time, season,
       line_id, station_name, total_offs
FROM rail_ridership
JOIN time_periods
ON rail_ridership.time_period_id = time_periods.time_period_id
JOIN stations
ON rail_ridership.station_id = stations.station_id
WHERE total_offs >= (SELECT MAX(total_offs) FROM rail_ridership);"""
)

# Q8
target_queries.append(
    """WITH this_ridership AS (
    SELECT station_id, total_ons
    FROM rail_ridership
    WHERE season = 'Fall 2018'
    AND line_id = 'orange'
    AND time_period_id = 'time_period_01'
    AND direction = 0
)
SELECT station_name, total_ons
FROM this_ridership JOIN stations
ON this_ridership.station_id = stations.station_id
WHERE total_ons > (SELECT AVG(total_ons) FROM this_ridership)
ORDER BY total_ons DESC, station_name;"""
)

# Q9
target_queries.append(
    """WITH aggr_routes_by_stations AS (
    SELECT station_id, COUNT(route_id) AS num_routes
    FROM station_orders
    GROUP BY station_id
),
max_routes_stations AS (
    SELECT station_id, num_routes
    FROM aggr_routes_by_stations
    WHERE num_routes = (SELECT MAX(num_routes) FROM aggr_routes_by_stations)
)
SELECT station_name, routes.route_id, line_id, num_routes
FROM max_routes_stations
JOIN stations
ON max_routes_stations.station_id = stations.station_id
JOIN station_orders
ON max_routes_stations.station_id = station_orders.station_id
JOIN routes
ON station_orders.route_id = routes.route_id
ORDER BY line_id, routes.route_id;"""
)

# Q10
target_queries.append(
    """WITH aggr_ridership AS (
    SELECT line_id, station_id,
           SUM(average_flow) AS total_flow,
           SUM(average_ons) AS total_ons,
           SUM(average_offs) AS total_offs
    FROM rail_ridership
    WHERE season = 'Fall 2019'
    GROUP BY line_id, station_id
),
bypassed_ratios_ridership AS (
    SELECT line_id, station_id,
           (total_flow - total_ons - total_offs) / CAST(total_flow AS REAL) AS ratio
    FROM aggr_ridership
),
maximally_bypassed_ridership AS (
    SELECT line_id, MAX(ratio) AS max_ratio
    FROM bypassed_ratios_ridership
    GROUP BY line_id
)
SELECT station_name, line_name, ratio
FROM bypassed_ratios_ridership
JOIN maximally_bypassed_ridership
ON bypassed_ratios_ridership.line_id = maximally_bypassed_ridership.line_id
AND ratio = max_ratio
JOIN stations
ON bypassed_ratios_ridership.station_id = stations.station_id
JOIN lines
ON bypassed_ratios_ridership.line_id = lines.line_id
ORDER BY line_name;"""
)

if __name__ == "__main__":
    print(target_queries[-1])
