# Contributing to Comprehensive Resource Library

## Code of Conduct

This project and everyone participating in it are governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs
- Use the issue template
- Describe the problem in detail
- Include reproduction steps
- Specify your environment (OS, Python version)

### Feature Requests
- Open an issue with the "enhancement" label
- Clearly describe the proposed feature
- Provide use cases

### Pull Request Process
1. Fork the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/amazing-new-thing
   ```
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Submit a pull request

### Development Setup
```bash
# Clone the repository
git clone https://github.com/iHelper30/Comprehensive_Resource_Library.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run tests
pytest tests/
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings
- 120 character line limit
- Use `black` for formatting
- Use `mypy` for type checking

### Commit Message Guidelines
- Use conventional commits
- Format: `<type>(<scope>): <description>`
- Types: 
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation
  - `style`: Formatting
  - `refactor`: Code restructure
  - `test`: Adding tests
  - `chore`: Maintenance

## Questions?
Join our [Discord Community](https://discord.gg/comprehensive-resource-library) or open an issue!
