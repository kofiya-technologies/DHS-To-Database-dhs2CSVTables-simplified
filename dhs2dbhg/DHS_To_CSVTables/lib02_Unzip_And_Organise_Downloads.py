"""

DISCLAIMER - This part of the code "dhs_to_database_webapp/DHS_To_CSVTables" is taken from
https://github.com/harry-gibson/DHS-To-Database by Harry Gibson. The main contribution of our solution is to bring this
great tool to a bigger audience. We believe that this WebApp helps non-Python users to easily convert their DHS survey
raw data to relational database.

"""

import os
import zipfile
import re
import fnmatch
import traceback

from dhs2dbhg.utils.timer import pprint_elapsed_time
from dhs2dbhg.DHS_To_CSVTables.cspro_parser.DCF_Parser import DCF_Parser
from dhs2dbhg.DHS_To_CSVTables.cspro_parser.DAT_Parser import parse_dat_file


DHS_CONVERSION_CODE_ERRORS = {
    1: "LINE=ASSERT_FLAT - Invalid file format. Only FLAT file format is allowed for conversion. Sorry!",
    2: "LINE=dcf_files - Only FLAT file format is allowed for conversion. Sorry!",
    3: "LINE=dat_files - Only FLAT file format is allowed for conversion. Sorry!"
}


@pprint_elapsed_time
def unzip_and_sort(zip_path, survey_num, out_folder):
    """Extracts the root contents of the zipfile zip_path to a folder out_folder/survey_num, prepending
    'survey_num.' to each extracted filename"""
    if str.lower(zip_path).find('.zip') == -1:
        raise ValueError("Apparently not a zip file")
    out_dir = os.path.join(out_folder, survey_num)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    output_files = []
    with zipfile.ZipFile(zip_path) as zf:
        name_list = zf.namelist()
        for zipped_file in name_list:
            if zipped_file.endswith('/'):
                continue
            zipped_file_filename = zipped_file.split('/')[-1]
            unzipped_filename = '.'.join((survey_num, zipped_file_filename))
            unzipped_fn_path = os.path.join(out_dir, unzipped_filename)
            if not os.path.exists(unzipped_fn_path):
                # print(' -> '.join((zipped_file, unzipped_fn_path)))

                out_file = zf.extract(zipped_file, out_dir)
                os.rename(out_file, unzipped_fn_path)
            output_files.append(unzipped_fn_path)
    return output_files


@pprint_elapsed_time
def parse_download_spec(download_urls_file):
    """Parse the text file of download URLs provided by the DHS download manager to extract
    the downloaded filename and the numerical survey id it corresponds to, return dictionary
    mapping the local filename to numerical survey id."""
    results = {}

    try:
        with open(file=download_urls_file, mode='r') as url_file:
            for line in url_file:
                print("INFO - LINE: {}".format(line))

                params = line.split('?')[1]
                fn, tp, ctry, survid, _, _ = params.split('&')
                filename = fn.split('=')[1].upper()
                # ctry_code = ctry.split('=')[1].upper()
                survey_num = survid.split('=')[1]
                results[filename] = survey_num
        return results
    except Exception as err:
        print("ERROR - Failed to parse file due to {}".format(traceback.print_exc()))

        return None


@pprint_elapsed_time
def organise_batch_downloaded(download_urls_list, staging_folder,
                              conversion_issue_warnings=None):
    
    survey_num_mapping = parse_download_spec(download_urls_list)

    downloaded_files_folder = os.path.dirname(download_urls_list)
    extracted_files_folder_root = os.path.join(staging_folder, "downloaded")
    
    all_files = [
        i for i in os.listdir(downloaded_files_folder) if os.path.isfile(os.path.join(downloaded_files_folder, i))
    ]
    regex = re.compile(fnmatch.translate('*.zip'), re.IGNORECASE)
    in_files = [os.path.join(downloaded_files_folder, j) for j in all_files if re.match(regex, j)]
    # need to be case insensitive https://stackoverflow.com/a/12213141
    # in_files = glob.glob(os.path.join(downloaded_files_folder, "*.zip"))

    all_unzipped_files = []
    for f in in_files:
        basename = os.path.basename(f).upper()
        if basename not in survey_num_mapping:
            conversion_issue_warnings.extend(
                ["Details not found for existing file {}, skipping".format(basename)]
            )
            # print("WARNING - Details not found for existing file {}, skipping".format(basename))

            continue

        survey_num = survey_num_mapping[basename]
        unzipped_files = unzip_and_sort(f, survey_num, extracted_files_folder_root)
        all_unzipped_files.extend(unzipped_files)
    in_files_upper = [os.path.basename(f).upper() for f in in_files]
    missing = [f for f in survey_num_mapping.keys() if f not in in_files_upper]
    for m in missing:
        conversion_issue_warnings.extend(
            ["{} has not been downloaded, skipping".format(m)]
        )
        # print("WARNING - {} has not been downloaded, skipping".format(m))

    return all_unzipped_files, conversion_issue_warnings


@pprint_elapsed_time
def organise_manual_downloaded(downloaded_files_folder, staging_folder):
    all_files = [
        i for i in os.listdir(downloaded_files_folder) if os.path.isfile(os.path.join(downloaded_files_folder, i))
    ]
    regex = re.compile(fnmatch.translate('*.zip'), re.IGNORECASE)
    in_files = [os.path.join(downloaded_files_folder, j) for j in all_files if re.match(regex, j)]
    # in_files = glob.glob(os.path.join(downloaded_files_folder, "*.ZIP"))
    all_unzipped_files = []
    extracted_files_folder_root = os.path.join(staging_folder, "downloaded")
    for f in in_files:
        filename = os.path.basename(f)
        survey_num = filename.split(".")[0]
        unzipped_files = unzip_and_sort(f, survey_num, extracted_files_folder_root)
        all_unzipped_files.extend(unzipped_files)
    return all_unzipped_files


