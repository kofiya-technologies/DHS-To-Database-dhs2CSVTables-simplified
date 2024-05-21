import os
import time
import subprocess
import traceback

from funcy import print_durations

from dhs_to_database_hg.DHS_To_CSVTables import lib02_Unzip_And_Organise_Downloads as dhs2csvtables


@print_durations
def create_sqlite_dhs_database(dir_dhs_output, filename_database):
    dir_database_out = os.path.join(dir_dhs_output, 'database')
    if not os.path.exists(dir_database_out):
        os.makedirs(dir_database_out)

    s1 = subprocess.Popen(
        'csvs-to-sqlite '
        + ' '.join([os.path.join(dir_dhs_output, 'tables'),
                    os.path.join(dir_dhs_output, 'parsed_specs'),
                    os.path.join(dir_database_out, filename_database)]),
        shell=True
    )

    s1.wait()


def run(survey_country, survey_year, dir_dhs_raw_zipped, dir_dhs_output, file_format_dhs_raw):
    """
    IMPORTANT - To run conversion for multiple countries, better to store each zipped raw dhs data per country in a
    separate folder as D:\DHS\FullDHSDatabase\test\ET_2005, D:\DHS\FullDHSDatabase\test\ET_2016, ZA_2015, etc

    """

    try:
        # === Run the first conversion (from raw DHS data to CSVTables)
        is_conversion_success, conversion_issue_warnings, conversion_issue_errors = dhs2csvtables.run(
            downloads_file_or_folder=dir_dhs_raw_zipped,
            staging_folder=dir_dhs_output,
            dhs_file_format=file_format_dhs_raw,
            parse_dcfs=True,
            parse_data=True
        )

        # === Run the second conversion (from CSVTables to SQLite database)
        if is_conversion_success:
            print("\nINFO [SECOND CONVERSION] - Creating SQLite DHS database...")

            filename_database = ''.join([survey_country, '_', survey_year, '.db'])
            create_sqlite_dhs_database(dir_dhs_output=dir_dhs_output, filename_database=filename_database)
    except Exception as err:
        print("ERROR - Failed to perform DHS-To-Database conversion due to {}".format(traceback.print_exc()))


if __name__ == '__main__':
    # === Config
    SURVEY_COUNTRY = 'et'
    SURVEY_YEAR = '2016'
    DIR_DHS_MANUAL_PROJECT = r'D:\DHS\FullDHSDatabase\test\ET_2016'
    DHS_FILE_FORMAT = 'flat'   # ATTENTION - Only FLAT file types are supported to perform first conversion!!!

    # === Start conversion
    t_s = time.time()

    run(survey_country=SURVEY_COUNTRY,
        survey_year=SURVEY_YEAR,
        dir_dhs_raw_zipped=DIR_DHS_MANUAL_PROJECT,
        dir_dhs_output=DIR_DHS_MANUAL_PROJECT,
        file_format_dhs_raw=DHS_FILE_FORMAT
        )

    print("INFO - Elapsed time to execute task (mins): {}".format(round((time.time() - t_s) / 60, 2)))