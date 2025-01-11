@echo off
REM Type Stubs Installation Script

REM Install type stubs for external libraries
pip install types-requests types-beautifulsoup4 pandas-stubs types-html5lib types-markdown

REM Run mypy to verify type stub installation
python -m mypy .

echo Type stubs installation complete!
