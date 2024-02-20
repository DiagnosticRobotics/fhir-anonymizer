# FHIR Anonymizer

FHIR Anonymizer is a Python package designed to anonymize (FHIR) data contained in Newline Delimited JSON (NDJSON) files. This tool provides a flexible way to remove or obscure personal health information (PHI) to help comply with privacy laws and regulations.

## Features

- Anonymize individual NDJSON files containing FHIR data.
- Batch process multiple NDJSON files within a directory.

## Installation

```bash
git clone https://github.com/DiagnosticRobotics/fhir-anonymizer.git
cd fhir-anonymizer
pip install .
```

## Usage

After installation, the package can be used via the command line or imported into your own Python scripts.

### Command Line

To anonymize a single NDJSON file:

```bash
fhir-anonymizer yourfile.ndjson
```

To process all NDJSON files in a directory:

```bash
fhir-anonymizer /your/folder
```

Optional arguments:

- `--output`: Specify the output file or directory. By default, the tool generates the output file(s) in the same location as the input file(s) with `_anon` appended to the filename before the extension.

### Python Script

```python
from fhir_anonymizer import process_ndjson_file, anonymize_fhir_data

# Define your custom rules
rules = {
   'Patient': 
        {'$.name[*].family': mask(),'$.name[*].given[*]': mask()}
}

# Anonymize a single file
process_ndjson_file('path/to/input.ndjson', 'path/to/output.ndjson', custom_rules=rules)
```

## Custom Rules

### Rule Components Available

The FHIR Anonymizer supports a variety of rule components to meet different anonymization needs. These components can be applied to specific fields within FHIR data.

- **Masking (`mask()`):** Replaces the original value with a fixed mask value to hide sensitive information. This is useful for fields where the specific data is sensitive, such as names and addresses. The mask function can also take an optional argument to replace values with a specific mask value.

- **Hashing (`hash_string()`):** Applies a hash function to the original value, producing a unique string that cannot be easily reversed. This is suitable for identifiers that need to be consistent across records but don't need to be human-readable.

- **Time Shifting (`shift_time()`):** Shifts dates and times to obscure the exact values while maintaining the relative sequence of events. This method is particularly useful for birth dates and event dates, helping to protect age-related information or the timing of medical events.


### Defining Rules

Rules are defined in a Python dictionary, associating FHIR resource types with their corresponding anonymization strategies:

```python
rules = {
    "Patient": 
    {
        '$.name[*].family': mask(),
        '$.name[*].given[*]': mask()
    }
}
```


## Contributing

Contributions to FHIR Anonymizer are welcome! Here's how you can contribute:

- **Issues**: Report bugs or suggest new features by creating issues.
- **Pull Requests**: Submit pull requests with bug fixes or new features.

## License

This project is licensed under the MIT License.
