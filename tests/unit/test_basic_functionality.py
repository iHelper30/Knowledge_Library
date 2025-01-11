import pytest
import sys
import os

# Ensure project root is in path
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
        '..'))
sys.path.insert(0, PROJECT_ROOT)


def test_project_structure():
    """
    Basic test to verify project structure and import capabilities.
    """
    # Verify key directories exist
    assert os.path.exists(os.path.join(PROJECT_ROOT, 'src')
                          ), "Source directory missing"
    assert os.path.exists(
        os.path.join(
            PROJECT_ROOT, 'tests')), "Tests directory missing"
    assert os.path.exists(
        os.path.join(
            PROJECT_ROOT, 'requirements.txt')), "Requirements file missing"


def test_python_version():
    """
    Ensure Python version compatibility.
    """
    major, minor = sys.version_info.major, sys.version_info.minor
    assert (
        major, minor) >= (
        3, 8), f"Python version {major}.{minor} is not supported"


def test_import_project_modules():
    """
    Verify that core project modules can be imported.
    """
    try:
        # Replace these with actual module names from your project
        import src.core
        import src.utils
    except ImportError as e:
        pytest.fail(f"Failed to import core project modules: {e}")


def test_environment_variables():
    """
    Check critical environment variables are set.
    """
    # Add environment variables specific to your project
    critical_env_vars = [
        'PROJECT_NAME',
        'LOG_LEVEL'
    ]

    for var in critical_env_vars:
        assert var in os.environ, f"Critical environment variable {var} is not set"
