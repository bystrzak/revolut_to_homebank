from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse, parserinfo


@dataclass
class Entry:
    pass


@dataclass
class RevolutEntry(Entry):
    date: datetime
    description: str
    paid_out: float
    paid_in: float
    exchange_out: str
    exchange_in: str
    balance: float
    category: str
    notes: str

    @classmethod
    def from_row(cls, row):
        def str_to_float(value: str):
            if value:
                return float(value.strip().replace(',', ''))
            else:
                return None

        return cls(
            date=parse(row[0]),
            description=row[1].strip(),
            paid_out=str_to_float(row[2]),
            paid_in=str_to_float(row[3]),
            exchange_out=row[4].strip(),
            exchange_in=row[5].strip(),
            balance=row[6],
            category=row[7],
            notes=row[8],
        )


@dataclass
class MBankPLEntry(Entry):
    date: datetime
    description: str
    source_account: str
    category: str
    amount: float

    @classmethod
    def from_row(cls, row):
        def str_to_float(value: str) -> [float, None]:
            if value:
                return float(value.replace(' ', '').replace(',', '.').replace('PLN', '').strip())
            else:
                return None

        def remove_multiple_whitespaces(string: str) -> str:
            return ' '.join(string.split())

        return cls(
            date=parse(row[0]),
            description=remove_multiple_whitespaces(row[1]),
            source_account=row[2].strip(),
            category=row[3],
            amount=str_to_float(row[4]),
        )

@dataclass
class NestBankEntry(Entry):
    date: datetime
    type: str
    amount: float
    currency: str
    payee: str
    payee_acc_no: str
    description: str
    balance: float

    @classmethod
    def from_row(cls, row):
        def str_to_float(value: str) -> [float, None]:
            if value:
                return float(value.replace(' ', '').replace(',', '.').strip())
            else:
                return None

        return cls(
            date=parse(row[1], parserinfo=parserinfo(dayfirst=True)),
            type=row[2],
            amount=str_to_float(row[3]),
            currency=row[4],
            payee=row[5],
            payee_acc_no=row[6],
            description=row[7],
            balance=row[8],
        )


@dataclass
class HomeBankEntry:
    date: datetime
    payment_type: int
    info: str
    payee: str
    memo: str
    amount: float
    category: str
    tags: str

    @classmethod
    def from_entry(cls, entry: Entry):
        if isinstance(entry, RevolutEntry):
            return cls.from_revolutentry(entry)
        elif isinstance(entry, MBankPLEntry):
            return cls.from_mbankplentry(entry)
        elif isinstance(entry, NestBankEntry):
            return cls.from_nestbankentry(entry)

    @classmethod
    def from_revolutentry(cls, revolut_entry: RevolutEntry):
        def calculate_amount():
            if revolut_entry.paid_out:
                return -1 * revolut_entry.paid_out
            elif revolut_entry.paid_in:
                return revolut_entry.paid_in

        def get_payment_type():
            if revolut_entry.paid_in and revolut_entry.exchange_out:
                return 4
            else:
                return 5

        return cls(
            date=revolut_entry.date,
            payment_type=get_payment_type(),
            info=revolut_entry.notes,
            payee='',
            memo=revolut_entry.description,
            amount=calculate_amount(),
            category=revolut_entry.category,
            tags='',
        )

    @classmethod
    def from_mbankplentry(cls, mbankpl_entry: MBankPLEntry):
        return cls(
            date=mbankpl_entry.date,
            payment_type=5,
            info='BA',
            payee=mbankpl_entry.description,
            memo=mbankpl_entry.description,
            amount=mbankpl_entry.amount,
            category='',
            tags='',
        )

    @classmethod
    def from_nestbankentry(cls, nestbank_entry: NestBankEntry):
        return cls(
            date=nestbank_entry.date,
            payment_type=5,
            info='BA',
            payee=nestbank_entry.payee,
            memo=nestbank_entry.description,
            amount=nestbank_entry.amount,
            category='',
            tags='',
        )