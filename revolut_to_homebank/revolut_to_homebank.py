import argparse
import csv
from dataclasses import asdict
from enum import Enum

from revolut_to_homebank.models import RevolutEntry, HomeBankEntry, MBankPLEntry


class ConverterType(Enum):
    REVOLUT = 'revolut'
    MBANKPL = 'mbankpl'


def get_converter(export_type, input_file):
    if not export_type:
        print("Type not provided")
        if 'lista_operacji' in input_file:
            export_type = ConverterType.MBANKPL.value
        elif 'Revolut' in input_file:
            export_type = ConverterType.REVOLUT.value
        print("Guessed", export_type)

    if export_type == ConverterType.REVOLUT.value:
        return RevolutEntry
    elif export_type == ConverterType.MBANKPL.value:
        return MBankPLEntry


def convert(input_file, export_type, output_file="output.csv", delimiter=';'):
    converter = get_converter(export_type, input_file)

    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delimiter, skipinitialspace=True)
        line_count = 0
        hb_entries = list()
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(row)
                hb_entry = convert_to_homebank(row, converter)
                print(hb_entry)
                hb_entries.append(convert_to_homebank(row, converter))

                line_count += 1
        print(f'Processed {line_count} lines.')

    with open(output_file, 'w') as output_file:
        writer = csv.writer(output_file, delimiter=delimiter)
        writer.writerows([asdict(hb_entry).values() for hb_entry in hb_entries])


def convert_to_homebank(row, converter):
    entry = converter.from_row(row)
    print(entry)
    return HomeBankEntry.from_entry(entry)


def main():
    parser = argparse.ArgumentParser(description='revolut_to_homebank.py')
    parser.add_argument('source', metavar='filepath', type=str, help='file tp be converted')
    parser.add_argument('-t', '--type', metavar='type', choices=[e.value for e in ConverterType], help='type of input')
    parser.add_argument('-o', '--output', metavar='filename', default='output.csv', help='filename output name')
    parser.add_argument('-d', '--delimiter', metavar='delimiter', default=';', help='delimiter')

    args = parser.parse_args()
    convert(args.source, args.type, output_file=args.output, delimiter=args.delimiter)


if __name__ == '__main__':
    main()
