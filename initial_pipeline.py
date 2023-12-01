from model import Model, GPT_4
from utils import num_tokens_from_string, compare_accuracy, print_and_append
import sqlite3
import time
import os
from mbta_tests import system_knowledge, user_prompts, target_queries

# following https://platform.openai.com/examples/default-sql-translate and https://stackoverflow.com/questions/76053920/how-do-i-extract-only-code-content-from-chat-gpt-response
# adding a system prompt lets chatgpt know what to return (in this case, a sql query, but we can also ask it to include explanations as well as it did in the UI)

mbta_db = 'mbta.sqlite' # replace with your path to mbta
conn = sqlite3.connect(mbta_db)
c = conn.cursor()

results_dir = 'results_db_description/'
if not os.path.exists(results_dir):
  os.mkdir(results_dir)

for i in range(0, 10):
  results_path = results_dir + 'mbta_' + str(i) + '.txt'
  user_prompt = user_prompts[i]
  target_query = target_queries[i]

  out_str = f"Testing prompt {i}:\n" + user_prompt + "\n\n"
  out_str += "total number of tokens: ".upper() + str(num_tokens_from_string(system_knowledge + user_prompt)) + '\n\n'
  print_and_append(results_path, out_str)

  model = Model(GPT_4, system_prompt=system_knowledge)
  # model = Model(GPT_3, system_prompt=system_knowledge)
  start = time.time()
  answer = model.query(user_prompt)
  end = time.time()

  out_str = "Model's answer:\n" + f"{answer}\n\n"
  out_str += "time taken to generate answer: ".upper() + f"{end - start} seconds\n"
  out_str += "===================================\n"
  print_and_append(results_path, out_str)

  # test_query = answer.removeprefix("```sql").removesuffix("```")
  
  # sometimes gpt-4 provides multiple queries with explanations, we want to extract all sql queries presented
  answer_copy = answer
  test_queries = []
  while answer_copy.find("```sql") != -1:
    answer_copy = answer_copy[answer_copy.find("```sql") + len("```sql"):]
    test_queries.append(answer_copy[:answer_copy.find("```")])
    answer_copy = answer_copy[answer_copy.find("```") + len("```"):]

  try:
    # test_result = c.execute(test_query).fetchall()
    # target_result = c.execute(target_query).fetchall()
    # f.write(compare_accuracy(test_result, target_result) + '\n\n')
    # f.write(f"time taken: {end - start} seconds\n")
    qry_start = time.time()
    target_result = c.execute(target_query).fetchall()
    qry_end = time.time()
    out_str = "Target query:\n" + target_query + "\n\n"
    out_str += "time taken to run target query: ".upper() + f"{qry_end - qry_start} seconds\n"
    print_and_append(results_path, out_str)
    # comment until next 3 lines if don't want to see results
    # print("results from expected query".upper())
    # print(target_result)
    # print()
    print_and_append(results_path, "===================================\n" + "running sql query(s) from model:\n".upper())
    ctr = 0
    for t in test_queries:
      print_and_append(results_path, "------------\n" + f"Generated query {ctr}:\n{t}\n\n")
      qry_start = time.time()
      test_result = c.execute(t).fetchall()
      qry_end = time.time()
      out_str = "time taken to run model query: ".upper() + f"{qry_end - qry_start} seconds\n"
      # comment until next 3 lines if don't want to see results
      # print("results from sql query above".upper())
      # print(test_result)
      # print()
      out_str += compare_accuracy(test_result, target_result)
      out_str += "\n"
      print_and_append(results_path, out_str)
      ctr += 1
  except Exception as e:
      print_and_append(results_path, f"error running sql query: {e}\n")
  print_and_append(results_path, "\n==========END OF TEST==========\n\n")