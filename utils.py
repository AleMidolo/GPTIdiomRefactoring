import os
import re

def extract_text_and_code(text):
    """
    Extracts text and the first Python code block from the given text.

    Args:
        text (str): The input text containing both plain text and Python code blocks.

    Returns:
        tuple: A tuple containing two elements:
            - text_only (str): The input text with the Python code blocks removed.
            - code (str or None): The first Python code block found in the input text, or None if no code block is found.
    """
    code_blocks = re.findall(r'```python(.*?)```', text, re.DOTALL)
    code = code_blocks[0].strip() if code_blocks else None

    text_only = re.sub(r'```python.*?```', '', text, flags=re.DOTALL).strip()

    return text_only, code

def list_files_recursive(directory):
    """
    Recursively lists all files in a given directory.

    Args:
        directory (str): The path to the directory to search.

    Returns:
        list: A list of file paths for all files found within the directory and its subdirectories.
    """
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            all_files.append(os.path.join(root, file))
    return all_files

def get_diff_lines(A, B):
    """
    Compare two code snippets and return the lines that are present in the second snippet but not in the first.

    Args:
        A (str): The first code snippet to compare.
        B (str): The second code snippet to compare.

    Returns:
        list: A list of lines that are present in the second code snippet (B) but not in the first (A), 
              after removing spaces for comparison.
    """
    # Split the code snippets into lines
    lines_A = set(line.replace(" ", "") for line in str(A).splitlines())  # Remove spaces for comparison in A
    lines_B = str(B).splitlines()

    # Collect lines from B that are not in A after removing spaces for comparison
    diff_lines = [line for line in lines_B if line.replace(" ", "") not in lines_A]

    return diff_lines

def getRefactoringType(file):
    """
    Determines the type of refactoring based on specific keywords found in the given file name.

    Args:
        file (str): The name of the file to be analyzed for refactoring type.

    Returns:
        str: A string describing the type of refactoring based on the detected keyword.
             Possible return values include:
             - "pep 448 - Additional Unpacking Generalizations"
             - "PEP 498 – Literal String Interpolation"
             - "PEP 343 – The “with” Statement"
             - "PEP 202 – List Comprehensions"
             - "PEP 274 – Dictionary Comprehensions"
             - "set comprehension"
             - "chain comparison"
             - "truth value test"
             - "for multiple targets"
             - "chain assign same value"
             - "assign multiple targets"
             - "loop else"
    """
    refactoring_type = ""

    if "star_in_func_call" in file:
        refactoring_type = "pep 448 - Additional Unpacking Generalizations"
    elif "fstring" in file:
        refactoring_type = "PEP 498 – Literal String Interpolation"
    elif "with" in file:
        refactoring_type = "PEP 343 – The “with” Statement"
    elif "list_comprehension" in file:
        refactoring_type = "PEP 202 – List Comprehensions"
    elif "dict_comprehension" in file:
        refactoring_type = "PEP 274 – Dictionary Comprehensions"
    elif "set_comprehension" in file:
        refactoring_type = "set comprehension"
    elif "chain_compare" in file:
        refactoring_type = "chain comparison"
    elif "truth_test" in file:
        refactoring_type = "truth value test"
    elif "for_multi_tar" in file:
        refactoring_type = "for multiple targets"
    elif "chain_ass" in file:
        refactoring_type = "chain assign same value"
    elif "ass_multi_tar" in file:
        refactoring_type = "assign multiple targets"
    elif "loop_else" in file:
        refactoring_type = "loop else"

    return refactoring_type