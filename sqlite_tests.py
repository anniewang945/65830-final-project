import sqlite3
from mbta_tests import target_queries
from utils import compare_accuracy

# following https://platform.openai.com/examples/default-sql-translate and https://stackoverflow.com/questions/76053920/how-do-i-extract-only-code-content-from-chat-gpt-response
# adding a system prompt lets chatgpt know what to return (in this case, a sql query, but we can also ask it to include explanations as well as it did in the UI)

mbta_db = 'mbta.sqlite' # replace with your path to mbta
conn = sqlite3.connect(mbta_db)
c = conn.cursor()

for i in range(7,8):
  print(f"Test {i}")
  target_query = target_queries[i]

  test_query = """
    SELECT s.station_name, r.total_ons
    FROM stations s
    JOIN rail_ridership r ON s.station_id = r.station_id
    WHERE r.season = 'Fall 2018'
    AND r.line_id = 'orange'
    AND r.direction = 0
    AND r.time_period_id = 'time_period_01'
    AND r.total_ons > (SELECT AVG(total_ons) 
                    FROM rail_ridership 
                    WHERE season = 'Fall 2018' 
                    AND time_period_id = 'time_period_01' 
                    AND direction = 0
                    AND line_id = 'orange')
    ORDER BY r.total_ons DESC, s.station_name ASC;"""
    
  try:
    print('===============\n')
    test_result = c.execute(test_query).fetchall()
    target_result = c.execute(target_query).fetchall()
    print(compare_accuracy(test_result, target_result) + '\n\n')
    print(f"{test_result}\n\n")
    print(f"{target_result}\n")
  except Exception as e:
    print("error running sql query: ", e)