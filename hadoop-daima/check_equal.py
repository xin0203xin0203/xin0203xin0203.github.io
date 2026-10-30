import pandas as pd

hdfs = pd.read_csv("shop_top.tsv", sep="\t", header=None,
                   names=["shop", "h_sales", "h_gmv"])
local = pd.read_csv("pandas_shop_top.csv")

m = hdfs.merge(local, on="shop", how="outer", indicator=True)

print("店铺数 HDFS=%d  单机=%d  匹配=%d" % (len(hdfs), len(local), len(m)))
print("只在一边出现的店铺:", (m["_merge"] != "both").sum())

m["sales_diff"] = (m["h_sales"] - m["total_sales"]).abs()
m["gmv_diff"] = (m["h_gmv"] - m["total_gmv"]).abs()

print("销量最大差异: %s" % m["sales_diff"].max())
print("金额最大差异: %.2f 元" % m["gmv_diff"].max())
ok = m["_merge"].eq("both").all() and m["sales_diff"].max() == 0 and m["gmv_diff"].max() < 0.01
print("结论:", "完全一致 ✓" if ok else "存在差异，需排查")