def get_filecode(filename):
    return os.path.extsep.join(os.path.basename(filename).split(os.path.extsep)[:-1])


def get_new_name(old_name):
    pattern = r'\.[A-Z]{2}([A-Z]{2,3})[\dA-Z]+FL\.'
    match = re.search(pattern, old_name)  # TODO - Expects a flat (FL) file!

    if match:
        prefix = match.group(1)
        if "RECORD1" in old_name:
            return f"{prefix}_main.csv"
        elif "FlatRecordSpec" in old_name:
            return f"{prefix}_variable.csv"
        elif "FlatValuesSpec" in old_name:
            return f"{prefix}_recode.csv"
        elif "RelationshipsSpec" in old_name:
            return f"{prefix}_relationshipSpec.csv"
        elif "HWREC" in old_name:
            return f"{prefix}_hwrec.csv"
        elif "FWRECORD" in old_name:
            return f"{prefix}_fwrecord.csv"
    return None


@pprint_elapsed_time
def run_dhs2db_lib02(downloads_file_or_folder, staging_folder, dhs_file_format, parse_dcfs=False, parse_data=False):
    try:
        conversion_issue_warnings = []
        conversion_issue_errors = []
        is_conversion_success = False

        if dhs_file_format != 'flat':
            conversion_issue_errors.extend([DHS_CONVERSION_CODE_ERRORS[0]])
            print("ERROR - LINE=ASSERT_FLAT - Invalid file format={}. Only FLAT file format is allowed for conversion. Sorry!".format(dhs_file_format))

            is_conversion_success = False

            return is_conversion_success, conversion_issue_warnings, conversion_issue_errors

        print("\nINFO [FIRST CONVERSION] - Converting raw (zipped) DHS raw data into CSV tables...")

        # Conversion
        if os.path.isfile(downloads_file_or_folder):
            unzipped, conversion_issue_warnings = organise_batch_downloaded(
                downloads_file_or_folder, staging_folder, conversion_issue_warnings
            )
        else:
            unzipped = organise_manual_downloaded(
                downloads_file_or_folder, staging_folder
            )

        dcf_files = [f for f in unzipped if f.lower().endswith('.dcf')]
        dat_files = [f for f in unzipped if f.lower().endswith('.dat')]

        # Check if FLAT files are idenfified
        if not dcf_files:
            conversion_issue_errors.extend([DHS_CONVERSION_CODE_ERRORS[2]])
            # print("ERROR - LINE=dcf_files - Only FLAT file format is allowed for conversion. Sorry!")

            is_conversion_success = False

            return is_conversion_success, conversion_issue_warnings, conversion_issue_errors

        if not dat_files:
            conversion_issue_errors.extend([DHS_CONVERSION_CODE_ERRORS[3]])
            # print("ERROR - LINE=dat_files - Only FLAT file format is allowed for conversion. Sorry!")

            is_conversion_success = False

            return is_conversion_success, conversion_issue_warnings, conversion_issue_errors

        # Process
        parsed_spec_folder = os.path.join(staging_folder, "parsed_specs")
        parsed_data_folder = os.path.join(staging_folder, "tables")

        if parse_dcfs:
            for dcf_file in dcf_files:
                parser = DCF_Parser(dcf_file, parsed_spec_folder)
                if parser.done():
                    # print("{} is already done, skipping".format(dcf_file))

                    continue

                conversion_issue_warnings = parser.parse(conversion_issue_warnings=conversion_issue_warnings)
                parser.write()

        if parse_data:
            for dat_file in dat_files:
                filecode = get_filecode(dat_file)
                spec_file = os.path.join(parsed_spec_folder, f"{filecode}.FlatRecordSpec.csv")
                # all surveys have a REC01 table so see if this exists
                test_output_fn = os.path.join(parsed_data_folder, f"{filecode}.REC01.csv")
                if os.path.exists(test_output_fn):
                    # print("{} already parsed to datafiles, skipping".format(filecode))

                    continue

                parse_dat_file(dat_file, spec_file, parsed_data_folder,
                               conversion_issue_warnings=conversion_issue_warnings)

        # === Rename lengthy filenames to easily query in SQLite database
        # Metadata
        for old_fname in os.listdir(parsed_spec_folder):
            new_fname = get_new_name(old_fname)
            if new_fname:
                try:
                    os.rename(src=os.path.join(parsed_spec_folder, old_fname),
                              dst=os.path.join(parsed_spec_folder, new_fname))
                except FileNotFoundError:
                    print(f"File '{old_fname}' not found.")
                except Exception as e:
                    print(f"Error renaming '{old_fname}' to '{new_fname}': {e}")
            else:
                print(f"No mapping found for '{old_fname}'")

        # Tables
        for old_fname in os.listdir(parsed_data_folder):
            new_fname = get_new_name(old_fname)
            if new_fname:
                try:
                    os.rename(src=os.path.join(parsed_data_folder, old_fname),
                              dst=os.path.join(parsed_data_folder, new_fname))
                except FileNotFoundError:
                    print(f"File '{old_fname}' not found.")
                except Exception as e:
                    print(f"Error renaming '{old_fname}' to '{new_fname}': {e}")
            else:
                print(f"No mapping found for '{old_fname}'")

        is_conversion_success = True

        return is_conversion_success, conversion_issue_warnings, conversion_issue_errors
    except Exception as err:
        print('ERROR - Failed during DHS-To-Database conversion process due to {}'.format(traceback.print_exc()))

        return False, None, None