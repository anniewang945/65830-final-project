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

user_prompts = []
# Q1
user_prompts.append("""Find all stations which are at least 1 mile away from the previous station. Report the station ID, route ID, and distance
(in miles) to the previous station, sorted by decreasing distance. Break ties in distance by sorting by route ID and then
station ID, both in ascending order.""")

# Q2
user_prompts.append("""Find the first and last station for each route on each line. Report the line name, route direction name, and first and last station name. Sort the results by the line name, direction name, first station name, and then last station name—all in ascending order.""")

# Q3
user_prompts.append("""Report the historical total ons on weekdays between 4:00 PM and 6:30 PM per season for the “Kendall/MIT” Red Line station. Report the season, line ID, direction, and total ons, sorted by the season and direction in ascending order.""")

# Q4
user_prompts.append("""Find the total length in miles and number of stations of each line’s routes. Report the route id, direction, route - name, number of stations, and length in miles for each route. Exclude the Green Line since the distance between stations is missing. Sort the results by total number of stations in descending order (break tie using total length in miles in descending).""")

# Q5
user_prompts.append("""For each station in each season, find the average number of line service days. (That is, find the average of the number of number service days over different lines, directions and time periods, but do not sum over different values for season.) Report the station name, season, and averaged number service days value, sorted by that average value in descending order. Break ties by sorting by season and then station name, both in ascending order.""")

# Q6
user_prompts.append("""Find the station(s) with the most gated entries over the summer of 2021 (June, July, August of 2021). Report the station
6.5830/6.5831 Problem Set 1 (Fall 2023) 4 name(s) and the number of gated entries.""")

# Q7
user_prompts.append("""Find the station, time period, and season with the largest number of people who get off (the largest “total offs”). A station may be associated with multiple directions; consider these directions to be distinct for the purposes of finding the largest total offs (e.g., the total offs for Kendall/MIT with a direction of 0 should be considered separately from the total offs for Kendall/MIT with a direction of 1 when you are computing the largest total offs). Report the day type, period start time, season, line id, station name, and total offs for this station.""")

# Q8
user_prompts.append("""Find every Orange Line station in Fall 2018 that, during time period 01 and the direction of 0, had a total ons passenger count that was greater than average for all Orange Line stations at that same time period, same season, and in the same direction. Report the station name and the total ons value. Sort the results by total ons in descending order and then station name in ascending order.""")

# Q9
user_prompts.append("""Find the station with most number of routes passing through it. (E.g. North Station has six routes passing through it: orange line in both directions and two green lines in both directions) Report station name, route id, line id, and total number of routes passing through the station. Sort the results by line id in ascending order and then route id in ascending order.""")

# Q10
user_prompts.append("""For each line, in the Fall 2019 season, find the station with “maximally bypassed ratio”. That is, the station “s” that has the largest ratio “(a - b)/a”, where “a” is the the sum of average flow values for all time periods and all directions of “s” and “b” is the total sum of: the sum of its average ons and sum of its average offs values. Therefore, the ratio “(a - b)/a” represents the proportion of people who bypassed one station. Report the station name, its line name, and its bypassed ratio. Sort the results by line name in ascending order. HINT: You may need to use function CAST(total flow AS REAL) to cast the summation of flows (i.e. “a” above) to real number.""")

target_queries = []
# Q1
target_queries.append("""SELECT station_id, route_id, distance_from_last_station_miles
FROM station_orders
WHERE distance_from_last_station_miles >= 1
ORDER BY distance_from_last_station_miles DESC, route_id, station_id;""")

# Q2
target_queries.append("""SELECT line_name, direction_desc, x.station_name, y.station_name
FROM routes JOIN lines ON routes.line_id = lines.line_id
JOIN stations x
ON x.station_id = first_station_id
JOIN stations y
ON y.station_id = last_station_id
ORDER BY line_name, direction_desc, x.station_name, y.station_name;""")

# Q3
target_queries.append("""WITH tp_ids AS (
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
ORDER BY season, direction;""")

# Q4
target_queries.append("""WITH no_green_routes AS (
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
         SUM(distance_from_last_station_miles) DESC;""")

# Q5
target_queries.append("""SELECT station_name, season, AVG(number_service_days)
FROM rail_ridership JOIN stations
ON rail_ridership.station_id = stations.station_id
GROUP BY rail_ridership.station_id, season
ORDER BY AVG(number_service_days) DESC, season, station_name;""")

# Q6
target_queries.append("""WITH station_total_entries AS (
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
ON station_total_entries.station_id = stations.station_id;""")

# Q7
target_queries.append("""SELECT day_type, period_start_time, season,
       line_id, station_name, total_offs
FROM rail_ridership
JOIN time_periods
ON rail_ridership.time_period_id = time_periods.time_period_id
JOIN stations
ON rail_ridership.station_id = stations.station_id
WHERE total_offs >= (SELECT MAX(total_offs) FROM rail_ridership);""")

# Q8
target_queries.append("""WITH this_ridership AS (
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
ORDER BY total_ons DESC, station_name;""")

# Q9
target_queries.append("""WITH aggr_routes_by_stations AS (
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
ORDER BY line_id, routes.route_id;""")

# Q10
target_queries.append("""WITH aggr_ridership AS (
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
ORDER BY line_name;""")

if __name__ == "__main__":
    print(target_queries[-1])