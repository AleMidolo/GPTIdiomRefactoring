#Analyse extracted data
import pandas as pd
import os
from utils import list_files_recursive

def performanceEvaluation():
    """
    Evaluates the performance of GPT-based refactorings by comparing them with benchmark results.

    This function reads CSV files from a specified directory, processes the data to compare GPT-based refactorings
    with benchmark results, and generates a LaTeX table summarizing the results. It also saves detailed comparison
    results into separate CSV files based on different criteria.

    The function performs the following steps:
    1. Recursively lists all files in the specified source directory.
    2. Initializes counters and a LaTeX table header.
    3. Iterates over each file, reads the data, and performs comparisons between GPT and benchmark counts.
    4. Saves detailed comparison results into separate CSV files based on the comparison criteria.
    5. Updates the total counters and appends the results to the LaTeX table.
    6. Writes the final LaTeX table to a text file.

    Returns:
        None

    Note:
    Run the "main" function from the main.py file before calling this function to generate the required result files.
    This evaluation must be performed after manually updating the 'count_gpt' column for all result files in the './Results/all_refactorings/' directory.
    """
    sourcePath = "./Results/all_refactorings/"

    onlyfiles = list_files_recursive(sourcePath)
    suffix = ".csv"

    latex_table = "pythonic idiom & count\_gpt & count\_bench & equals & gpt_more & bench_more & gpt_zero & methods \\\\\n"
    total_count_gpt = 0
    total_count_bench = 0
    totale_equals = 0
    total_gpt_more = 0
    total_bench_more = 0
    total_gpt_zero = 0

    for file in onlyfiles:

        print("Analysing file: ", file)
        type_name = type_name.replace(suffix, "")

        df = pd.read_csv(file)
        gpt_more = (df['count_gpt'] > df['count_bench']).sum()
        bench_more = (df['count_gpt'] < df['count_bench']).sum()
        equals = (df['count_gpt'] == df['count_bench']).sum()
        gpt_zero = (df['count_gpt'] == 0).sum()

        methods_count = df.shape[0]
        count_gpt = df['count_gpt'].sum()
        count_bench = df['count_bench'].sum()

        if equals > 0:
            more_df = df[df['count_gpt'] == df['count_bench']]
            more_df.to_csv("./Results/peformance_evaluation/equals/equals_" + type_name + ".csv", index=False)

        if bench_more > 0:
            more_df = df[df['count_gpt'] < df['count_bench']]
            more_df.to_csv("./Results/peformance_evaluation/bench_more/more_" + type_name + ".csv", index=False)

        if gpt_more > 0:
            more_df = df[df['count_gpt'] > df['count_bench']]
            more_df.to_csv("./Results/peformance_evaluation/gpt_more/more_" + type_name + ".csv", index=False)

        if gpt_zero > 0:
            zer_df = df[df['count_gpt'] == 0]
            zer_df.to_csv("./Results/peformance_evaluation/zero/zero_" + type_name + ".csv", index=False)

        total_count_gpt += count_gpt
        total_count_bench += count_bench
        totale_equals += equals
        total_gpt_more += gpt_more
        total_bench_more += bench_more
        total_gpt_zero += gpt_zero

        new_line = f"{type_name} & {count_gpt} & {count_bench} & {equals} & {gpt_more} & {bench_more} & {gpt_zero} & {methods_count}\\\\\n"
        latex_table += new_line

    new_line =  f"Total & {total_count_gpt} & {total_count_bench} & {totale_equals} & {total_gpt_more} & {total_bench_more} & {total_gpt_zero} & 1201\\\\\n"
    latex_table += new_line
    file_path = "./Results/metrics_table.txt"


    with open(file_path, 'w') as file:
        file.write(latex_table)

if __name__ == "__main__":
    performanceEvaluation()