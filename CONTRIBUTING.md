# Contributing to HackMerlin Agent

Thank you for your interest in contributing to the HackMerlin Agent project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues
- Use the GitHub issue tracker to report bugs or suggest features
- Provide detailed information about the problem
- Include steps to reproduce the issue
- Attach relevant logs or screenshots

### Submitting Changes
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🛠️ Development Setup

### Prerequisites
- Python 3.8+
- Git
- Chrome browser
- OpenAI API key

### Setup
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/hackmerlin-agent.git
cd hackmerlin-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 📝 Code Style

### Python
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions small and focused

### Example
```python
def extract_password(self, level: int, response: str, merlin_prompt: str = None) -> str:
    """
    Extract password from Merlin's response using appropriate strategy.
    
    Args:
        level: Current game level (1-7)
        response: Merlin's response text
        merlin_prompt: Original prompt sent to Merlin
        
    Returns:
        Extracted password or None if extraction failed
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_extractor.py
```

### Writing Tests
- Create test files in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (APIs, web requests)

### Example Test
```python
import pytest
from llm_extractor import PasswordExtractor

def test_rule_based_extraction_level_1():
    extractor = PasswordExtractor()
    response = 'The password is "SECRET"'
    result = extractor.rule_based(1, response)
    assert result == "SECRET"
```

## 🎯 Areas for Contribution

### High Priority
- Fix Level 6 acrostic extraction
- Improve Level 7 last-word extraction
- Add more robust error handling
- Optimize AI prompt engineering

### Medium Priority
- Add visual analysis capabilities
- Implement better logging and monitoring
- Create configuration management
- Add performance metrics

### Low Priority
- Add support for more puzzle types
- Create web interface for monitoring
- Implement machine learning improvements
- Add multi-language support

## 📋 Pull Request Guidelines

### Before Submitting
- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation is updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Screenshots (if applicable)
Add screenshots to help explain your changes

## Additional Notes
Any additional information about the changes
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - Python version
   - Operating system
   - Browser version
   - Package versions

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected behavior
   - Actual behavior

3. **Error Information**
   - Full error traceback
   - Log files
   - Screenshots if applicable

4. **Additional Context**
   - Any workarounds found
   - Related issues
   - System configuration

## 💡 Feature Requests

When suggesting features:

1. **Problem Description**
   - What problem does this solve?
   - Why is it important?

2. **Proposed Solution**
   - How should it work?
   - Any implementation ideas?

3. **Alternatives Considered**
   - Other solutions you've thought of
   - Why this approach is better

## 📚 Documentation

### Code Documentation
- Use docstrings for all public functions
- Include type hints
- Add inline comments for complex logic

### User Documentation
- Update README.md for user-facing changes
- Add examples for new features
- Keep installation instructions current

## 🔒 Security

- Never commit API keys or sensitive information
- Use environment variables for configuration
- Report security issues privately to maintainers
- Follow secure coding practices

## 📞 Getting Help

- Check existing issues and discussions
- Join our community discussions
- Contact maintainers for urgent issues

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing to HackMerlin Agent! 🚀
