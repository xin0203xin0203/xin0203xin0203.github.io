import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("shop,"):
        continue
    parts = line.split(",")
    if len(parts) != 7:
        continue
    shop, category, title, price, sales, comments, date = parts
    try:
        p = float(price)
        s = int(sales)
    except ValueError:
        continue
    print("%s\t%d\t%.2f" % (shop, s, p * s))
