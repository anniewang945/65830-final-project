# 6.5830 Final Project: Leveraging GPT-4 for Enhanced SQL Query Generation Using Natural Language Prompts

This repository contains the pipeline code and data to run our experiments as described in our accompanying paper. We utilize 3 base contexts and their permutations:
- Example Rows
- Database Descriptions
- Required Columns and Tables

We have a total of 17 branches where each branch represents a context. Underneath each branch name, there will be an explanation of how to run the code. Our pipeline has evolved throughout the contexts, so the same file on a different branch may behave differently. We utilize 2 datasets: MBTA from class and Spider as benchmarks. 

## Branches
The naming convention of the branches is datasetname_context. The main branch is the base branch for all other branches. There is nothing to run on this branch.

### MBTA Dataset
The MBTA dataset we used from class is not present in this repo, however, we will denote the line in each branch where one needs to replace the path to their local copy to run it. All questions from PSET1 of the class are used for evaluation. 
Instead of going through each branch to explore each context in detail, you can also go to branch [mbta-db-desc-w-example-row-w-req-tables-and-cols](#mbta-db-desc-w-example-row-w-req-tables-and-cols) and change lines 15-18 in the file mentioned in its section to change to different contexts.
#### mbta
This branch uses schema only (aka no context). You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and it will populate a results folder with files named for each question in the PSET 1, starting with index 0. Each file for a question will contain all 3 trials. 
#### mbta-db-description-context
This branch adds database descriptions as the context. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and it will populate a results_db_description folder with files named for each question in the PSET 1, starting with index 0. Each file for a question will contain all 3 trials. 
#### mbta-example-row-context
This branch adds example rows as the context. You will need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 104) for every trial and question in PSET1. For each trial, you will need to pass in the question you are testing from PSET1 on line 79, and the expected target query on line 109. This branch does not generate a results folder and prints out its results in stdout. 
#### mbta-req-cols-only
This branch adds only the required columns as the context. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 10) once and it will populate a results folder with files named for each question in the PSET 1, starting with index 1. Each file for a question will contain all 6 trials. 
#### mbta-req-cols-and-tables
This branch adds required columns and tables as the context. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 10) once and it will populate a results folder with files named for each question in the PSET 1, starting with index 1. Each file for a question will contain all 6 trials.
#### mbta-db-desc-w-example-row
This branch adds database descriptions and example rows as the context. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and it will populate a results_db_desc_w_example_row folder with files named for each question in the PSET 1, starting with index 0. Each file for a question will contain all 3 trials. 
#### mbta-db-desc-w-example-row-w-req-cols
This branch adds database descriptions, example rows, and required columns as the context. You need to run the file mbta_pipeline.py (change the path to the MBTA database to your local copy on line 11) 3 times (or as many trials you as wish) and it will populate a results folder with files named for each trial run, starting with index 1. Each file for a trial will contain the results for all 10 questions in one file.
#### mbta-db-desc-w-example-row-w-req-tables-and-cols
This branch adds database descriptions, example rows, required columns, and required tables as the context. You need to run the file mbta_pipeline.py (change the path to the MBTA database to your local copy on line 11) 3 times (or as many trials as you wish) and it will populate a results folder with files named for each trial run, starting with index 1. Each file for a trial will contain the results for all 10 questions in one file.

### Spider Dataset
The Spider dataset is available on this repo, so no downloads are necessary for it. Out of the 1034 questions available to benchmark in the original source, we chose 15 questions available in [dev_questions.txt](https://github.com/anniewang945/65830-final-project/blob/spider/dev_questions.txt) to evaluate. Instead of going through each branch to explore each context in detail, you can also go to branch [spider-db-desc-w-req-cols](#spider-db-desc-w-req-cols) and change lines 11-13 in the spider_pipeline.py to feed in different contexts.
#### spider
This branch uses schema only (aka no context). You need to run the file spider_pipeline.py 3 times (or as many trials as you wish). This branch does not generate a results folder and prints out its results in stdout. Each run will contain the results for all questions. Existing results are in a folder named results with files named for each trial run, starting with index 1.
#### spider-db-description-context
This branch adds database descriptions as the context. You need to run the file spider_pipeline.py 3 times (or as many trials as you wish). This branch does not generate a results folder and prints out its results in stdout. Each run will contain the results for all questions. Existing results are in a folder named results_db_description with files named for each trial run, starting with index 1.

For the remaining contexts, you need to run the file spider_pipeline.py 3 times (or as many trials as you wish). The branches do not generate a results folder and print out their results in stdout. Each run will contain the results for all questions using the context from the branch. Existing results in each branch are in a folder named results with files named for each trial run, starting with index 1.
#### spider-example-row-context
This branch adds example rows as the context. 
#### spider-req-cols-only
This branch adds only the required columns as the context.
#### spider-cols-and-tables
This branch adds required columns and tables as the context.
#### spider-db-desc-w-example-row
This branch adds database descriptions and example rows as the context.
#### spider-db-desc-w-req-cols
This branch adds database descriptions and required columns as the context.
#### spider-db-desc-w-example-row-w-req-cols
This branch adds database descriptions, example rows, and required columns as the context.
#### spider-db-desc-w-example-row-w-req-tables-and-cols
This branch adds database descriptions, example rows, required columns, and required tables as the context.
