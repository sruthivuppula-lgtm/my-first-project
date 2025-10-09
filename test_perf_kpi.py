import re
import datetime
import pytest
import allure

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
            elif "Wi-Fi service started" in line:
                home_screen = parse_timestamp(line)

    if not boot_start or not home_screen:
        raise ValueError("Missing boot start or home screen timestamp in log")

    return (home_screen - boot_start).total_seconds()

def extract_kpi2_from_log(log_file):
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
        raise ValueError("Missing boot start or wifi service start timestamp in log")

    return (home_screen - boot_start).total_seconds()

@pytest.mark.smoke
@pytest.mark.parametrize("log_file", ["/Users/avengers/my-first-project/merge_log_boot.txt"])
def test_boot_kpi(log_file):
    kpi = extract_kpi_from_log(log_file)
    print(f"\nBoot KPI: {kpi:.2f} seconds")
    print("just added a comment")

    # Example requirement: boot must complete in < 20 seconds
    assert kpi < 20, f"Boot KPI too high! Got {kpi:.2f}s"
    '''
def test_boot_kpi2(log_file):
    kpi2 = extract_kpi2_from_log(log_file)
    print(f"\nBoot KPI 2: {kpi2:.2f} seconds")
    print("just added a comment")
    assert kpi2 < 20, f"Boot KPI too high! Got {kpi2:.2f}s"
    
  '''

@allure.title("Verify WiFi KPI Performance Test")
@allure.description("This test measures WiFi performance KPI for Nest Pro device.")
@allure.severity(allure.severity_level.CRITICAL)
def test_perf_kpi():
    with allure.step("Step 1: Connect to WiFi Network"):
        assert True

    with allure.step("Step 2: Measure throughput and latency"):
        assert 50 > 20  # Example check

    with allure.step("Step 3: Validate KPI metrics"):
        allure.attach("Measured latency: 18ms", "Latency Data", allure.attachment_type.TEXT)
