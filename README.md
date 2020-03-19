# revolut_to_homebank

Script converting Revolut statement exports to [homebank csv format](http://homebank.free.fr/help/misc-csvformat.html#txn)

## Installation

Clone the repository and run
```bash
pip install .
```

## Usage

### rev2hb

If installed, `rev2hb` should be available in your path.

```bash
rev2hb -o <output-file> <source-file>
```

If `-o` is omitted output will be written to `output.csv` in the current directory

### Native python

You need python3.7 with `python_dateutils` installed to run this script. 
```bash
python <revolut-export.csv>
```
Script accepts filepath as a first parameter and writes ouput to `output.csv` in current directory
