# Two stacked (separate) charts:
# - Chart 1: "Chu kỳ chính" + composite of main cycles + vertical lines for NBER US recessions (with labels at first year)
# - Chart 2: "Chu kỳ phụ" + vertical lines for World War II and COVID-19
# Notes:
# - Synthetic sine cycles are illustrative. No seaborn, no explicit colors, each chart on its own figure.
# - Save SVGs to current path "./" (as requested) and also to "/mnt/data" for convenient download links.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.dates import YearLocator, DateFormatter

# ---------- Timeline ----------
dates = pd.date_range(start="1925-01-01", end="2035-12-31", freq="MS")
t_years = (dates - dates[0]).days / 365.25

# ---------- Define cycles ----------
# Main cycles (name, period_years, phase_rad, weight)
main_cycles = [
    ("Tín dụng",                 14.0, 0.0,  1.00),
    ("Bất động sản",             18.0, 0.7,  0.90),
    ("Kinh doanh–tồn kho",        4.0, 1.3,  0.55),
    ("Lãi suất/thanh khoản",      6.0, 0.5,  0.80),
    ("Đô la/toàn cầu hóa vốn",    8.0, 2.1,  0.70),
]

# Secondary cycles
secondary_cycles = [
    ("Nhân khẩu học/đổi mới CN", 45.0, 0.9, 0.65),
    ("Chứng khoán",               9.0, 1.2, 0.60),
]

# ---------- Build series ----------
def build_cycle_series(cycles):
    series_dict = {}
    composite = np.zeros_like(t_years, dtype=float)
    for name, period, phase, weight in cycles:
        s = np.sin(2*np.pi * (t_years / period) + phase)
        series_dict[f"{name} (T≈{period}y)"] = s
        composite += weight * s
    # Normalize composite
    composite /= (np.max(np.abs(composite)) + 1e-9)
    return series_dict, composite

main_series, main_composite = build_cycle_series(main_cycles)
secondary_series, secondary_composite = build_cycle_series(secondary_cycles)

# ---------- Recessions (NBER, US) ----------
recession_periods = [
    ("1929-08-01", "1933-03-01", "Đại Suy thoái 1929–33"),
    ("1937-05-01", "1938-06-01", "Suy thoái 1937–38"),
    ("1945-02-01", "1945-10-01", "Suy thoái 1945 (hậu chiến)"),
    ("1948-11-01", "1949-10-01", "Suy thoái 1948–49"),
    ("1953-07-01", "1954-05-01", "Suy thoái 1953–54"),
    ("1957-08-01", "1958-04-01", "Suy thoái 1957–58"),
    ("1960-04-01", "1961-02-01", "Suy thoái 1960–61"),
    ("1969-12-01", "1970-11-01", "Suy thoái 1969–70"),
    ("1973-11-01", "1975-03-01", "Suy thoái 1973–75 (dầu mỏ)"),
    ("1980-01-01", "1980-07-01", "Suy thoái 1980"),
    ("1981-07-01", "1982-11-01", "Suy thoái 1981–82"),
    ("1990-07-01", "1991-03-01", "Suy thoái 1990–91"),
    ("2001-03-01", "2001-11-01", "Suy thoái 2001 (dot-com)"),
    ("2007-12-01", "2009-06-01", "Khủng hoảng 2007–09"),
    ("2020-02-01", "2020-04-01", "COVID-19 2020"),
]

# Build sets for vertical lines and labels (first year of each period)
recession_years = set()
first_year_to_label = {}
for start_str, end_str, label in recession_periods:
    s = pd.to_datetime(start_str)
    e = pd.to_datetime(end_str)
    months = pd.date_range(start=s, end=e, freq="MS")
    years = sorted(set(m.year for m in months))
    for y in years:
        recession_years.add(y)
    if years:
        first_year_to_label[years[0]] = label
recession_years = sorted(recession_years)

# ---------- Chart 1: Main cycles + composite + recession lines ----------
plt.figure(figsize=(13, 6))

