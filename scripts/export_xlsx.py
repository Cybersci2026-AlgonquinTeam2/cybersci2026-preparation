#!/usr/bin/env python3
"""Build tracker/CyberSci-Tracker.xlsx from the CSV files (styled, with a formula dashboard).

Run `python scripts/export_xlsx.py`, then (optionally) LibreOffice recalc so cached values exist.
CSV files stay the source of truth; the workbook is a view. Re-run after `tracker.py done ...`.
"""
from csv import DictReader
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

TDIR = Path(__file__).resolve().parent.parent / "tracker"
FONT = "Arial"
INK, MUTED = "1F2937", "6B7280"
HEAD_BG, HEAD_FG = "1F3A5F", "FFFFFF"
BAND = "F3F6FA"
THIN = Side(style="thin", color="D5DAE1")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
STATUS_FILL = {"done": "C6EFCE", "doing": "FFEB9C", "skipped": "E5E7EB"}
TIER_FILL = {"A": "DBEAFE", "B": "E0F2FE", "C": "F3F4F6", "E": "FDE68A", "R": "EDE9FE"}
BLOCK_FILL = {"Event": "FDE68A", "Commute": "EDE9FE", "Build": "DCFCE7",
              "Review": "FCE7F3", "Admin": "E5E7EB"}


def read(name):
    with (TDIR / name).open(newline="", encoding="utf-8") as f:
        return list(DictReader(f))


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return v


def sheet(wb, title, rows, widths, numeric=(), wrap=(), color=None, tab="1F3A5F"):
    ws = wb.create_sheet(title)
    ws.sheet_properties.tabColor = tab
    cols = list(rows[0].keys())
    ws.append(cols)
    for r in rows:
        ws.append([num(r[c]) if c in numeric else r[c] for c in cols])
    for j, c in enumerate(cols, 1):
        cell = ws.cell(1, j)
        cell.font = Font(name=FONT, bold=True, color=HEAD_FG, size=10)
        cell.fill = PatternFill("solid", fgColor=HEAD_BG)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
        ws.column_dimensions[get_column_letter(j)].width = widths.get(c, 14)
    ws.row_dimensions[1].height = 30
    for i in range(2, ws.max_row + 1):
        band = BAND if i % 2 == 0 else "FFFFFF"
        for j, c in enumerate(cols, 1):
            cell = ws.cell(i, j)
            cell.font = Font(name=FONT, size=10, color=INK)
            cell.fill = PatternFill("solid", fgColor=band)
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=c in wrap)
            if c in numeric:
                cell.alignment = Alignment(horizontal="center", vertical="top")
            if c == "url" and str(cell.value).startswith("http"):
                cell.hyperlink = cell.value
                cell.font = Font(name=FONT, size=10, color="1D4ED8", underline="single")
        if color:
            color(ws, i, cols)
    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions
    ws.sheet_view.zoomScale = 100
    return ws, cols


