import sys

cur = None
total_sales = 0
total_gmv = 0.0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    shop, s, gmv = line.split("\t")
    if shop != cur:
        if cur is not None:
            print("%s\t%d\t%.2f" % (cur, total_sales, total_gmv))
        cur = shop
        total_sales = int(s)
        total_gmv = float(gmv)
    else:
        total_sales += int(s)
        total_gmv += float(gmv)

if cur is not None:
    print("%s\t%d\t%.2f" % (cur, total_sales, total_gmv))
