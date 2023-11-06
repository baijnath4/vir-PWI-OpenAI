import openai
import pandas as pd
import numpy as np
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import get_embedding, cosine_similarity
import re
deployment_name = "qa"
openai.api_type = "azure"
openai.api_key = "f18496fb664247a59ec58c91b068458f"
openai.api_base = "https://bpogenaiopenai.openai.azure.com/"
openai.api_version = "2023-05-15"
import os

import sys
userQuestion = sys.argv[1]

df = pd.read_csv('.\\Data\\Demo_Unified_Dashboard_Data_2023.csv')

def extract_details(question):
    # prompt = f"{question}\n{text}\n\\n:"
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=deployment_name,
        prompt=question,
        max_tokens=20,
        temperature=0,
        n = 1,
        stop=None
    )
    diffs = response.choices[0].text
    return diffs.strip()


def dataFromDf(userQuestion,df=df):
    df=df
    # ques = f'count of country from column Country? '
    openai_prompt = f"create pandas code of user question, pandas dataframe name df. user question is {userQuestion}"
    response = extract_details(openai_prompt)
    finalResult = eval(response)
    return finalResult

finalResult = dataFromDf(userQuestion, df)
print(finalResult)