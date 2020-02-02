import csv
import sys
from dataclasses import asdict

from models import RevolutEntry, HomeBankEntry


def main(input_file, delimiter=';'):
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
                hb_entry = convert_to_homebank(row)
                print(hb_entry)
                hb_entries.append(convert_to_homebank(row))

                line_count += 1
        print(f'Processed {line_count} lines.')

    with open("output.csv", 'w') as output_file:
        writer = csv.writer(output_file, delimiter=delimiter)
        writer.writerows([asdict(hb_entry).values() for hb_entry in hb_entries])


def convert_to_homebank(row):
    revolut_entry = RevolutEntry.from_row(row)
    print(revolut_entry)
    return HomeBankEntry.from_revolutentry(revolut_entry)


if __name__ == '__main__':
    main(sys.argv[1])
