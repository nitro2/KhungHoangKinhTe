# Combined chart with main cycles (0.5-1.0) and secondary cycles (0.0-0.5)
# Events shown as horizontal lines at different y positions

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.dates import YearLocator, DateFormatter

# ---------- Constants ----------
# Y-axis positions for horizontal lines (3-level zigzag)
CRISIS_Y_POSITIONS = [1.0, 1.1, 1.2]      # Red horizontal lines for crises (3 levels)
RECESSION_Y_POSITIONS = [1.3, 1.4, 1.5]   # Blue horizontal lines for recessions (3 levels)
POLITICAL_Y_POSITIONS = [-0.1, -0.2, -0.3]   # Purple horizontal lines for political/war events (3 levels)
DISASTER_Y_POSITIONS = [-0.4, -0.5, -0.6]    # Orange/Yellow horizontal lines for disasters (3 levels)

# Sine wave amplitude and positioning
MAIN_CYCLES_MIN = 0.5        # Main cycles range: 0.5 to 1.0
MAIN_CYCLES_MAX = 1.0
SECONDARY_CYCLES_MIN = 0.0   # Secondary cycles range: 0.0 to 0.5
SECONDARY_CYCLES_MAX = 0.5

# Y-axis limits for combined chart
Y_AXIS_MIN = -0.7           # Minimum y-axis value to show disaster events (down to -0.6)
Y_AXIS_MAX = 1.6            # Maximum y-axis value (increased for recession at 1.5)

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

# Political/War Events (Purple)
political_events = [
    ("1939-09-01", "1945-09-02", "WWII 1939–45"),
    ("1950-06-25", "1953-07-27", "Korean War 1950–53"),
    ("1956-07-26", "1957-03-07", "Suez Crisis 1956"),
    ("1967-06-05", "1975-06-05", "Canal closed 1967–75"),
    ("1971-08-15", "1973-03-01", "Nixon Shock 1971–73"),
    ("1973-10-06", "1974-03-18", "Oil embargo 1973–74"),
    ("1978-01-01", "1980-12-31", "Oil shock 1979–80"),
    ("1980-09-22", "1988-08-20", "Iran–Iraq War 1980–88"),
    ("1990-08-02", "1991-04-11", "Gulf War 1990–91"),
    ("2001-09-11", "2001-09-11", "9/11 (2001)"),
    ("2003-03-20", "2011-12-18", "Iraq War 2003–11"), 
    ("2011-02-01", "2012-12-31", "Arab Spring 2011–12"),
    ("2018-07-06", "2025-12-31", "US–China tariffs (Sec. 301) 2018–"),
    ("2022-02-24", "2024-12-31", "Russia–Ukraine 2022–"),
    ("2023-01-01", "2025-12-31", "AI & Data Center boom 2023–"),
    ("2023-10-07", "2025-12-31", "Israel–Hamas 2023–"),
    ("2024-05-14", "2025-12-31", "US tariffs 2024 (EVs, batteries, solar)"),
]

# Natural Disaster/Pandemic Events (Orange/Yellow)
disaster_events = [
    ("1957-02-01", "1958-12-31", "Flu 1957–58"),
    ("1968-07-01", "1970-12-31", "Flu 1968–70"),
    ("2002-11-01", "2003-07-31", "SARS 2003"),
    ("2004-12-26", "2004-12-26", "Tsunami 2004"),
    ("2010-04-15", "2010-04-21", "Iceland ash 2010"),
    ("2011-03-11", "2011-03-11", "Tohoku 2011"),
    ("2011-07-01", "2011-12-31", "Thailand floods 2011"),
    ("2014-03-01", "2016-06-09", "Ebola 2014–16"),
    ("2020-03-11", "2023-12-31", "COVID-19 2020–"),
    ("2022-06-01", "2022-10-31", "Pakistan floods 2022"),
]

# ---------- Combined Chart: All cycles + events ----------
plt.figure(figsize=(16, 8))

# Plot main cycles (range 0.5 to 1.0)
for col, series in main_series.items():
    plt.plot(dates, series, linewidth=1, label=f"[Chính] {col}")

# Composite of main cycles
plt.plot(dates, main_composite, linestyle="--", linewidth=2, label="[Chính] Chỉ số hợp lực (normalized)")

# Plot secondary cycles (range 0.0 to 0.5)
for col, series in secondary_series.items():
    plt.plot(dates, series, linewidth=1, label=f"[Phụ] {col}")

# Composite of secondary cycles
plt.plot(dates, secondary_composite, linestyle="--", linewidth=2, label="[Phụ] Hợp lực (normalized)")

# Horizontal lines for recession periods with alternating y positions (blue)
label_added_recession = False
for i, (start_str, end_str, label) in enumerate(recession_periods):
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # Ensure minimum 1 year duration
    if (end_date - start_date).days < 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    # Cycle through the three y positions
    y_position = RECESSION_Y_POSITIONS[i % 3]
    
    if not label_added_recession:
        plt.plot([start_date, end_date], [y_position, y_position], color='blue', linewidth=4, 
                label="Suy thoái (NBER, Mỹ)")
        label_added_recession = True
    else:
        plt.plot([start_date, end_date], [y_position, y_position], color='blue', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, y_position + 0.05), ha='center', va='bottom', 
                fontsize=7, color='blue', rotation=0)

