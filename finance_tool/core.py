from sqlalchemy.orm import Session
from .models import Transaction, Category
from .categorizer import SmartCategorizer

class FinanceRepo:
    def __init__(self, session:Session):
        self.s = session
        self.cat = SmartCategorizer()

    def import_df(self, df):
        added = 0
        for _,r in df.iterrows():
            if self.s.query(Transaction).filter_by(date=r['date'].date(),
                                                   amount=r['amount'],
                                                   description=r['description']).first():
                continue
            cat_name = self.cat.categorize(r['description'])
            cat = self.s.query(Category).filter_by(name=cat_name).first() or Category(name=cat_name)
            self.s.add(Transaction(date=r['date'].date(), amount=r['amount'],
                                   description=r['description'], category=cat))
            added += 1
        self.s.commit()
        return added
