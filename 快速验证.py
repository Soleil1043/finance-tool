# 快速验证.py
from finance_tool.models import init_db
from sqlalchemy import text

Session = init_db()          # 返回 sessionmaker
with Session() as session:
    total = session.execute(text("SELECT COUNT(*) FROM transactions")).scalar()
    print("总行数:", total)

    rows = session.execute(text("SELECT date, amount, description FROM transactions LIMIT 5"))
    for row in rows:
        print(row)

