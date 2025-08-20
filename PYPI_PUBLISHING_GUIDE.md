# PyPI Publishing Guide for PDF Action Inspector

This document provides step-by-step instructions for publishing the PDF Action Inspector package to PyPI.

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - Test PyPI: https://test.pypi.org/account/register/
   - Production PyPI: https://pypi.org/account/register/

2. **API Tokens**: Generate API tokens for both environments:
   - Test PyPI: https://test.pypi.org/manage/account/token/
   - Production PyPI: https://pypi.org/manage/account/token/

3. **Build Tools**: Install required tools:
   ```bash
   pip install build twine
   ```

## Building the Package

1. **Clean Previous Builds**:
   ```bash
   rm -rf build/ dist/ *.egg-info/
   ```

2. **Build the Package**:
   ```bash
   python -m build
   ```

3. **Check the Package**:
   ```bash
   python -m twine check dist/*
   ```

## Publishing Process

### Step 1: Test on Test PyPI

1. **Upload to Test PyPI**:
   ```bash
   python -m twine upload --repository testpypi dist/*
   ```
   
   When prompted, use:
   - Username: `__token__`
   - Password: Your Test PyPI API token

2. **Test Installation**:
   ```bash
   pip install --index-url https://test.pypi.org/simple/ pdf-action-inspector
   ```

3. **Verify the Package**:
   ```python
   # Test the installation
   python -c "import src.core.inspector; print('Package imported successfully')"
   
   # Test console script
   pdf-action-inspector --help
   ```

### Step 2: Publish to Production PyPI

1. **Upload to PyPI**:
   ```bash
   python -m twine upload dist/*
   ```
   
   When prompted, use:
   - Username: `__token__`
   - Password: Your Production PyPI API token

2. **Verify Publication**:
   - Visit: https://pypi.org/project/pdf-action-inspector/
   - Check package details and download links

3. **Test Installation from PyPI**:
   ```bash
   pip install pdf-action-inspector
   ```

## Package Information

- **Package Name**: `pdf-action-inspector`
- **Version**: `0.1.0`
- **Author**: Foxit Software Inc.
- **License**: MIT
- **Python Versions**: 3.8+

## Dependencies

- PyPDF2 >= 3.0.0
- fastmcp >= 2.0.0

## Console Scripts

After installation, the following command will be available:
```bash
pdf-action-inspector
```

## Automated Scripts

Use the provided scripts for easier building:

### Linux/macOS:
```bash
./build_and_publish.sh
```

### Windows:
```batch
build_and_publish.bat
```

## Version Management

To release a new version:

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md` with new changes
3. Commit and tag the release:
   ```bash
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to x.y.z"
   git tag vx.y.z
   git push origin main --tags
   ```
4. Build and publish following the steps above

## Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all `__init__.py` files are present
2. **Missing Dependencies**: Check `requirements.txt` and `pyproject.toml`
3. **Permission Errors**: Verify API tokens and repository access
4. **Version Conflicts**: Update version number if package already exists

### Package Testing:

```python
# Test basic functionality
from src.core.inspector import PDFActionInspector
from src.core.cache_manager import CacheManager
from src.core.error_handler import ErrorHandler

# Initialize components
cache_manager = CacheManager()
error_handler = ErrorHandler()
inspector = PDFActionInspector(cache_manager, error_handler)

print("PDF Action Inspector initialized successfully!")
```

## Support

For issues related to package publishing:
- PyPI Support: https://pypi.org/help/
- Packaging Guide: https://packaging.python.org/tutorials/packaging-projects/

For project-specific issues:
- GitHub Issues: https://github.com/foxitsoftware/PDFActionInspector/issues
