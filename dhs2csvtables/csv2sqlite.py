import os
import subprocess
import traceback
import sqlite3
import warnings

from dhs2csvtables.utils.timer import pprint_elapsed_time

warnings.simplefilter(action='ignore', category=FutureWarning)  # TODO - Internship - can you debug it please?


@pprint_elapsed_time
def rename_table_names(filepath_db):
    """
    Rename tables in the SQLite database at db_path by removing
    leading '.\' or '.\\' from table names.
    """
    conn = sqlite3.connect(filepath_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    renamed = 0

    for (table_name,) in tables:
        # Detect tables starting with '.\' or '.\\'
        if table_name.startswith('.\\') or table_name.startswith('.\\\\'):
            # Remove the leading '.\' characters
            new_name = table_name.lstrip('.\\')
            print(f'INFO - Renaming "{table_name}" to "{new_name}"...')
            try:
                cursor.execute(f'ALTER TABLE "{table_name}" RENAME TO "{new_name}";')
                renamed += 1
            except Exception as e:
                print(f'ERROR - Error renaming {table_name}: {e}')

    conn.commit()
    conn.close()


@pprint_elapsed_time
def run_csv2sqlite(dir_input_dhs_csv_files: str, survey_info: str) -> None:
    """
    Converts CSV files in a specified directory to a SQLite database using the `csvs-to-sqlite` command-line tool.

    This function takes the directory containing DHS CSV files and converts them into a relational SQLite database.
    It outputs the SQLite database into a 'database' subdirectory within the input directory.

    Args:
        dir_input_dhs_csv_files (str): The directory path where the CSV files and other resources (such as parsed specs) are located.
        survey_info (str): The name of the survey to use as the SQLite database name or relevant metadata identifier.

    Behavior:
        - It first checks if the output directory for the database exists. If not, it creates one.
        - It then invokes the `csvs-to-sqlite` tool via a subprocess call, passing it the paths to the necessary CSV files and specs.
        - Once the SQLite database is generated, it is saved in the 'database' subdirectory inside `dir_input_dhs_csv_files`.
        - If the process fails at any step, the error is caught and printed.

    Decorators:
        @pprint_elapsed_time: A decorator that prints the time taken to execute this function.

    Raises:
        Any exceptions that occur during the execution are caught and printed as part of the traceback.

    Returns:
        None: The function does not return any value.
    """
    try:
        print("\nINFO [SECOND CONVERSION] - Generating SQLite database from CSV relational tables...")

        # Directory for the database output
        dir_database_out = os.path.join(dir_input_dhs_csv_files, 'database')
        if not os.path.exists(dir_database_out):
            os.makedirs(dir_database_out)

        db_path = os.path.join(dir_database_out, survey_info)

        # == Command to execute the conversion using csvs-to-sqlite
        s1 = subprocess.Popen(
            'csvs-to-sqlite '
            + ' '.join([os.path.join(dir_input_dhs_csv_files, 'tables'),
                        os.path.join(dir_input_dhs_csv_files, 'parsed_specs'),
                        db_path]),
            shell=True
        )

        # Wait for the subprocess to complete
        s1.wait()

        print("\nINFO - Successfully generated SQLite database and saved it here: {}".format(dir_database_out))

        # == Now rename tables inside the DB if needed
        filepath_db = ''.join([db_path, '.db'])
        rename_table_names(filepath_db)
    except Exception as err:
        print("ERROR - Failed to generate SQLite database due to \n{}".format(traceback.print_exc()))
