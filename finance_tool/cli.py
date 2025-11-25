import argparse, pandas as pd
from .models import init_db
from .core import FinanceRepo

def main():
    parser = argparse.ArgumentParser(description='个人财务工具')
    parser.add_argument('file', help='CSV 路径')
    parser.add_argument('-b', '--bank', default='default', help='银行格式')
    args = parser.parse_args()

    from .parser import parse_csv
    df = parse_csv(args.file, args.bank)

    engine = init_db()
    with engine() as sess:
        repo = FinanceRepo(sess)
        n = repo.import_df(df)
        print(f'✅ 新增 {n} 条记录')

if __name__ == '__main__':
    main()
