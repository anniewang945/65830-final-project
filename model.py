from openai import OpenAI
import time
import os
import regex

GPT_3 = "gpt-3.5-turbo-1106"
GPT_4 = "gpt-4"
DEFAULT_SYS = "You are a helpful assistant."
api_key = os.environ[
    "OPENAI_API_KEY"
]  # set api key with this env var and api will automatically pick it up


class Model:
    def __init__(self, model_type, system_prompt=DEFAULT_SYS, num_retries=3):
        self.model_type = model_type
        self.num_retries = num_retries
        self.base_message = [{"role": "system", "content": system_prompt}]

    def query(self, question: str, verbose=False) -> str:
        """
        Queries the specified model and returns the output.
        Retries queries NUM_RETRIES times in the case of failure.
        """
        start = time.time()
        for _ in range(self.num_retries):
            try:
                client = OpenAI()
                output = client.chat.completions.create(
                    model=self.model_type,
                    messages=self.base_message
                    # + [{"role": "assistant", "content": "SELECT * FROM table"}] # apparently you can also use assistant
                    + [{"role": "user", "content": question}],
                )
                answer = output.choices[0].message.content
                if verbose:
                    print("API call time: " + str(time.time() - start))
                break  # no errors, move on to next question
            except Exception as e:
                answer = ""
                print(e)
                continue
        return answer


if __name__ == "__main__":
    model = Model(GPT_4)
    print(model.query("what is the today's date?"))
