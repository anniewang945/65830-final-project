from model import Model, GPT_4
from utils import num_tokens_from_string, compare_accuracy
import sqlite3
import time

# following https://platform.openai.com/examples/default-sql-translate and https://stackoverflow.com/questions/76053920/how-do-i-extract-only-code-content-from-chat-gpt-response
# adding a system prompt let's chatgpt know what to return (in this case, a sql query, but we can also ask it to include explanations as well as it did in the UI)
system_knowledge = """Given the following SQL tables schemas, your job is to write queries given a user’s request.
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

# Tried including "Do not attempt to format on the result apart from selecting the correct columns. Selecting from the table gives the expected display output regardless of what the prompt says."
# but it didn't work

# need to change this based on the prompt you are trying for
user_prompt = """Report the historical total ons on weekdays between 4:00 PM and 6:29 PM (time period 6) per season for the “Kendall/MIT”
Red Line station. Report the season, line ID, direction, and total ons, sorted by the season and direction in ascending
order."""

print("total number of tokens in the current prompt:".upper(), num_tokens_from_string(system_knowledge + user_prompt))

model = Model(GPT_4, system_prompt=system_knowledge)
start = time.time()
answer = model.query(user_prompt)
end = time.time()
print("model's answer:".upper(), answer, "\n(took", end-start, "seconds)\n")
print("===================================\n")

# sometimes gpt-4 provides multiple queries with explanations, we want to extract all sql queries presented
answer_copy = answer
test_queries = []
while answer_copy.find("```sql") != -1:
   answer_copy = answer_copy[answer_copy.find("```sql") + len("```sql"):]
   test_queries.append(answer_copy[:answer_copy.find("```")])
   answer_copy = answer_copy[answer_copy.find("```") + len("```"):]

mbta_db = '../lab0/mbta.sqlite' # replace with your path to mbta
conn = sqlite3.connect(mbta_db)
c = conn.cursor()

# replace with the correct query you are looking for based on the prompt
target_query = """
select season, line_id, direction, total_ons from rail_ridership as r join time_periods as t on r.time_period_id = t.time_period_id join stations as s on r.station_id = s.station_id where day_type = "weekday" and period_start_time between '16:00:00' AND '18:30:00' and station_name = "Kendall/MIT" order by season, direction;
"""

try:
    start = time.time()
    target_result = c.execute(target_query).fetchall()
    end = time.time()
    print("time taken with running expected query:", end-start, "seconds")
    # comment until next 3 lines if don't want to see results
    print("results from expected query".upper())
    print(target_result)
    print()
    print("===================================\n")
    print("running sql query(s) from model:".upper())
    for t in test_queries:
        print(t)
        start = time.time()
        test_result = c.execute(t).fetchall()
        end = time.time()
        print("time taken with running model query:", end-start, "seconds")
        # comment until next 3 lines if don't want to see results
        print("results from sql query above".upper())
        print(test_result)
        print()
        print("comparing query accuracy with target".upper())
        print(compare_accuracy(test_result, target_result))
        print()
        print("===================================\n")
except Exception as e:
    print("error running sql query: ".upper(), e)