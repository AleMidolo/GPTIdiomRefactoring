import pandas as pd
from utils import *
from gpt_model import ask_Gpt
from metrics import performanceEvaluation

def main():
    """
    Main function to process benchmark files, refactor code using GPT, and evaluate performance.
    This function performs the following steps:
    1. Defines the path to the benchmark files.
    2. Initializes an empty DataFrame to store the results.
    3. Recursively lists all benchmark files in the specified directory.
    4. Iterates over each benchmark file and processes its content:
        a. Reads the CSV file into a DataFrame.
        b. Determines the type of refactoring required for the file.
        c. Iterates over each row in the DataFrame:
            i. Extracts the old code to be refactored.
            ii. Sends the old code to GPT for refactoring.
            iii. Extracts the refactored code and additional text from GPT's response.
            iv. Creates a new row with the original and refactored code, and other relevant information.
            v. Appends the new row to the results DataFrame.
    5. Saves the results DataFrame to a CSV file for each refactoring type.
    6. Calls the performance evaluation function to assess the refactoring results.
    Note:
    Before performing the evaluation, manually update the 'count_gpt' column for all result files in the './results/all_refactorings/' directory.
    """
    benchmark_path = "./Data/benchmarks/"

    result_df = pd.DataFrame(columns=['file_html', 'method_content', 'file_name', 'lineno', 'old_code', 'bench_code', 'count_bench', 'gpt_code', 'count_gpt', 'text', 'answer'])

    benchmarkFiles = list_files_recursive(benchmark_path)

    for file in benchmarkFiles:

        print("Processing file: ", file)
        df = pd.read_csv(file)

        refactoring_type = getRefactoringType(file)

        for index, row in df.iterrows():
            bench_code = row['old_code']
            result = ask_Gpt(bench_code, refactoring_type)

            text, gpt_code = extract_text_and_code(result)

            row = {'file_html': row['file_html'], 'method_content': row['method_content'], 'file_name': row['file_name'], 'lineno': row['lineno'], 'old_code': row['old_code'], 'bench_code': row['new_code'], 'count_bench': '1', 'gpt_code': gpt_code, 'count_gpt': '', 'text': text, 'answer': result}
            df = pd.DataFrame([row])
            result_df = pd.concat([result_df, df], ignore_index=True)

        result_df.to_csv(f'./Results/all_refactorings/{refactoring_type}.csv', index=False)
    
    # before performing this evaluation, make sure to manually update the 'count_gpt' column for all results file in ./results/all_refactorings/
    performanceEvaluation()

if __name__ == "__main__":
    main()