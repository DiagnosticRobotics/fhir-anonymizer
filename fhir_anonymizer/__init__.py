import json
from jsonpath_ng import  parse
from tqdm import tqdm
from fhir_anonymizer.rules import rules
import click
import os


def anonymize_fhir_data(fhir_json, rules):
    """
    Anonymize FHIR data based on provided rules.
    """
    for (path,rule) in rules.items():
        jsonpath_expr = parse(path)
        jsonpath_expr.find(fhir_json)
        jsonpath_expr.update(fhir_json, rule)
    return fhir_json


def process_ndjson_file(input_file_path, output_file_path, custom_rules=None):
    """
    Process an NDJSON file to anonymize FHIR data based on provided rules.
    """
    if custom_rules is None:
        custom_rules = {}
    process_rules = {**rules, **custom_rules}
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file, \
         tqdm(total=os.path.getsize(input_file_path)) as pbar:
        for line in input_file:
            fhir_json = json.loads(line)
            pbar.update(len(line))
            resource_type =  fhir_json['resourceType']
            anonymized_fhir_json = anonymize_fhir_data(fhir_json, process_rules[resource_type])
            json.dump(anonymized_fhir_json, output_file)
            output_file.write('\n')


@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(), help='Path to the output NDJSON file. Optional.')
def main(input, output):
    """
    Process a single NDJSON file or all NDJSON files in a given folder.
    """
    if os.path.isdir(input):
        anon_dir = os.path.join(input, "anon")
        os.makedirs(anon_dir, exist_ok=True)

        for filename in os.listdir(input):
            if filename.endswith(".ndjson"):
                input_file_path = os.path.join(input, filename)
                output_file_path = os.path.join(anon_dir, f"{os.path.splitext(filename)[0]}.ndjson")
                click.echo(f"Processing {filename} into {output_file_path}...")
                process_ndjson_file(input_file_path, output_file_path)
    elif os.path.isfile(input):
        # Process a single file
        if not output:
            # Generate output path if not specified
            base, ext = os.path.splitext(input)
            output = f"{base}_anon{ext}"
        click.echo(f"Processing {os.path.basename(input)}...")
        process_ndjson_file(input, output)
    else:
        click.echo("Input is not a file or directory.")

if __name__ == "__main__":
    main()