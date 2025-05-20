# Contributing to Customer Service Discussion Generator

Thank you for considering contributing to the Customer Service Discussion Generator! This document provides guidelines and instructions for contributing to this project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a new branch for your feature or bugfix

## Setting Up the Development Environment

1. Install Python 3.6 or higher
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your AWS credentials:
   ```bash
   aws configure
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Add comments for complex logic
- Include docstrings for functions and classes

### Adding a New Language

To add support for a new language:

1. Update the `generate_prompt` function in `generate_conversations.py` to include a language-specific prompt template
2. Add the appropriate speaker labels to the `parse_conversation` function
3. Update the `get_supported_languages` function in `generate_all_languages_conversations.py`
4. Update the language table in `README.md`
5. Test the new language thoroughly

### Testing

Before submitting a pull request, please test your changes:

1. Test text generation for your changes
2. Test audio generation if applicable
3. Verify that the script works with different sentiments
4. Check that the generated conversations are realistic and follow the expected format

## Submitting Changes

1. Commit your changes with a clear commit message
2. Push to your fork
3. Submit a pull request with a description of the changes

## Reporting Issues

If you find a bug or have a suggestion for improvement:

1. Check if the issue already exists in the GitHub issue tracker
2. If not, create a new issue with a clear description and steps to reproduce

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT License.
