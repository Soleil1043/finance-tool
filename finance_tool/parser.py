# finance_tool/parser.py
import pandas as pd

# 不同银行/平台的列名映射
BANK_FMT = {
    'icbc': {'date': '交易日期', 'amount': '收入金额', 'desc': '交易备注'},
    'cmb': {'date': '记账日期', 'amount': '交易金额', 'desc': '交易摘要'},
    'alipay': {'date': '交易时间', 'amount': '金额', 'desc': '商品说明'},
    'default': {'date': 'Date', 'amount': 'Amount', 'desc': 'Description'}
}

def parse_csv(path, bank='default'):
    """统一列名 → [date, amount, description]"""
    fmt = BANK_FMT.get(bank, BANK_FMT['default'])
    # 自动识别编码
    df = pd.read_csv(path, encoding='utf-8' if bank == 'default' else 'gbk')

    # 重命名列（支持大小写差异 / 中文列名）
    df = df.rename(columns={
        fmt['date']: 'date',
        fmt['amount']: 'amount',
        fmt['desc']: 'description'
    })

    # 类型转换
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # 只保留需要的列，并删除空行
    return df[['date', 'amount', 'description']].dropna()

