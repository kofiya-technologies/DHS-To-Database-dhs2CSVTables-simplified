from dhs2dbhg.conversion_engine import run_conversion_engine


if __name__ == '__main__':
    # === Run conversion
    dir_dhs_raw_data = r'D:\DHS\FullDHSDatabase\test\ET_2005'
    dhs_raw_data_file_format = 'flat'   # IMPORTANT - Only FLAT file types are supported to perform first conversion!!!
    survey_country = 'ethiopia'
    survey_year = 2005

    run_conversion_engine(
        dir_dhs_raw_zipped=dir_dhs_raw_data,
        dir_dhs_output=dir_dhs_raw_data,
        file_format_dhs_raw=dhs_raw_data_file_format,
        survey_country=survey_country,
        survey_year=survey_year
    )