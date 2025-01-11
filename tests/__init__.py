# Comprehensive Resource Library Test Suite
# Initializes test environment and provides common testing utilities

import logging
import os
import sys

# Ensure the project root is in the Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Configure logging for tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def setup_test_environment():
    """
    Global test environment setup.
    Runs before any tests are executed.
    """
    # Add any global test setup logic here
    logging.info("Initializing test environment")


def teardown_test_environment():
    """
    Global test environment teardown.
    Runs after all tests are completed.
    """
    # Add any global test cleanup logic here
    logging.info("Cleaning up test environment")
