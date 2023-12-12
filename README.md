# 65380-final-project

This repository contains the pipeline code and data to run our experiments as described in our accompanying paper. We utilize 4 base contexts and their permutations:
- Example Rows
- Database Descriptions
- Required Columns
- Required Columns and Tables

We have a total of 19 branches where each branch represents a context. Underneath each branch name, there will be an explanation of how to run the code. Our pipeline has evolved throughout the contexts, so the same file on a different branch may behave differently. We utilize 2 data sets. The MBTA data set we used from class is not present in this repo, however, we will denote the line in each branch where one needs to replace the path to their local copy to run it. The Spider data set is available on this repo, so no downloads necessary for it.

## Branches
The naming convention of the branches is datasetname_context.
- main
This branch includes the file initial_pipeline.py. This is the base branch for all other branches. Nothing to run on this branch.

### MBTA Data Set
Instead of going through each branch to explore each context in detail, you can also go to branch mbta-db-desc-w-example-row-w-req-tables-and-cols and change lines 15-18 in the file mentioned there to feed in different contexts. See how underneath u
#### mbta
This branch is for the MBTA data set with schema only (aka no context). You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and you will populate a results folder with files named for each question in the PSET 1, starting index 0. Each file for a question will contain all 3 trials. 
#### mbta-db-description-context
This branch is for the MBTA data set with database descriptions passed in. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and you will populate a results_db_description folder with files named for each question in the PSET 1, starting index 0. Each file for a question will contain all 3 trials. 
- mbta-example-row-context
This branch is for the MBTA data set with example rows passed in. You will need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 104) for every trial and question in PSET1. For each trial, you will need to pass in the question you are testing from PSET1 on line 79, and the expected target query on line 109. This branch does not generate a results folder and prints out its results in stdout. 
- mbta-req-cols-only
This branch is for the MBTA data set with only required columns passed in. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 10) once and you will populate a results folder with files named for each question in the PSET 1, starting index 1. Each file for a question will contain all 3 trials. 
- mbta-req-cols-and-tables
This branch is for the MBTA data set with required columns and tables passed in. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 10) once and you will populate a results folder with files named for each question in the PSET 1, starting index 1. Each file for a question will contain all 3 trials.
- mbta-db-desc-w-example-row
This branch is for the MBTA data set with database descriptions and example rows passed in. You only need to run the file initial_pipeline.py (change the path to the MBTA database to your local copy on line 11) once and you will populate a results_db_desc_w_example_row folder with files named for each question in the PSET 1, starting index 0. Each file for a question will contain all 3 trials. 
- mbta-db-desc-w-example-row-w-req-cols
This branch is for the MBTA data set with database descriptions, example rows, and required columns passed in. You only need to run the file mbta_pipeline.py (change the path to the MBTA database to your local copy on line 11) 3 times (or as many trials you wish) and you will populate a results folder with files named for each trial run, starting index 1. Each file for a trial will contain containing all 10 questions in one file.
- mbta-db-desc-w-example-row-w-req-tables-and-cols
This branch is for the MBTA data set with database descriptions, example rows, required columns, and required tables passed in. You only need to run the file mbta_pipeline.py (change the path to the MBTA database to your local copy on line 11) 3 times (or as many trials you wish) and you will populate a results folder with files named for each trial run, starting index 1. Each file for a trial will contain containing all 10 questions in one file. 
- spider
- spider-db-description-context
- spider-example-row-context
- spider-req-cols-only
- spider-cols-and-tables
- spider-db-desc-w-example-row
- spider-db-desc-w-req-cols
- spider-db-desc-w-example-row-w-req-cols
- spider-db-desc-w-example-row-w-req-tables-and-cols
