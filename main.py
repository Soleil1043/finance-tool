import pandas as pd

def main():
    df = pd.read_csv('data/sample_bill.csv', parse_dates=['Date'])
    print("✅ 读取成功！")
    print("📊 总行数:", len(df))
    print("💰 净余额:", df['Amount'].sum())
    print("\n前 5 行：")
    print(df.head())

if __name__ == "__main__":
    main()
