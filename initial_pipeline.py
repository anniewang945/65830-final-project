from model import Model, GPT_4
from utils import num_tokens_from_string, compare_accuracy
import sqlite3
import time

# following https://platform.openai.com/examples/default-sql-translate and https://stackoverflow.com/questions/76053920/how-do-i-extract-only-code-content-from-chat-gpt-response
# adding a system promot let's chatgpt know what to return (in this case, a sql query, but we can also ask it to include explanations as well as it did in the UI)
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

# need to change this based on the prompt you are trying for
user_prompt = """Find all stations which are at least 1 mile away from the previous station. Report the station ID, route ID, and distance
(in miles) to the previous station, sorted by decreasing distance. Break ties in distance by sorting by route ID and then
station ID, both in ascending order."""

print("total number of tokens in the current prompt:".upper(), num_tokens_from_string(system_knowledge + user_prompt))

model = Model(GPT_4, system_prompt=system_knowledge)
start = time.time()
answer = model.query(user_prompt)
end = time.time()
print("model's answer:".upper(), answer, "\n(took", end-start, "seconds)\n")
print("===================================\n")

test_query = answer[answer.find("```sql") + len("```sql"):]
test_query = test_query[:test_query.find("```")]
# test_query = answer.removeprefix("```sql").removesuffix("```")

mbta_db = '../lab0/mbta.sqlite' # replace with your path to mbta
conn = sqlite3.connect(mbta_db)
c = conn.cursor()

# replace with the correct query you are looking for based on the prompt
target_query = """
select station_id, route_id, distance_from_last_station_miles as distance from station_orders where distance >= 1.0 order by distance desc, route_id, station_id;
"""

try:
    print("running sql query from model:".upper(), test_query)
    print()
    print("===================================\n")
    test_result = c.execute(test_query).fetchall()
    print("results from sql query from model".upper())
    print(test_result)
    print()
    target_result = c.execute(target_query).fetchall()
    print("results from expected query".upper())
    print(target_result)
    print()
    print("===================================\n")
    print("comparing query accuracy with target".upper())
    print(compare_accuracy(test_result, target_result))
except Exception as e:
    print("error running sql query: ".upper(), e)