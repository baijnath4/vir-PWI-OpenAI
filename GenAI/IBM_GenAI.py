import pandas as pd
import numpy as np
import os
from credential import API_KEY, PROJECT_ID

import sys
# userQuestion = sys.argv[1]
userQuestion = "Your question Accounts that are Below Target by SLA for last month year ?"

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",
    "apikey":API_KEY
    }
project_id = PROJECT_ID

# -------------------IBM GEN AI ----------------------------
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
# print([model.name for model in ModelTypes])

model_id = ModelTypes.STARCODER

from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams

parameters = {
    GenParams.DECODING_METHOD: "greedy",
    GenParams.MAX_NEW_TOKENS: 200,
    GenParams.STOP_SEQUENCES: ["<end·of·code>"]
}

from ibm_watson_machine_learning.foundation_models import Model

model = Model(
    model_id=model_id, 
    params=parameters, 
    credentials=credentials,
    project_id=project_id)

# Defining the model parameters

# model.get_details()

dataread = pd.read_excel('.\\Data\\KLARITY.KLARITY_LIGHT_PUBLISH_SUMMARY_1.xlsm')
requiredData = dataread[['MONTH','YEAR','ACCOUNT','GEO','PROCESS','SLA_CATEGORY','METRIC_NAME','MEASURE_TYPE','EXPECTED_TARGET','SLA_PERFORMANCE','VOLUME','AMOUNT_IN_USD','CYCLE_TIME','METRIC_ACTUAL']]
df = requiredData.copy()
last_month = df['MONTH'].max() 
last_year = df['YEAR'].max()

# Generate code based on instruction

instruction = """Using the directions below, generate Python code for the given task.

data frame name is df. 

The columns and their data types are given below as a Python dictionary with keys showing column names and values showing the data types.

{'MONTH': 'str', 'YEAR': 'int', 'ACCOUNT': 'str', 'GEO': 'str', 'PROCESS': 'str', 'SLA_CATEGORY': 'str', 'METRIC_NAME': 'str', 'MEASURE_TYPE': 'str',
 'EXPECTED_TARGET': 'float', 'SLA_PERFORMANCE': 'float', 'VOLUME': 'float', 'AMOUNT_IN_USD': 'float', 'CYCLE_TIME': 'float', 'METRIC_ACTUAL': 'float'}

Month – Account  sla month is available in this column
Year – Account sla year is available
Account – different type of account
EXPECTED_TARGET – expected target or SLA value of different accounts
SLA_PERFORMANCE – current sla achieved by account

Input:
# write python code to get last month from the column Month.

output:
last_month = df['MONTH'].max() 

Input:
# write python code to get last year from the column Year.

output:
last_year = df['YEAR'].max() 


Input:
# write python code to accounts sla performance below target.

Output:
df = df.loc[df['SLA_PERFORMANCE'] < df['EXPECTED_TARGET']]
   
<end of code>
"""

question = f"""Input:
# Write only python code to.  {userQuestion} ?

"""

# Generat the code using BigCode starcoder-15.5b model

result = model.generate_text(" ".join([instruction, question]))
code_as_text = result.split('Output:')[1].split('<end of code>')[0]
last_month = df['MONTH'].max() 
last_year = df['YEAR'].max()
def genAIResultParsing(df,code_as_text):
    df=df
   
    splitedResult = code_as_text.split("\n")

    for item in splitedResult:
        if item != "":
            try:
                df = eval(item.split(" = ")[1])
            except:
                pass
    return df

result = genAIResultParsing(df,code_as_text)

jsonData = result.to_json(orient='records')



print(jsonData)


