from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse


@dataclass
class RevolutEntry:
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
                return float(value.strip())
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
