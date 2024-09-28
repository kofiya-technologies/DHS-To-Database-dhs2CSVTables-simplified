import traceback

from dhs2dbhg.utils.timer import pprint_elapsed_time
from dhs2dbhg.DHS_To_CSVTables import lib02_Unzip_And_Organise_Downloads as dhs2csvtables


@pprint_elapsed_time
def run_conversion_engine(dir_dhs_raw_zipped: str,
                          dir_dhs_output: str,
                          file_format_dhs_raw: str = 'flat',
                          survey_country: str = None,
                          survey_year: int = None
                          ) -> None:
    """
    Executes the conversion of raw DHS (Demographic and Health Surveys) data into a format suitable for database storage (CSVTables).

    This function utilizes and extends an existing Python tool, DHS-To-Database, developed by Harry Gibson
    (https://github.com/harry-gibson/DHS-To-Database). We created a Python library around this tool to make it more accessible and easier
    for users to run DHS data conversions. The default file format for the raw DHS data is set to 'flat'.

    Args:
        dir_dhs_raw_zipped (str): The directory path containing the zipped raw DHS data files.
        dir_dhs_output (str): The directory path where the converted CSV tables will be stored.
        file_format_dhs_raw (str, optional): The file format of the raw DHS data. Only 'flat' type is accepted. Defaults to 'flat'.
        survey_country (str, optional): The country corresponding to the DHS survey data. Defaults to None.
        survey_year (int, optional): The year corresponding to the DHS survey data. Defaults to None.

    Returns:
        None: This function does not return any value. It performs the conversion process and stores the output in the specified directory.

    Raises:
        ValueError: If file_format_dhs_raw is not 'flat'.
        Exception: If any other error occurs during the conversion process, it logs the error using traceback and prints an error message.

    Notes:
        - This function wraps around the `dhs2csvtables.run_dhs2db_lib02()` method to perform the conversion, passing in the required parameters such as
          file paths, file formats, and whether to parse DCFS and data.

        - IMPORTANT: To run conversions for multiple countries, it is recommended to store each zipped raw DHS data file for each country
          in a separate folder, organized by country code and year. For example:
            > D:\\DHS\\FullDHSDatabase\\test\\ET_2005
            > D:\\DHS\\FullDHSDatabase\\test\\ET_2016
            > D:\\DHS\\FullDHSDatabase\\test\\ZA_2015
    """

    # Validation to check if file_format_dhs_raw is 'flat'
    if file_format_dhs_raw != 'flat':
        raise ValueError("ERROR - Invalid file format. Only 'flat' format is accepted.")

    try:
        # === Run the first conversion (from raw DHS data to CSVTables)
        is_conversion_success, conversion_issue_warnings, conversion_issue_errors = dhs2csvtables.run_dhs2db_lib02(
            downloads_file_or_folder=dir_dhs_raw_zipped,
            staging_folder=dir_dhs_output,
            dhs_file_format=file_format_dhs_raw,
            parse_dcfs=True,
            parse_data=True
        )
    except Exception as err:
        print("ERROR - Something went wrong during conversion due to \n{}".format(traceback.print_exc()))



