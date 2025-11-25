# finance_tool/reports.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import font_manager
from sqlalchemy.orm import Session

# 设置中文字体
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False

class ReportGen:
    def __init__(self, session: Session):
        self.session = session

    def monthly_flow(self, year):
        """返回年度各月收支 DataFrame"""
        sql = """
        SELECT strftime('%Y-%m', date) as month,
               SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
               SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS expense
        FROM transactions
        WHERE strftime('%Y', date) = :year
        GROUP BY month
        ORDER BY month
        """
        return pd.read_sql(sql, self.session.bind, params={'year': str(year)})

    def expense_pie(self, year, month):
        """指定年月支出分类饼图 → matplotlib Figure"""
        sql = """
        SELECT c.name, ABS(SUM(t.amount)) AS total
        FROM transactions t
        JOIN categories c ON t.category_id = c.id
        WHERE strftime('%Y-%m', t.date) = :ym AND t.amount < 0
        GROUP BY c.name
        ORDER BY total DESC
        """
        df = pd.read_sql(sql, self.session.bind, params={'ym': f'{year}-{month:02d}'})
        if df.empty:
            return None

        fig, ax = plt.subplots(figsize=(4, 4))
        # 中文标签 + 百分比
        wedges, texts, autotexts = ax.pie(df['total'], labels=df['name'],
                                          autopct='%1.1f%%',
                                          startangle=90,
                                          colors=sns.color_palette('Set3', n_colors=len(df)))
        # 文字大小
        for t in texts + autotexts:
            t.set_fontsize(10)
        ax.set_title(f'{year} 年 {month} 月 支出分布', fontsize=12)
        return fig

