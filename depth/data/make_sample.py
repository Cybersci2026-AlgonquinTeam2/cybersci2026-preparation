#!/usr/bin/env python3
"""Deterministic sample data for depth-page labs. Usage: python make_sample.py DIR   (writes sales.csv and access.log)"""
import random
import sys
from pathlib import Path

d = Path(sys.argv[1]); d.mkdir(parents=True, exist_ok=True)
r = random.Random(20261126)
# sales.csv: date,region,item,qty,price
items = {"apple": 0.5, "banana": 0.25, "cherry": 4.0, "date": 6.5, "elderberry": 9.0}
rows = ["date,region,item,qty,price"]
for i in range(60):
    it = r.choice(list(items))
    rows.append(f"2026-11-{1 + i % 28:02d},{r.choice(['north', 'south', 'east', 'west'])},{it},{r.randint(1, 12)},{items[it]}")
(d / "sales.csv").write_text("\n".join(rows) + "\n")
# access.log: combined-style web log
paths = ["/", "/index.html", "/products", "/products/42", "/login", "/admin", "/static/app.js", "/api/items", "/search?q=apple", "/robots.txt"]
agents = ["Mozilla/5.0", "curl/8.5.0", "python-requests/2.31", "Googlebot/2.1"]
ips = [f"10.0.{r.randint(0, 3)}.{r.randint(2, 40)}" for _ in range(12)] + ["203.0.113.9"] * 6
lines = []
for i in range(300):
    ip = r.choice(ips)
    p = r.choice(paths)
    code = r.choices([200, 200, 200, 301, 304, 403, 404, 500], k=1)[0]
    if ip == "203.0.113.9":
        p, code = r.choice(["/login", "/admin"]), r.choice([401, 401, 403])
    size = r.randint(120, 9000)
    lines.append(f'{ip} - - [26/Nov/2026:{9 + i // 60:02d}:{i % 60:02d}:{r.randint(0, 59):02d} +0000] "GET {p} HTTP/1.1" {code} {size} "-" "{r.choice(agents)}"')
(d / "access.log").write_text("\n".join(lines) + "\n")
print("wrote", d / "sales.csv", d / "access.log")

# messy.csv: deliberately awkward data for adversarial labs (fixed text, not random)
(d / "messy.csv").write_text("""date,region,item,qty,price
2026-11-01,north,apple,3,0.5
2026-11-01,North,apple,2,0.5
2026-11-02, south,banana,4,0.25

date,region,item,qty,price
2026-11-03,east,"cherry, dark",1,4.0
2026-11-03,west,date,5,6.5
2026-11-04,west,date,,6.5
2026-11-04,north,apple,10,0.5
""")
