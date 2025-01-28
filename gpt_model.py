from openai import OpenAI

client = OpenAI()

def ask_Gpt(code, index, df, refactoring_type, column):
    """
    Asks GPT to refactor the given code using a specified Python idiom.

    Args:
      code (str): The code to be refactored.
      index (int): The index of the code snippet in the dataframe.
      df (pandas.DataFrame): The dataframe containing the code snippets.
      refactoring_type (str): The type of Python idiom to use for refactoring.
      column (str): The column name in the dataframe where the code is located.

    Returns:
      str: The refactored code and the number of refactorings made.
    """
    prompt = "Refactor the code using python " + refactoring_type + " idiom, and provide the python code refactored and the number of " + refactoring_type + " refactoring you have made.:\n" + str(code)
    completion = client.chat.completions.create(
      model="chatgpt-4o-latest",
      messages=[
        {"role": "system", "content": "You are a software developer, skilled in writing python source code and refactoring python code using " + refactoring_type},
        {"role": "user", "content": prompt}
      ]
    )

    message = completion.choices[0].message.content
    return message