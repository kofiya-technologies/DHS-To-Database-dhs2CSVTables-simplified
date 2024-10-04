# Changelog

## [v0.2.0] - 2024-10-04
### Added
- **CSV to SQLite Conversion**: Introduced a new feature to convert relational CSV tables generated from DHS raw data into a SQLite database.
  - The new `csv2sqlite` function takes CSV files in a directory and uses the `csvs-to-sqlite` tool to create a relational SQLite database.
  - It outputs the database into a `database` subdirectory within the input directory.
  - The function also captures any errors during the process and outputs detailed traceback information.

### Changed
- Refactored the conversion pipeline to include both the initial CSV conversion and the new SQLite database generation functionality.


## [v0.1.0] - 2024-09-29
### Added
- **Initial Migration**: Migrated Harry Gibson's original `DHS-To-Database` tool to a simplified version for easier conversion of DHS raw data into CSV tables.
