# DHS-To-Database-dhs2CSVTables-simplified

This repository provides an easy-to-use Python wrapper around the original `DHS-To-Database` tool developed by [Harry Gibson](https://github.com/harry-gibson/DHS-To-Database). The goal of this tool is to simplify the conversion of raw DHS (Demographic and Health Surveys) data into a format suitable for database storage, specifically in CSVTables format.

## Features

- **Convenient Wrapper**: We built a Python wrapper function to make it easier to run DHS data conversions without diving deep into the original library’s internals.

## Requirements

- **Python 3.8 and above**

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/kofiya-technologies/DHS-To-Database-dhs2CSVTables-simplified.git
   ```

2. Install dependencies using `pipenv`:
   ```bash
   pipenv install --deploy --ignore-pipfile
   ```

## Usage

You can use the `run_conversion_engine` function to convert raw DHS data into CSV tables. Here's a quick example:

```python
from dhs2csvtables.conversion_engine import run_conversion_engine

# == Define the paths for raw DHS data and the output directory
dir_dhs_raw_data = r'D:\DHS\FullDHSDatabase\test\ET_2005'
dhs_raw_data_file_format = 'flat'   # IMPORTANT - Only FLAT file types are supported to perform first conversion!!!
survey_country = 'ethiopia'
survey_year = 2005

# == Run conversion
run_conversion_engine(
    dir_dhs_raw_zipped=dir_dhs_raw_data,
    dir_dhs_output=dir_dhs_raw_data,
    file_format_dhs_raw=dhs_raw_data_file_format,
    survey_country=survey_country,
    survey_year=survey_year
)
```

### Arguments

- `dir_dhs_raw_zipped` (str): Directory path containing the zipped raw DHS data files.
- `dir_dhs_output` (str): Directory where the converted CSV tables will be saved.
- `file_format_dhs_raw` (str, optional): File format of the raw DHS data. Only `'flat'` is supported. Defaults to `'flat'`.
- `survey_country` (str, optional): Country name for the DHS survey. Defaults to `None`.
- `survey_year` (int, optional): Year of the DHS survey. Defaults to `None`.

### Important Notes

- Only the `flat` file format is supported.
- It is recommended to organize DHS raw data files by country and year, placing each survey in a separate folder. Example structure:
  ```
  D:\DHS\FullDHSDatabase\test\ET_2005
  D:\DHS\FullDHSDatabase\test\ET_2016
  D:\DHS\FullDHSDatabase\test\ZA_2015
  ```

## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

This tool is built upon the amazing work of [Harry Gibson](https://github.com/harry-gibson) and his `DHS-To-Database` tool.