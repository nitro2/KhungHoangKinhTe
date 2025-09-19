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

# ---------- Constants ----------
# Y-axis positions for horizontal lines
CRISIS_Y_POSITION = 1.1      # Red horizontal lines for crises
RECESSION_Y_POSITION = 1.2   # Blue horizontal lines for recessions
EVENTS_Y_POSITION = -0.1     # Purple horizontal lines for war/disaster events

# Sine wave amplitude and positioning
MAIN_CYCLES_MIN = 0.5        # Main cycles range: 0.5 to 1.0
MAIN_CYCLES_MAX = 1.0
SECONDARY_CYCLES_MIN = 0.0   # Secondary cycles range: 0.0 to 0.5
SECONDARY_CYCLES_MAX = 0.5
SINE_AMPLITUDE = 0.25        # Half-amplitude for scaling (0.5 range = 0.25 amplitude)

# Y-axis limits for combined chart
Y_AXIS_MIN = -0.3           # Minimum y-axis value to show events
Y_AXIS_MAX = 1.4            # Maximum y-axis value

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
def build_main_cycle_series(cycles):
    """Build main cycles with range 0.5 to 1.0"""
    series_dict = {}
    composite = np.zeros_like(t_years, dtype=float)
    for name, period, phase, weight in cycles:
        s = np.sin(2*np.pi * (t_years / period) + phase)
        # Scale to range 0.5 to 1.0
        s_scaled = MAIN_CYCLES_MIN + (MAIN_CYCLES_MAX - MAIN_CYCLES_MIN) * (s + 1) / 2
        series_dict[f"{name} (T≈{period}y)"] = s_scaled
        composite += weight * s
    # Normalize and scale composite to same range
    composite /= (np.max(np.abs(composite)) + 1e-9)
    composite_scaled = MAIN_CYCLES_MIN + (MAIN_CYCLES_MAX - MAIN_CYCLES_MIN) * (composite + 1) / 2
    return series_dict, composite_scaled

def build_secondary_cycle_series(cycles):
    """Build secondary cycles with range 0.0 to 0.5"""
    series_dict = {}
    composite = np.zeros_like(t_years, dtype=float)
    for name, period, phase, weight in cycles:
        s = np.sin(2*np.pi * (t_years / period) + phase)
        # Scale to range 0.0 to 0.5
        s_scaled = SECONDARY_CYCLES_MIN + (SECONDARY_CYCLES_MAX - SECONDARY_CYCLES_MIN) * (s + 1) / 2
        series_dict[f"{name} (T≈{period}y)"] = s_scaled
        composite += weight * s
    # Normalize and scale composite to same range
    composite /= (np.max(np.abs(composite)) + 1e-9)
    composite_scaled = SECONDARY_CYCLES_MIN + (SECONDARY_CYCLES_MAX - SECONDARY_CYCLES_MIN) * (composite + 1) / 2
    return series_dict, composite_scaled

main_series, main_composite = build_main_cycle_series(main_cycles)
secondary_series, secondary_composite = build_secondary_cycle_series(secondary_cycles)

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

crisis_periods = [
    ("1929-10-24", "1933-03-01", "Đại Khủng hoảng 1929–33"),
    ("1973-10-01", "1975-03-01", "Khủng hoảng dầu mỏ 1973–75"),
    ("1979-01-01", "1982-12-01", "Sốc dầu lần 2 & thắt chặt 1979–82"),
    ("1982-08-01", "1983-12-01", "Khủng hoảng nợ Mỹ Latinh 1982–83"),
    ("1997-07-01", "1998-12-01", "Khủng hoảng châu Á 1997–98"),
    ("2000-03-01", "2002-12-01", "Vỡ bong bóng dot-com 2000–02"),
    ("2007-08-01", "2009-06-01", "Khủng hoảng tài chính toàn cầu 2007–09"),
    ("2010-01-01", "2012-12-01", "Khủng hoảng nợ Eurozone 2010–12"),
    ("2020-02-01", "2020-12-31", "Sốc COVID-19 2020"),
    ("2022-01-01", "2023-12-31", "Lạm phát toàn cầu & siết tiền tệ 2022–23"),
]

# Build sets for vertical lines and labels (first year of each period) for recessions (blue)
recession_years = set()
recession_year_to_label = {}
for start_str, end_str, label in recession_periods:
    s = pd.to_datetime(start_str)
    e = pd.to_datetime(end_str)
    months = pd.date_range(start=s, end=e, freq="MS")
    years = sorted(set(m.year for m in months))
    for y in years:
        recession_years.add(y)
    if years:
        recession_year_to_label[years[0]] = label
