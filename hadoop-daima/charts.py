import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.sans-serif"] = ["Noto Sans CJK JP", "Noto Sans CJK SC", "WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["figure.dpi"] = 150

BLUE = "#1F4E79"

top = pd.read_csv("pandas_shop_top.csv").head(10)

# 图1 横向柱状图：TOP10 销量
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top["shop"][::-1], top["total_sales"][::-1], color=BLUE)
ax.set_xlabel("累计销量（件）")
ax.set_title("店铺累计销量 TOP 10")
for i, v in enumerate(top["total_sales"][::-1]):
    ax.text(v, i, " %d" % v, va="center", fontsize=8)
plt.tight_layout()
plt.savefig("charts/1-top10-sales.png")
plt.close()

# 图2 饼图：销售额占比
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(top["total_gmv"], labels=top["shop"], autopct="%1.1f%%",
       startangle=90, textprops={"fontsize": 8})
ax.set_title("店铺销售额占比（TOP 10）")
plt.tight_layout()
plt.savefig("charts/2-gmv-pie.png")
plt.close()

# 图3 直方图：商品价格分布
df = pd.read_csv("products_clean.csv")
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.hist(df["price"], bins=40, color=BLUE, edgecolor="white")
ax.set_xlabel("单价（元）")
ax.set_ylabel("商品数")
ax.set_title("商品价格分布（清洗后 %d 条）" % len(df))
plt.tight_layout()
plt.savefig("charts/3-price-hist.png")
plt.close()

print("已生成 3 张图")
