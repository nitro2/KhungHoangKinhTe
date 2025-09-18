# Update chart:
# - Keep synthetic multi-cause cycles.
# - Draw vertical lines for every year that contains an NBER US recession month.
# - Label the FIRST vertical line of each recession period with the crisis name.
# - Reduce x-axis year tick density (lower resolution), here every 10 years.
# - Save SVG to the CURRENT PATH "./" as requested and report absolute path for download.
#
# Notes: pedagogical illustration; not a forecast.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.dates import YearLocator, DateFormatter

# ---------- 1) Time axis & synthetic cycles ----------
dates = pd.date_range(start="1925-01-01", end="2035-12-31", freq="MS")
t_years = (dates - dates[0]).days / 365.25

cycles = [
    ("Tín dụng",         14.0, 0.0,   1.00),
    ("Bất động sản",     18.0, 0.8,   0.85),
    ("Chứng khoán",       9.0, 1.2,   0.65),
    ("Chiến tranh/CT",   24.0, 0.5,   0.70),
    ("Năng lượng/hàng hóa", 11.0, 2.1, 0.55),
    ("Thiên tai/khí hậu",  7.0, 2.6,  0.40),
]

data = {}
composite = np.zeros_like(t_years, dtype=float)
for name, period, phase, weight in cycles:
    series = np.sin(2*np.pi * (t_years / period) + phase)
    data[f"{name} (T≈{period}y)"] = series
    composite += weight * series

comp_norm = composite / (np.max(np.abs(composite)) + 1e-9)
data["Chỉ số hợp lực (normalized)"] = comp_norm
df = pd.DataFrame(data, index=dates)

# Peaks (reference)
threshold = np.quantile(df["Chỉ số hợp lực (normalized)"].values, 0.85)
comp_vals = df["Chỉ số hợp lực (normalized)"].values
is_peak = np.zeros_like(comp_vals, dtype=bool)
for i in range(1, len(comp_vals)-1):
    if comp_vals[i-1] < comp_vals[i] > comp_vals[i+1] and comp_vals[i] >= threshold:
        is_peak[i] = True
peak_dates = df.index[is_peak]
peak_vals = comp_vals[is_peak]

# ---------- 2) Recession periods & labels (NBER, US) ----------
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

# Build set of recession years and lookup for first-year label
recession_years = set()
first_year_to_label = {}
for start_str, end_str, label in recession_periods:
    s = pd.to_datetime(start_str)
    e = pd.to_datetime(end_str)
    months = pd.date_range(start=s, end=e, freq="MS")
    years = sorted(set(m.year for m in months))
    for y in years:
        recession_years.add(y)
    # Label the first year of this period
    if years:
        first_year_to_label[years[0]] = label

recession_years = sorted(recession_years)

# ---------- 3) Plot ----------
fig = plt.figure(figsize=(13, 6))

# Individual causes
for col in [c for c in df.columns if c != "Chỉ số hợp lực (normalized)"]:
    plt.plot(df.index, df[col], linewidth=1, label=col)

# Composite
plt.plot(df.index, df["Chỉ số hợp lực (normalized)"], linestyle="--", linewidth=2, label="Chỉ số hợp lực (normalized)")

# Peaks
if len(peak_dates) > 0:
    plt.scatter(peak_dates, peak_vals, marker="o", s=25, label="Đỉnh vượt ngưỡng (top 15%)")
    for d in peak_dates:
        plt.axvline(d, linestyle="dotted", linewidth=0.7)

# Vertical lines for all recession years
label_added = False
for y in recession_years:
    ts = pd.Timestamp(f"{y}-01-01")
    if not label_added:
        plt.axvline(ts, linestyle="-", linewidth=0.9, label="Năm có suy thoái (NBER, Mỹ)")
        label_added = True
    else:
        plt.axvline(ts, linestyle="-", linewidth=0.9)

# Labels on the FIRST vertical line of each recession period
for y, text in first_year_to_label.items():
    ts = pd.Timestamp(f"{y}-01-01")
    # Place text close to the top, rotated, with slight pixel offset
    plt.annotate(text, xy=(ts, 1.02), xycoords=('data', 'axes fraction'),
                 xytext=(3, 2), textcoords='offset points', rotation=90,
                 va='bottom', ha='left', fontsize=8)

# Axes cosmetics: lower x resolution (major tick every 10 years)
ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator(base=10))  # tick every 10 years
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
for label in ax.get_xticklabels():
    label.set_rotation(0)

plt.title("Mô phỏng chu kỳ nguyên nhân + vạch năm suy thoái (NBER, Mỹ) + nhãn kỳ suy thoái")
plt.xlabel("Năm")
plt.ylabel("Biên độ chuẩn hóa")
plt.grid(True, linewidth=0.3)
plt.legend(ncol=2, fontsize=8)
plt.tight_layout()

# ---------- 4) Save SVG to CURRENT PATH ----------
svg_rel = "./ChuKy_KhungHoang_MoPhong_Labeled.svg"
plt.savefig(svg_rel, format="svg")
abs_path = os.path.abspath(svg_rel)
abs_path

plt.show()