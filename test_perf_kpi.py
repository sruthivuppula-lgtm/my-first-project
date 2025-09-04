import re
import datetime
import pytest

def parse_timestamp(line):
    """Extract timestamp from log line and convert to datetime"""
    match = re.match(r"\[(.*?)\]", line)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S.%f")
    return None

def extract_kpi_from_log(log_file):
    """Parse log file and calculate boot KPI"""
    boot_start = None
    home_screen = None

    with open(log_file, "r") as f:
        for line in f:
            if "Bootloader: Starting boot sequence" in line:
                boot_start = parse_timestamp(line)
            elif "Home screen displayed" in line:
                home_screen = parse_timestamp(line)

    if not boot_start or not home_screen:
        raise ValueError("Missing boot start or home screen timestamp in log")

    return (home_screen - boot_start).total_seconds()

@pytest.mark.parametrize("log_file", ["merge_log_boot.txt"])
def test_boot_kpi(log_file):
    kpi = extract_kpi_from_log(log_file)
    print(f"\nBoot KPI: {kpi:.2f} seconds")

    # Example requirement: boot must complete in < 20 seconds
    assert kpi < 20, f"Boot KPI too high! Got {kpi:.2f}s"
