import json, pathlib

class SmartCategorizer:
    RULE_FILE = pathlib.Path('data/category_rules.json')
    DEFAULT = {
    "餐饮": ["美团", "饿了么", "肯德基", "星巴克"],
    "购物": ["淘宝", "京东", "拼多多", "超市"],
    "交通": ["滴滴", "地铁", "加油", "高铁"],
    "娱乐": ["电影票", "steam", "游戏"],
    "工资": ["工资", "salary"]
}
    def __init__(self):
        self.rules = json.loads(self.RULE_FILE.read_text()) if self.RULE_FILE.exists() else self.DEFAULT

    def categorize(self, desc:str) -> str:
        desc = desc.lower()
        for cat, kws in self.rules.items():
            if any(kw in desc for kw in kws):
                return cat
        return "其他"

    def add_rule(self, cat, kw):
        self.rules.setdefault(cat,[]).append(kw)
        self.RULE_FILE.write_text(json.dumps(self.rules, ensure_ascii=False))