# Horizontal lines for crisis periods with alternating y positions (red)
label_added_crisis = False
label_added_crisis_start = False
for i, (start_str, end_str, label) in enumerate(crisis_periods):
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # Cycle through the three y positions first to get the crisis position
    y_position = CRISIS_Y_POSITIONS[i % 3]
    
    # Add vertical line from y=0 to the actual crisis y position
    if not label_added_crisis_start:
        plt.axvline(start_date, ymin=(0-Y_AXIS_MIN)/(Y_AXIS_MAX-Y_AXIS_MIN), 
                   ymax=(y_position-Y_AXIS_MIN)/(Y_AXIS_MAX-Y_AXIS_MIN), 
                   color='red', linestyle=':', linewidth=2, alpha=0.7,
                   label="Bắt đầu khủng hoảng")
        label_added_crisis_start = True
    else:
        plt.axvline(start_date, ymin=(0-Y_AXIS_MIN)/(Y_AXIS_MAX-Y_AXIS_MIN), 
                   ymax=(y_position-Y_AXIS_MIN)/(Y_AXIS_MAX-Y_AXIS_MIN), 
                   color='red', linestyle=':', linewidth=2, alpha=0.7)
    
    # Ensure minimum 1 year duration
    if (end_date - start_date).days < 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    if not label_added_crisis:
        plt.plot([start_date, end_date], [y_position, y_position], color='red', linewidth=4, 
                label="Khủng hoảng (chọn lọc)")
        label_added_crisis = True
    else:
        plt.plot([start_date, end_date], [y_position, y_position], color='red', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, y_position + 0.05), ha='center', va='bottom', 
                fontsize=7, color='red', rotation=0)

# Horizontal lines for political/war events with alternating y positions (purple)
label_added_political = False
for i, (start_str, end_str, label) in enumerate(political_events):
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # For single-day events (like 9/11), extend to 1 year for visibility
    # For multi-year events, ensure maximum 1 year duration
    if (end_date - start_date).days > 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    # Cycle through the three y positions
    y_position = POLITICAL_Y_POSITIONS[i % 3]
    
    if not label_added_political:
        plt.plot([start_date, end_date], [y_position, y_position], color='purple', linewidth=4, 
                label="Sự kiện chính trị/chiến tranh")
        label_added_political = True
    else:
        plt.plot([start_date, end_date], [y_position, y_position], color='purple', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, y_position - 0.05), ha='center', va='top', 
                fontsize=7, color='purple', rotation=0)

# Horizontal lines for disaster/pandemic events with alternating y positions (orange)
label_added_disaster = False
for i, (start_str, end_str, label) in enumerate(disaster_events):
    start_date = pd.to_datetime(start_str)
    end_date = pd.to_datetime(end_str)
    
    # For single-day events (like Tsunami, Tohoku), extend to 1 year for visibility
    # For multi-year events, ensure maximum 1 year duration
    if (end_date - start_date).days > 365:
        end_date = start_date + pd.DateOffset(years=1)
    
    # Cycle through the three y positions
    y_position = DISASTER_Y_POSITIONS[i % 3]
    
    if not label_added_disaster:
        plt.plot([start_date, end_date], [y_position, y_position], color='orange', linewidth=4, 
                label="Thiên tai/đại dịch")
        label_added_disaster = True
    else:
        plt.plot([start_date, end_date], [y_position, y_position], color='orange', linewidth=4)
    
    # Add label at the middle of the line
    mid_date = start_date + (end_date - start_date) / 2
    plt.annotate(label, xy=(mid_date, y_position - 0.05), ha='center', va='top', 
                fontsize=7, color='orange', rotation=0)

# Axis cosmetics
ax = plt.gca()
ax.xaxis.set_major_locator(YearLocator(base=5))    # Major ticks every 5 years instead of 10
ax.xaxis.set_minor_locator(YearLocator(base=1))    # Minor ticks every year
ax.xaxis.set_major_formatter(DateFormatter('%Y'))
ax.grid(True, which='major', linewidth=0.3, alpha=0.7)   # Major grid lines
ax.grid(True, which='minor', linewidth=0.1, alpha=0.3)   # Minor grid lines
plt.ylim(Y_AXIS_MIN, Y_AXIS_MAX)  # Set y-axis limits using constants
plt.title("Biểu đồ Tổng Hợp — Chu kỳ Chính (0.5-1.0) & Chu kỳ Phụ (0.0-0.5) & Các Sự kiện")
plt.xlabel("Năm")
plt.ylabel("Biên độ chuẩn hóa")
plt.legend(ncol=3, fontsize=7, loc='upper left')
plt.tight_layout()

# Save SVG
svg_rel = "./BieuDo_TongHop_ChuKy_SuKien.svg"
plt.savefig(svg_rel, format="svg")
svg_abs = os.path.abspath(svg_rel)

plt.show()

print(f"Biểu đồ tổng hợp đã được lưu: {svg_abs}")
