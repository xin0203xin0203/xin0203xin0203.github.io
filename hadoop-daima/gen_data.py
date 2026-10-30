import random, csv

random.seed(42)

SHOPS = ["数码优选旗舰店", "极客数码专营店", "星辰家居旗舰店", "悦动运动专营店", "简衣女装店",
         "潮男服饰旗舰店", "康健保健专营店", "味道食品旗舰店", "萌宠生活馆", "文具办公专营店",
         "母婴优选旗舰店", "美妆护肤专营店", "车品配件旗舰店", "户外运动装备店", "厨房电器专营店",
         "手机配件专营店", "图书音像旗舰店", "家纺布艺专营店", "智能家电旗舰店", "日用百货超市"]
CATS = ["手机", "蓝牙耳机", "笔记本电脑", "运动鞋", "纯棉T恤", "每日坚果", "猫粮", "笔记本",
        "婴儿奶粉", "面霜", "车载充电器", "户外帐篷", "电饭煲", "数据线", "小说",
        "四件套", "扫地机器人", "抽纸", "平板电脑", "保温杯"]
TAGS = ["旗舰版", "2024新款", "爆款", "限时特惠", "官方正品", "高性价比", "热销款", "升级款"]
HEADER = ["shop", "category", "title", "price", "sales", "comments", "crawl_date"]

clean_rows = []
for _ in range(100000):
    shop = random.choice(SHOPS)
    cat = random.choice(CATS)
    clean_rows.append([shop, cat, shop[:2] + cat + random.choice(TAGS),
                       round(random.uniform(19, 2999), 2), random.randint(0, 500),
                       random.randint(0, 9999),
                       "2023-{:02d}-{:02d}".format(random.randint(1, 9), random.randint(1, 28))])

dirty = [list(r) for r in clean_rows]
dup = miss = abn = 0
for _ in range(3000):
    dirty.append(list(random.choice(clean_rows))); dup += 1
for i in random.sample(range(len(dirty)), 4000):
    dirty[i][4 if random.random() < 0.5 else 3] = ""; miss += 1
for i in random.sample(range(len(dirty)), 3000):
    dirty[i][3] = random.choice(["-1", "0", "999999"]); abn += 1

with open("products_raw.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(HEADER); w.writerows(dirty)

seen_set = set(); seen = []
for row in dirty:
    key = tuple(row)
    if key in seen_set: continue
    seen_set.add(key); seen.append(row)

cleaned = []
for row in seen:
    if row[3] == "" or row[4] == "": continue
    try:
        price = float(row[3]); sales = int(row[4])
    except ValueError:
        continue
    if price <= 0 or price > 9999 or sales < 0: continue
    cleaned.append(row)

with open("products_clean.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f); w.writerow(HEADER); w.writerows(cleaned)

print("原始行数（含表头）:", len(dirty) + 1)
print("注入：重复 %d / 缺失 %d / 异常 %d" % (dup, miss, abn))
print("清洗后行数（含表头）:", len(cleaned) + 1)
print("丢弃比例: %.1f%%" % (100.0 * (1 - len(cleaned) / float(len(dirty)))))
