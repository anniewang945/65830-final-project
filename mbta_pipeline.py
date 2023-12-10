import sqlite3
import time

from dotenv import load_dotenv
load_dotenv()

from model import GPT_4, Model
from utils import compare_accuracy, num_tokens_from_string

DB_DESCRIPTIONS_FILE_PATH = "dev_db_descriptions.txt"
MBTA_DATABASE_PATH = "database/mbta/mbta.sqlite"
QUESTIONS_FILE_PATH = "dev_questions_mbta.txt"
SCHEMA_INFO_FILE_PATH = "dev_cols_only.txt"

VERBOSE_PRINTING = False
INCLUDE_EXAMPLE_ROW = True
INCLUDE_SCHEMA_INFO = True
INCLUDE_DB_DESCRIPTION = True


def context_db_descriptions(file_path: str) -> dict:
    desc = dict()
    with open(file_path, "r", encoding='utf8') as db_desc:
        for db_line in db_desc.readlines():
            if db_line.startswith("db_id"):
                db_id = db_line[len("db_id: "):].strip()
                desc[db_id] = ""
            else:
                if len(db_line.strip()) > 0:
                    desc[db_id] += db_line
    if VERBOSE_PRINTING:
        print(desc)
    return desc

def extract_questions(file_path) -> dict:
    # Extracting questions and schemas first
    with open(file_path, 'r', encoding='utf8') as questions:
        ques_tables = dict()
        tables = dict()
        queries = []
        for l in questions.readlines():
            if l.startswith("Question"):
                ques = l[l.find(": ") + len(": "):l.find(" ||| ")]
                curr_table = l[l.find(" ||| ") + len(" ||| "):].strip()
                cursor = sqlite3.connect(MBTA_DATABASE_PATH).cursor()
                try:
                    schema_results = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
                except Exception as err:
                    print("error running sql query: ".upper(), err)
                schema = ""
                for r in schema_results:
                    for s in r:
                        schema += s
                        if INCLUDE_EXAMPLE_ROW:
                            table_name = s[len("CREATE TABLE "):s.find("(")]
                            schema_results = cursor.execute(f"SELECT * FROM {table_name} LIMIT 1").fetchone()
                            schema += f"\nExample row for {table_name}: {schema_results}\n"
                if VERBOSE_PRINTING:
                    print(f"Question: {ques}\nSchema: {schema}")
                
                ques_tables[ques] = curr_table
                if curr_table not in tables:
                    tables[curr_table] = schema
            elif l.startswith("SQL"):
                q = l[l.find("SQL:  ") + len("SQL:  "):]
                if VERBOSE_PRINTING:
                    print(f"Target Query: {q}\n")
                queries.append(q)

        return ques_tables, tables, queries

def extract_tables_and_cols(file_path, n_questions) -> dict:
    with open(file_path, "r", encoding='utf8') as f:
        ctx = f.read().split("```")

    if VERBOSE_PRINTING:
        print(f"length of context: {len(ctx)}")
        print(f"number of questions: {n_questions}")

    assert len(ctx) == n_questions
    return ctx

if __name__ == "__main__":
    questions_and_tables, table_and_schemas, target_queries = extract_questions(QUESTIONS_FILE_PATH)
    db_and_descriptions = context_db_descriptions(DB_DESCRIPTIONS_FILE_PATH)
    tables_and_cols_context = extract_tables_and_cols(SCHEMA_INFO_FILE_PATH, len(questions_and_tables))

    i = 0
    for question, tg in zip(questions_and_tables, target_queries):
        # add more context to schema if needed
        table = questions_and_tables[question]
        system_knowledge = "Given the following SQL tables schemas"
        system_knowledge += "" if not INCLUDE_EXAMPLE_ROW else "and its example row (SELECT * FROM table limit 1;)"
        system_knowledge += ", your job is to write queries given a user’s request.\n"
        system_knowledge += table_and_schemas[table]
        system_knowledge += "" if not INCLUDE_DB_DESCRIPTION else "\nThe following paragraphs further describe the database.\n" + db_and_descriptions['mbta']
        
        user_prompt = question
        if INCLUDE_SCHEMA_INFO:
            user_prompt += "\n" + tables_and_cols_context[i]

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

        conn = sqlite3.connect(MBTA_DATABASE_PATH)
        c = conn.cursor()
        target_query = tg

        try:
            if VERBOSE_PRINTING:
                print("running target sql query:".upper())
                print(target_query)

            start = time.time()
            target_result = c.execute(target_query).fetchall()
            end = time.time()
            print("time taken with running expected query:", end-start, "seconds")
            # comment until next 3 lines if don't want to see results
            if VERBOSE_PRINTING:
                print("results from expected query".upper())
                print(target_result)
                print()
            print("running sql query(s) from model:".upper())
            for tg in test_queries:
                print(tg)
                start = time.time()
                test_result = c.execute(tg).fetchall()
                end = time.time()
                print("time taken with running model query:", end-start, "seconds")

                if VERBOSE_PRINTING:
                    print("results from sql query above".upper())
                    print(test_result)
                    print()

                print("comparing query accuracy with target".upper())
                print(compare_accuracy(test_result, target_result))
                print()
        except Exception as e:
            print("error running sql query: ".upper(), e)
            print(compare_accuracy([], target_result))
            print()

        i += 1
        print("===================================\n")
        