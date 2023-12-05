import sqlite3
import time

from dotenv import load_dotenv
load_dotenv()

from model import GPT_4, Model
from utils import compare_accuracy, num_tokens_from_string


# Extract database descriptions
db_and_descriptions = dict()
db_desc = open("dev_db_descriptions.txt")
for l in db_desc.readlines():
    if l.startswith("db_id"):
        db = l[len("db_id: "):].strip()
        db_and_descriptions[db] = ""
    else:
        if len(l.strip()) > 0:
            db_and_descriptions[db] += l
db_desc.close()
# for k in db_and_descriptions:
#     print(k)
#     print(db_and_descriptions[k])
#     print("===")

# Extracting questions and schemas first
questions = open("dev_questions.txt")
questions_and_tables = dict()
table_and_schemas = dict()
target_queries = []
for l in questions.readlines():
    if l.startswith("Question"):
        question = l[l.find(": ") + len(": "):l.find(" ||| ")]
        table = l[l.find(" ||| ") + len(" ||| "):].strip()
        db = "database/{}/{}.sqlite".format(table, table)
        conn = sqlite3.connect(db)
        c = conn.cursor()
        try:
            schema_results = c.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
        except Exception as e:
            print("error running sql query: ".upper(), e)
        schema = ""
        for r in schema_results:
            for s in r:
                schema += s
                table_name = s[len("CREATE TABLE "):s.find("(")]
                schema_results = c.execute("SELECT * FROM {} LIMIT 1".format(table_name)).fetchone()
                schema += "\nExample row for {}: {}\n".format(table_name, schema_results)
        # print("Question: {}\nSchema: {}".format(question, schema))
        questions_and_tables[question] = table
        if table not in table_and_schemas:
            table_and_schemas[table] = schema
    elif l.startswith("SQL"):
        target_query = l[l.find("SQL:  ") + len("SQL:  "):]
        # print("Target Query: {}\n".format(target_query))
        target_queries.append(target_query)
    # else:
    #     print()

for q, t in zip(questions_and_tables, target_queries):
    # add more context to schema if needed
    table = questions_and_tables[q]
    system_knowledge = "Given the following SQL tables schemas and its example row (SELECT * FROM table limit 1;), your job is to write queries given a user’s request.\n" + table_and_schemas[table]
    user_prompt = q

    print("passing system knowledge:".upper() + system_knowledge)
    print("passing user prompt:".upper() + user_prompt)
    print("total number of tokens in the current prompt:".upper(), num_tokens_from_string(system_knowledge + user_prompt))

    model = Model(GPT_4, system_prompt=system_knowledge)
    start = time.time()
    answer = model.query(user_prompt)
    end = time.time()
    print("model's answer:".upper(), answer, "\n(took", end-start, "seconds)\n")
    print("")

    # sometimes gpt-4 provides multiple queries with explanations, we want to extract all sql queries presented
    answer_copy = answer
    test_queries = []
    while answer_copy.find("```sql") != -1:
        answer_copy = answer_copy[answer_copy.find("```sql") + len("```sql"):]
        test_queries.append(answer_copy[:answer_copy.find("```")])
        answer_copy = answer_copy[answer_copy.find("```") + len("```"):]

    db = "database/{}/{}.sqlite".format(table, table)
    conn = sqlite3.connect(db)
    c = conn.cursor()
    target_query = t

    try:
        start = time.time()
        target_result = c.execute(target_query).fetchall()
        end = time.time()
        print("time taken with running expected query:", end-start, "seconds")
        # comment until next 3 lines if don't want to see results
        # print("results from expected query".upper())
        # print(target_result)
        # print()
        print("running sql query(s) from model:".upper())
        for t in test_queries:
            print(t)
            start = time.time()
            test_result = c.execute(t).fetchall()
            end = time.time()
            print("time taken with running model query:", end-start, "seconds")
            # comment until next 3 lines if don't want to see results
            # print("results from sql query above".upper())
            # print(test_result)
            # print()
            print("comparing query accuracy with target".upper())
            print(compare_accuracy(test_result, target_result))
            print()
    except Exception as e:
        print("error running sql query: ".upper(), e)

    print("===================================\n")