# Plot main cycles
for col, series in main_series.items():
    plt.plot(dates, series, linewidth=1, label=col)

# Composite of main cycles
plt.plot(dates, main_composite, linestyle="--", linewidth=2, label="Chỉ số hợp lực (chu kỳ chính, normalized)")

# Vertical lines for recession years
label_added = False
for y in recession_years:
    ts = pd.Timestamp(f"{y}-01-01")
    if not label_added:
        plt.axvline(ts, linestyle="-", linewidth=0.9, label="Năm có suy thoái (NBER, Mỹ)")
        label_added = True
    else:
        plt.axvline(ts, linestyle="-", linewidth=0.9)

# Labels at first year of each recession period
for y, text in first_year_to_label.items():
    ts = pd.Timestamp(f"{y}-01-01")
    plt.annotate(text, xy=(ts, 1.02), xycoords=('data', 'axes fraction'),
                 xytext=(3, 2), textcoords='offset points', rotation=90,
                 va='bottom', ha='left', fontsize=8)

# Axis cosmetics
ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator(base=10))
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
plt.title("Biểu đồ 1 — Chu kỳ CHÍNH & Chỉ số hợp lực (chỉ từ chu kỳ chính)")
plt.xlabel("Năm")
plt.ylabel("Biên độ chuẩn hóa")
plt.grid(True, linewidth=0.3)
plt.legend(ncol=2, fontsize=8)
plt.tight_layout()

# Save SVGs (current path and /mnt/data for download)
svg1_rel = "./BieuDo_1_ChuKyChinh.svg"
plt.savefig(svg1_rel, format="svg")
svg1_abs = os.path.abspath(svg1_rel)
svg1_dl = "/mnt/data/BieuDo_1_ChuKyChinh.svg"
try:
    import shutil
    shutil.copyfile(svg1_abs, svg1_dl)
except Exception as e:
    pass

plt.show()

# ---------- Chart 2: Secondary cycles + war/COVID lines ----------
plt.figure(figsize=(13, 6))

# Plot secondary cycles
for col, series in secondary_series.items():
    plt.plot(dates, series, linewidth=1, label=col)

# Optional: show composite of secondary cycles (dashed) for reference
plt.plot(dates, secondary_composite, linestyle="--", linewidth=2, label="Hợp lực (chu kỳ phụ, normalized)")

# Vertical lines for World War II and COVID-19
events = [
    (pd.Timestamp("1939-01-01"), "Thế chiến II 1939–45"),
    (pd.Timestamp("2020-01-01"), "COVID-19 2020"),
]
label_added = False
for ts, label in events:
    if not label_added:
        plt.axvline(ts, linestyle="-", linewidth=0.9, label="Sự kiện (chiến tranh/thiên tai)")
        label_added = True
    else:
        plt.axvline(ts, linestyle="-", linewidth=0.9)
    # annotate near top
    plt.annotate(label, xy=(ts, 1.02), xycoords=('data', 'axes fraction'),
                 xytext=(3, 2), textcoords='offset points', rotation=90,
                 va='bottom', ha='left', fontsize=8)

# Axis cosmetics
ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator(base=10))
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
plt.title("Biểu đồ 2 — Chu kỳ PHỤ & Sự kiện (Thế chiến, COVID)")
plt.xlabel("Năm")
plt.ylabel("Biên độ chuẩn hóa")
plt.grid(True, linewidth=0.3)
plt.legend(ncol=2, fontsize=8)
plt.tight_layout()

# Save SVGs (current path and /mnt/data for download)
svg2_rel = "./BieuDo_2_ChuKyPhu.svg"
plt.savefig(svg2_rel, format="svg")
svg2_abs = os.path.abspath(svg2_rel)
svg2_dl = "/mnt/data/BieuDo_2_ChuKyPhu.svg"
try:
    import shutil
    shutil.copyfile(svg2_abs, svg2_dl)
except Exception as e:
    pass

plt.show()

(svg1_abs, svg2_abs, svg1_dl, svg2_dl)