recession_years = sorted(recession_years)

# Build sets for vertical lines and labels (first year of each period) for crises (red)
crisis_years = set()
crisis_year_to_label = {}
for start_str, end_str, label in crisis_periods:
    s = pd.to_datetime(start_str)
    e = pd.to_datetime(end_str)
    months = pd.date_range(start=s, end=e, freq="MS")
    years = sorted(set(m.year for m in months))
    for y in years:
        crisis_years.add(y)
    if years:
        crisis_year_to_label[years[0]] = label
crisis_years = sorted(crisis_years)

# ---------- Combined Chart: All cycles + events ----------
plt.figure(figsize=(13, 6))

# Plot main cycles
for col, series in main_series.items():
    plt.plot(dates, series, linewidth=1, label=col)

# Composite of main cycles
plt.plot(dates, main_composite, linestyle="--", linewidth=2, label="Chỉ số hợp lực (chu kỳ chính, normalized)")

# Horizontal lines for recession periods at y=1.2 (blue)
label_added_recession = False
for start_str, end_str, label in recession_periods:
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # Ensure minimum 1 year duration
    if (end_date - start_date).days < 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    if not label_added_recession:
        plt.plot([start_date, end_date], [RECESSION_Y_POSITION, RECESSION_Y_POSITION], color='blue', linewidth=4, 
                label="Suy thoái (NBER, Mỹ)")
        label_added_recession = True
    else:
        plt.plot([start_date, end_date], [RECESSION_Y_POSITION, RECESSION_Y_POSITION], color='blue', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, RECESSION_Y_POSITION + 0.05), ha='center', va='bottom', 
                fontsize=7, color='blue', rotation=0)

# Horizontal lines for crisis periods at y=1.1 (red)
label_added_crisis = False
for start_str, end_str, label in crisis_periods:
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # Ensure minimum 1 year duration
    if (end_date - start_date).days < 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    if not label_added_crisis:
        plt.plot([start_date, end_date], [CRISIS_Y_POSITION, CRISIS_Y_POSITION], color='red', linewidth=4, 
                label="Khủng hoảng (chọn lọc)")
        label_added_crisis = True
    else:
        plt.plot([start_date, end_date], [CRISIS_Y_POSITION, CRISIS_Y_POSITION], color='red', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, CRISIS_Y_POSITION + 0.05), ha='center', va='bottom', 
                fontsize=7, color='red', rotation=0)

# Axis cosmetics
ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator(base=10))
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
plt.ylim(Y_AXIS_MIN, Y_AXIS_MAX)  # Set y-axis limits using constants
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

# Vertical lines for major war/political events and disasters from CSV
events = [
    (pd.Timestamp("1939-01-01"), "WWII 1939–45"),
    (pd.Timestamp("1950-01-01"), "Korean War 1950–53"),
    (pd.Timestamp("1956-01-01"), "Suez Crisis 1956"),
    (pd.Timestamp("1967-01-01"), "Canal closed 1967–75"),
    (pd.Timestamp("1973-01-01"), "Oil embargo 1973–74"),
    (pd.Timestamp("1971-01-01"), "Nixon Shock 1971–73"),
    (pd.Timestamp("1978-01-01"), "Oil shock 1979–80"),
    (pd.Timestamp("1980-01-01"), "Iran–Iraq War 1980–88"),
    (pd.Timestamp("1990-01-01"), "Gulf War 1990–91"),
    (pd.Timestamp("2001-01-01"), "9/11 (2001)"),
    (pd.Timestamp("2003-01-01"), "Iraq War 2003–11"),
    (pd.Timestamp("2011-01-01"), "Arab Spring 2011–12"),
    (pd.Timestamp("2022-01-01"), "Russia–Ukraine 2022–"),
    (pd.Timestamp("1957-01-01"), "Flu 1957–58"),
    (pd.Timestamp("1968-01-01"), "Flu 1968–70"),
    (pd.Timestamp("2002-01-01"), "SARS 2003"),
    (pd.Timestamp("2004-01-01"), "Tsunami 2004"),
    (pd.Timestamp("2010-01-01"), "Iceland ash 2010"),
    (pd.Timestamp("2011-01-01"), "Tohoku 2011"),
    (pd.Timestamp("2011-01-01"), "Thailand floods 2011"),
    (pd.Timestamp("2014-01-01"), "Ebola 2014–16"),
    (pd.Timestamp("2020-01-01"), "COVID-19 2020–"),
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
