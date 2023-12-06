from model import Model, GPT_4
from utils import num_tokens_from_string, compare_accuracy
import sqlite3
import time
from mbta_tests import system_knowledge, user_prompts, target_queries

# following https://platform.openai.com/examples/default-sql-translate and https://stackoverflow.com/questions/76053920/how-do-i-extract-only-code-content-from-chat-gpt-response
# adding a system prompt lets chatgpt know what to return (in this case, a sql query, but we can also ask it to include explanations as well as it did in the UI)

mbta_db = "../pset1/mbta.sqlite"  # replace with your path to mbta
conn = sqlite3.connect(mbta_db)
c = conn.cursor()

for _ in range(6):
    for i in range(len(user_prompts)):
        print(f"Testing prompt {i}")
        user_prompt = user_prompts[i]
        target_query = target_queries[i]

        model = Model(GPT_4, system_prompt=system_knowledge)
        start = time.time()
        answer = model.query(user_prompt)
        end = time.time()
        test_query = answer.removeprefix("```sql").removesuffix("```")

        try:
            with open(f"results/mbta_{i+1}.txt", "a+") as f:
                f.write("===============\n")
                f.write(
                    "total number of tokens in the current prompt:"
                    + str(num_tokens_from_string(system_knowledge + user_prompt))
                    + "\n\n"
                )
                f.write(f"Generated query:\n{test_query}\n\n")
                test_result = c.execute(test_query).fetchall()
                target_result = c.execute(target_query).fetchall()
                f.write(compare_accuracy(test_result, target_result) + "\n\n")
                f.write(f"time taken: {end - start} seconds\n")
        except Exception as e:
            with open(f"results/mbta_{str(i+1)}.txt", "a+") as f:
                f.write(f"error running sql query: {e}\n")
            print("error running sql query: ", e)
