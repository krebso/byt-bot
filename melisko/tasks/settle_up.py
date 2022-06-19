from __future__ import annotations
from typing import List, Tuple, DefaultDict
from collections import defaultdict

import asyncio


TABLE = List[Tuple[str, List[str], int]]
WALLET = DefaultDict[str, DefaultDict[str, int]]


def create_messages(wallet: WALLET) -> List[str]:
    messages = []

    for debtor, payers in wallet.items():
        for payer in payers:
            amount = wallet[debtor][payer]
            if amount == 0:
                continue
            messages.append(f"{debtor} owes {payer}: {amount} czk")

    return messages


def settle_up(table: TABLE) -> WALLET:

    # key: person who paid
    # value: tuple of list of people who owe and amount owed

    wallet = defaultdict(lambda: defaultdict(int))

    for payer, debtors, amount in table:
        # debtors.append(payer)
        
        debt_share = amount / (len(debtors) + 1) # payer sets the amount without his share

        for debtor in debtors:
            wallet[debtor][payer] += debt_share

    for debtor, payers in wallet.items():
        for payer in payers:
            my_debt = wallet[debtor][payer]
            payer_debt = wallet[payer][debtor]

            if my_debt <= payer_debt:
                wallet[payer][debtor] -= my_debt
                wallet[debtor][payer] = 0

    return wallet


