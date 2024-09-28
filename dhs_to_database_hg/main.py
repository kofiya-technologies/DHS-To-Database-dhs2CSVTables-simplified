import time
import traceback

from funcy import print_durations

from dhs_to_database_hg.DHS_To_CSVTables import lib02_Unzip_And_Organise_Downloads as dhs2csvtables


@print_durations
def run(dir_dhs_raw_zipped: str,
        dir_dhs_output: str,
        file_format_dhs_raw: str,
        survey_country: str = None,
        survey_year: int = None
        ) -> None:
    """
    IMPORTANT - To run conversion for multiple countries, better to store each zipped raw dhs data per country in a
    separate folder as:
        > D:\DHS\FullDHSDatabase\test\ET_2005
        > D:\DHS\FullDHSDatabase\test\ET_2016
        > D:\DHS\FullDHSDatabase\test\ZA_2015

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
    except Exception as err:
        print("ERROR - Failed to perform DHS-To-Database conversion due to {}".format(traceback.print_exc()))


if __name__ == '__main__':
    # === Config
    DIR_DHS_MANUAL_PROJECT = r'D:\DHS\FullDHSDatabase\test\ET_2005'
    DHS_FILE_FORMAT = 'flat'   # IMPORTANT - Only FLAT file types are supported to perform first conversion!!!
    SURVEY_COUNTRY = 'et'
    SURVEY_YEAR = 2005

    # === Start conversion
    run(
        dir_dhs_raw_zipped=DIR_DHS_MANUAL_PROJECT,
        dir_dhs_output=DIR_DHS_MANUAL_PROJECT,
        file_format_dhs_raw=DHS_FILE_FORMAT,
        survey_country=SURVEY_COUNTRY,
        survey_year=SURVEY_YEAR
    )
