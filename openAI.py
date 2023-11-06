import openai
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import copy
import re

import pandas as pd
import csv

deployment_name = "contract_search"
deployment_name1 = "gpt-3.5-turbo"
openai.api_type = "azure"
openai.api_key = "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" # created 2 nov, 2023
openai.api_base = "https://bpogenaiopenai.openai.azure.com/"
openai.api_version = "2023-05-15"


df = pd.read_excel('Demo_Unified_Dashboard_Data_2023.xlsx')


# Question Answer ChatBot
def document(input_text, question='You are a Data Analyst. Can you please analyze the below data and generate insights'):
    prompt = (f"""{question}
    {input_text}
    """)

    response = openai.Completion.create(
        # engine="text-davinci-003",
        engine = deployment_name,
        prompt=prompt,
        max_tokens=300,
        n=1,
        stop=None,
        temperature=0.5,
    )
    document_chatbot = response.choices[0].text.strip()

    return {'document_chatbot': document_chatbot}

documentChatBot(df)