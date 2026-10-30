import time
import pandas as pd

t0 = time.time()
df = pd.read_csv("products_clean.csv")
t1 = time.time()

res = (df.assign(gmv=df["price"] * df["sales"])
         .groupby("shop", as_index=False)
         .agg(total_sales=("sales", "sum"), total_gmv=("gmv", "sum"))
         .sort_values("total_sales", ascending=False))
t2 = time.time()

print("行数: %d" % len(df))
print("读取 CSV: %.4f 秒" % (t1 - t0))
print("groupby 聚合: %.4f 秒" % (t2 - t1))
print("单机总耗时: %.4f 秒" % (t2 - t0))
print(res.head(10).to_string(index=False))
res.to_csv("pandas_shop_top.csv", index=False, encoding="utf-8")
