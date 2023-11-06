import openai
import openpyxl

# Set up your OpenAI API key
api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = api_key

def get_answer_from_chatgpt(question):
    # Send the user's question to ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Translate the following English text to French: {question}",
        max_tokens=50,
    )

    answer = response.choices[0].text.strip()

    return answer

def get_data_from_excel(excel_file, sheet_name, question):
    # Load Excel file
    workbook = openpyxl.load_workbook(excel_file)
    sheet = workbook[sheet_name]

    # Search for the answer based on the user's question
    for row in sheet.iter_rows(values_only=True):
        if question.lower() in row[0].lower():
            return row[1]

    return "Answer not found in the Excel sheet."

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please provide a question as a command-line argument.")
    else:
        question = sys.argv[1]
        excel_file = "your_excel_file.xlsx"
        sheet_name = "Sheet1"

        answer = get_data_from_excel(excel_file, sheet_name, question)
        if answer == "Answer not found in the Excel sheet.":
            answer = get_answer_from_chatgpt(question)

        print(answer)
