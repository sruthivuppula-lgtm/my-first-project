def pytest_addoption(parser):
    parser.addoption(
        "--boot-log", action="store", default="merge_log_boot.txt",
        help="Path to the boot log file"
    )

import pytest

@pytest.fixture
def log_file(request):
    return request.config.getoption("--boot-log")