def main():
    wb = Workbook()
    wb.remove(wb.active)

    daily = read("tracker.csv")
    sched = [r for r in daily if r["date"]]
    backlog = [r for r in daily if not r["date"]]

    def day_color(ws, i, cols):
        for key, fills in (("tier", TIER_FILL), ("block", BLOCK_FILL)):
            c = cols.index(key) + 1
            v = ws.cell(i, c).value
            if v in fills:
                ws.cell(i, c).fill = PatternFill("solid", fgColor=fills[v])

    widths = dict(id=7, date=11, day=6, week=7, phase=20, block=10, category=11, tier=6,
                  source=24, task=52, done_when=40, hours=7, level=7, status=9, spent=7,
                  url=34, notes=24)
    wsd, cols = sheet(wb, "Daily", sched + backlog, widths, numeric=("hours", "spent"),
                      wrap=("task", "done_when", "notes", "source"), color=day_color, tab="2563EB")
    n = wsd.max_row
    sc = cols.index("status") + 1
    dv = DataValidation(type="list", formula1='"todo,doing,done,skipped"', allow_blank=False)
    wsd.add_data_validation(dv)
    dv.add(f"{get_column_letter(sc)}2:{get_column_letter(sc)}{n}")
    rng = f"A2:{get_column_letter(len(cols))}{n}"
    sref = f"${get_column_letter(sc)}2"
    for status, fill in STATUS_FILL.items():
        wsd.conditional_formatting.add(
            rng, FormulaRule(formula=[f'{sref}="{status}"'], fill=PatternFill("solid", bgColor=fill)))

    # Weekly roll-up with formulas over Daily
    ws = wb.create_sheet("Weekly", 0)
    ws.sheet_properties.tabColor = "0F766E"
    hdr = ["Week", "Phase", "Planned h", "Done h", "% done", "Study h", "Commute h", "Events h"]
    ws.append(hdr)
    weeks = sorted({r["week"] for r in sched}, key=lambda w: int(w[1:]))
    colh = {c: get_column_letter(cols.index(c) + 1) for c in cols}
    rngc = lambda c: f"Daily!${colh[c]}$2:${colh[c]}${n}"
    for k, w in enumerate(weeks, 2):
        phase = next(r["phase"] for r in sched if r["week"] == w)
        ws.append([w, phase,
                   f'=SUMIFS({rngc("hours")},{rngc("week")},A{k})',
                   f'=SUMIFS({rngc("hours")},{rngc("week")},A{k},{rngc("status")},"done")',
                   f'=IF(C{k}=0,0,D{k}/C{k})',
                   f'=SUMIFS({rngc("hours")},{rngc("week")},A{k})-G{k}',
                   f'=SUMIFS({rngc("hours")},{rngc("week")},A{k},{rngc("block")},"Commute")',
                   f'=SUMIFS({rngc("hours")},{rngc("week")},A{k},{rngc("block")},"Event")'])
    last = ws.max_row
    ws.append(["Total", "", f"=SUM(C2:C{last})", f"=SUM(D2:D{last})",
               f"=IF(C{last + 1}=0,0,D{last + 1}/C{last + 1})", f"=SUM(F2:F{last})",
               f"=SUM(G2:G{last})", f"=SUM(H2:H{last})"])
    for j in range(1, len(hdr) + 1):
        c = ws.cell(1, j)
        c.font = Font(name=FONT, bold=True, color=HEAD_FG, size=10)
        c.fill = PatternFill("solid", fgColor=HEAD_BG)
        c.alignment = Alignment(horizontal="center")
        ws.column_dimensions[get_column_letter(j)].width = [8, 24, 12, 10, 9, 10, 12, 10][j - 1]
    for i in range(2, ws.max_row + 1):
        for j in range(1, len(hdr) + 1):
            c = ws.cell(i, j)
            c.font = Font(name=FONT, size=10, bold=(i == ws.max_row), color=INK)
            c.border = BORDER
            if j == 5:
                c.number_format = "0%"
            elif j > 2:
                c.number_format = "0.0"
    ws.freeze_panes = "A2"

    # Category roll-up
    cs = wb.create_sheet("Categories", 1)
    cs.sheet_properties.tabColor = "0F766E"
    cs.append(["Category", "Planned h", "Done h", "% done", "Items", "Items done"])
    cats = sorted({r["category"] for r in daily})
    for k, c in enumerate(cats, 2):
        cs.append([c,
                   f'=SUMIFS({rngc("hours")},{rngc("category")},A{k})',
                   f'=SUMIFS({rngc("hours")},{rngc("category")},A{k},{rngc("status")},"done")',
                   f'=IF(B{k}=0,0,C{k}/B{k})',
                   f'=COUNTIFS({rngc("category")},A{k})',
                   f'=COUNTIFS({rngc("category")},A{k},{rngc("status")},"done")'])
    for j in range(1, 7):
        c = cs.cell(1, j)
        c.font = Font(name=FONT, bold=True, color=HEAD_FG, size=10)
        c.fill = PatternFill("solid", fgColor=HEAD_BG)
        cs.column_dimensions[get_column_letter(j)].width = [16, 12, 10, 9, 8, 11][j - 1]
    for i in range(2, cs.max_row + 1):
        for j in range(1, 7):
            c = cs.cell(i, j)
            c.font = Font(name=FONT, size=10, color=INK)
            c.border = BORDER
            if j == 4:
                c.number_format = "0%"
            elif j in (2, 3):
                c.number_format = "0.0"
    cs.conditional_formatting.add(f"D2:D{cs.max_row}",
                                  CellIsRule(operator="greaterThanOrEqual", formula=["0.8"],
                                             fill=PatternFill("solid", bgColor="C6EFCE")))

    # Roadmap, Reading, Toolkit
    road = read("roadmap.csv")
    sheet(wb, "Roadmap", road,
          dict(week_start=12, week_end=12, phase=22, theme=30, practice=60, reading=44,
               backlog_ids=14, events=36, gate=40, level_target=8, hours=7),
          numeric=("hours",), wrap=("theme", "practice", "reading", "events", "gate"), tab="7C3AED")

    reading = read("reading.csv")
    wsr, rc = sheet(wb, "Reading", reading,
                    dict(id=6, title=46, author_source=28, type=10, format=12, cost=7,
                         category=11, level=12, est_hours=9, phase=9, commute_ok=10, url=36, status=9),
                    numeric=("est_hours",), wrap=("title", "author_source"), tab="B45309")
    dv2 = DataValidation(type="list", formula1='"todo,reading,done,skipped"')
    wsr.add_data_validation(dv2)
    k = rc.index("status") + 1
    dv2.add(f"{get_column_letter(k)}2:{get_column_letter(k)}{wsr.max_row}")

    tool = read("toolkit.csv")
    wst, tc = sheet(wb, "Toolkit", tool,
                    dict(id=6, type=10, name=36, category=12, purpose=44, url=40, priority=8,
                         setup_hours=9, install_by=12, status=9, safety_notes=36),
                    numeric=("setup_hours",), wrap=("name", "purpose", "safety_notes"), tab="B91C1C")
    dv3 = DataValidation(type="list", formula1='"todo,installed,done,skipped"')
    wst.add_data_validation(dv3)
    k = tc.index("status") + 1
    dv3.add(f"{get_column_letter(k)}2:{get_column_letter(k)}{wst.max_row}")

    out = TDIR / "CyberSci-Tracker.xlsx"
    wb.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
