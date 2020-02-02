# revolut_to_homebank

Script converting Revolut statement exports to [homebank csv format](http://homebank.free.fr/help/misc-csvformat.html#txn)

## Usage

You need python3.7 with `python_dateutils` installed to run this script. 
```bash
python <revolut-export.csv>
```
Script accepts filepath as a first parameter and writes ouput to `output.csv` in current directory
