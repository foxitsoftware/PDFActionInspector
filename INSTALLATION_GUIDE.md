# PDF Action Inspector v0.1.0 - Installation Guide

## Download Release Package

Download the latest release package from the GitHub releases page:

### Available Package Formats:

1. **Wheel Package (Recommended)**: `pdf_action_inspector-0.1.0-py3-none-any.whl` (~23KB)
   - Fast installation
   - Works on all platforms with Python 3.8+

2. **Source Distribution**: `pdf_action_inspector-0.1.0.tar.gz` (~972KB) 
   - Contains source code and examples
   - Includes sample PDF files for testing

## Installation Instructions

### Method 1: Install from Wheel (Recommended)

```bash
# Download the .whl file and install
pip install pdf_action_inspector-0.1.0-py3-none-any.whl
```

### Method 2: Install from Source

```bash
# Download the .tar.gz file and install
pip install pdf_action_inspector-0.1.0.tar.gz
```

### Method 3: Extract and Install

```bash
# Extract source package
tar -xzf pdf_action_inspector-0.1.0.tar.gz
cd pdf_action_inspector-0.1.0

# Install dependencies
pip install -r requirements.txt

# Run directly
python mcp_server.py
```

## Dependencies

The package requires:
- Python 3.8 or higher
- PyPDF2 >= 3.0.0
- fastmcp >= 2.0.0

Dependencies will be automatically installed when using pip.

## Usage After Installation

### Console Script
```bash
# Run the MCP server
pdf-action-inspector
```

### Python Module
```python
from src.core.inspector import PDFActionInspector
from src.core.cache_manager import CacheManager
from src.core.error_handler import ErrorHandler

# Initialize components
cache_manager = CacheManager()
error_handler = ErrorHandler()
inspector = PDFActionInspector(cache_manager, error_handler)
```

## VS Code Integration

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "pdf-action-inspector": {
      "command": "pdf-action-inspector"
    }
  }
}
```

## Environment Variables

Configure these optional environment variables:

- `PDF_CACHE_TIMEOUT_SECONDS=120` - Cache timeout (default: 120)
- `LOG_LEVEL=INFO` - Log level
- `MAX_PDF_FILE_SIZE_MB=50` - Maximum file size limit

## Sample Files

The source distribution includes example PDF files in `examples/pdf_samples/`:
- `confuse_js_code.pdf` - Malicious JavaScript example
- `test-signature_action.pdf` - Signature field with actions
- `without_actions.pdf` - Clean document example

## Support

- GitHub Issues: https://github.com/foxitsoftware/PDFActionInspector/issues
- Documentation: https://github.com/foxitsoftware/PDFActionInspector#readme

## License

MIT License - Copyright (c) 2025 Foxit Software Inc.
