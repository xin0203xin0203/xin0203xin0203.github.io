# -*- coding: utf-8 -*-
"""
把 Hadoop Streaming 的输出（shop_top.tsv）变成一个可双击打开的单文件 ECharts 看板。

用法（在 hadoop01 的 ~/streaming 目录下）：
    python3 mk_dashboard.py
产出：
    dashboard.html   —— 数据已内嵌，双击即可打开，不需要起服务
"""
import json
import os

SRC = "shop_top.tsv"
OUT = "dashboard.html"

rows = []
with open(SRC, "r", encoding="utf-8") as f:
    for line in f:
        line = line.rstrip("\n")
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        shop, sales, gmv = parts[0], int(parts[1]), float(parts[2])
        rows.append({"shop": shop, "sales": sales, "gmv": round(gmv, 2)})

rows.sort(key=lambda r: r["sales"], reverse=True)
data_json = json.dumps(rows, ensure_ascii=False)

TOTAL_SALES = sum(r["sales"] for r in rows)
TOTAL_GMV = sum(r["gmv"] for r in rows)
TOP = rows[0] if rows else {"shop": "-", "sales": 0, "gmv": 0}

HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>商品销量分析看板（Hadoop 输出）</title>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0; padding: 24px;
    font-family: "Microsoft YaHei", "PingFang SC", "Noto Sans CJK SC", sans-serif;
    background: #f5f7fa; color: #1f2d3d;
  }
  header { margin-bottom: 18px; }
  h1 { font-size: 22px; margin: 0 0 6px; color: #1F4E79; }
  .sub { font-size: 13px; color: #7a8899; }
  .cards { display: flex; gap: 14px; flex-wrap: wrap; margin: 16px 0 20px; }
  .card {
    flex: 1 1 180px; background: #fff; border-radius: 10px; padding: 14px 16px;
    box-shadow: 0 1px 4px rgba(31,78,121,.08); border-left: 4px solid #1F4E79;
  }
  .card .k { font-size: 12px; color: #8899aa; }
  .card .v { font-size: 22px; font-weight: 700; color: #1F4E79; margin-top: 4px; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  .panel {
    background: #fff; border-radius: 10px; padding: 12px;
    box-shadow: 0 1px 4px rgba(31,78,121,.08);
  }
  .panel.full { grid-column: 1 / -1; }
  .chart { width: 100%; height: 380px; }
  #tip { font-size: 13px; color: #7a8899; padding: 8px 4px 0; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { padding: 7px 10px; border-bottom: 1px solid #eef2f6; text-align: left; }
  th { background: #1F4E79; color: #fff; font-weight: 600; }
  tbody tr:hover { background: #f0f6fb; cursor: pointer; }
  td.num { text-align: right; font-variant-numeric: tabular-nums; }
  @media (max-width: 900px) { .grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<header>
  <h1>商品销量分析看板</h1>
  <div class="sub">数据来源：HDFS <code>/data/products/shoptop/part-00000</code> ｜ 计算方式：Hadoop Streaming（Python mapper + reducer）｜ 点击柱状图或表格行可看单店详情</div>
</header>

<div class="cards">
  <div class="card"><div class="k">店铺数</div><div class="v" id="c-shop">-</div></div>
  <div class="card"><div class="k">累计销量（件）</div><div class="v" id="c-sales">-</div></div>
  <div class="card"><div class="k">累计销售额（元）</div><div class="v" id="c-gmv">-</div></div>
  <div class="card"><div class="k">销量冠军</div><div class="v" id="c-top" style="font-size:17px">-</div></div>
</div>

<div class="grid">
  <div class="panel"><div id="bar" class="chart"></div></div>
  <div class="panel"><div id="pie" class="chart"></div></div>
  <div class="panel full"><div id="scatter" class="chart" style="height:340px"></div></div>
  <div class="panel full">
    <div id="tip">全部店铺明细（按销量降序）</div>
    <table>
      <thead><tr><th>排名</th><th>店铺</th><th style="text-align:right">累计销量</th><th style="text-align:right">累计销售额</th><th style="text-align:right">占总额</th></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
</div>

<script>
const DATA = __DATA__;
const BLUE = "#1F4E79";

const fmt = n => n.toLocaleString("zh-CN");
const money = n => (n / 10000).toLocaleString("zh-CN", {maximumFractionDigits: 1}) + " 万";

document.getElementById("c-shop").textContent = DATA.length;
document.getElementById("c-sales").textContent = fmt(__TOTAL_SALES__);
document.getElementById("c-gmv").textContent = money(__TOTAL_GMV__);
document.getElementById("c-top").textContent = "__TOP_SHOP__";

const tbody = document.getElementById("tbody");
DATA.forEach((d, i) => {
  const tr = document.createElement("tr");
  tr.innerHTML = `<td>${i + 1}</td><td>${d.shop}</td>
    <td class="num">${fmt(d.sales)}</td><td class="num">${fmt(d.gmv)}</td>
    <td class="num">${(d.gmv / __TOTAL_GMV__ * 100).toFixed(1)}%</td>`;
  tr.onclick = () => focusShop(d.shop);
  tbody.appendChild(tr);
});

const bar = echarts.init(document.getElementById("bar"));
const pie = echarts.init(document.getElementById("pie"));
const scatter = echarts.init(document.getElementById("scatter"));

const top10 = DATA.slice(0, 10);

bar.setOption({
  title: { text: "店铺累计销量 TOP 10", left: "center", textStyle: { fontSize: 14, color: BLUE } },
  grid: { left: 110, right: 70, top: 46, bottom: 30 },
  tooltip: { trigger: "axis", axisPointer: { type: "shadow" },
    formatter: p => `${p[0].name}<br/>销量：${fmt(p[0].value)} 件` },
  xAxis: { type: "value", axisLabel: { formatter: v => v / 1000 + "k" }, splitLine: { lineStyle: { color: "#eef2f6" } } },
  yAxis: { type: "category", inverse: true,
    data: top10.map(d => d.shop),
    axisLabel: { fontSize: 11, color: "#556" }, axisLine: { show: false }, axisTick: { show: false } },
  series: [{
    type: "bar", data: top10.map(d => d.sales), barWidth: "58%",
    itemStyle: { color: BLUE, borderRadius: [0, 4, 4, 0] },
    label: { show: true, position: "right", fontSize: 10, color: "#556",
      formatter: p => fmt(p.value) },
    emphasis: { itemStyle: { color: "#2E70A8" } }
  }]
});

function pieData() {
  const rest = DATA.slice(10);
  const restGmv = rest.reduce((s, d) => s + d.gmv, 0);
  const arr = DATA.slice(0, 10).map(d => ({ name: d.shop, value: d.gmv }));
  if (restGmv > 0) arr.push({ name: "其他 " + rest.length + " 家", value: restGmv });
  return arr;
}

pie.setOption({
  title: { text: "店铺销售额占比", left: "center", textStyle: { fontSize: 14, color: BLUE } },
  tooltip: { trigger: "item", formatter: p => `${p.name}<br/>${money(p.value)}（${p.percent}%）` },
  legend: { bottom: 0, type: "scroll", textStyle: { fontSize: 10 } },
  series: [{
    type: "pie", radius: ["38%", "62%"], center: ["50%", "48%"],
    avoidLabelOverlap: true, data: pieData(),
    label: { fontSize: 10, formatter: "{b}\\n{d}%" },
    labelLine: { length: 8, length2: 8 },
    itemStyle: { borderColor: "#fff", borderWidth: 2 }
  }]
});

scatter.setOption({
  title: { text: "销量 vs 销售额（每家店一个点）", left: "center", textStyle: { fontSize: 14, color: BLUE } },
  grid: { left: 90, right: 40, top: 50, bottom: 50 },
  tooltip: { formatter: p => `${p.data[2]}<br/>销量：${fmt(p.data[0])}<br/>销售额：${money(p.data[1])}` },
  xAxis: { name: "累计销量", nameLocation: "middle", nameGap: 28,
    axisLabel: { formatter: v => v / 1000 + "k" }, splitLine: { lineStyle: { color: "#eef2f6" } } },
  yAxis: { name: "累计销售额（万）", nameLocation: "middle", nameGap: 56,
    axisLabel: { formatter: v => (v / 10000).toFixed(0) },
    splitLine: { lineStyle: { color: "#eef2f6" } } },
  series: [{
    type: "scatter", symbolSize: 14,
    data: DATA.map(d => [d.sales, d.gmv, d.shop]),
    itemStyle: { color: BLUE, opacity: .75 }
  }]
});

function focusShop(name) {
  bar.dispatchAction({ type: "highlight", seriesIndex: 0, name: name });
  pie.dispatchAction({ type: "highlight", seriesIndex: 0, name: name });
  const d = DATA.find(x => x.shop === name);
  document.getElementById("tip").innerHTML =
    `<b style="color:${BLUE}">${name}</b> ｜ 销量 ${fmt(d.sales)} 件 ｜ 销售额 ${money(d.gmv)} ｜ 占总销售额 ${(d.gmv / __TOTAL_GMV__ * 100).toFixed(1)}%`;
  setTimeout(() => {
    bar.dispatchAction({ type: "downplay", seriesIndex: 0, name: name });
    pie.dispatchAction({ type: "downplay", seriesIndex: 0, name: name });
  }, 2500);
}

bar.on("click", p => focusShop(p.name));
window.addEventListener("resize", () => { bar.resize(); pie.resize(); scatter.resize(); });
</script>
</body>
</html>
"""

html = (HTML
        .replace("__DATA__", data_json)
        .replace("__TOTAL_SALES__", str(TOTAL_SALES))
        .replace("__TOTAL_GMV__", repr(TOTAL_GMV))
        .replace("__TOP_SHOP__", TOP["shop"]))

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print("店铺数: %d" % len(rows))
print("累计销量: %d 件" % TOTAL_SALES)
print("累计销售额: %.2f 元" % TOTAL_GMV)
print("销量冠军: %s（%d 件）" % (TOP["shop"], TOP["sales"]))
print("已生成: %s（%d KB）" % (os.path.abspath(OUT), len(html.encode("utf-8")) // 1024))
