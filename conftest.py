import time

def pytest_configure(config):
    time.sleep(10)  # Wait for 10 seconds before starting tests for the other containers to run
