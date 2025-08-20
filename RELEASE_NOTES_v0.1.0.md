# PDF Action Inspector v0.1.0 Release Notes

## 🎉 First Public Release

We're excited to announce the first public release of **PDF Action Inspector** - a powerful Model Context Protocol (MCP) server for extracting and analyzing JavaScript Actions from PDF files.

## 📦 What's New

### Core Features
- **Complete PDF Actions Extraction**: Extract Actions from all levels (document, page, annotation, field)
- **Security Analysis Framework**: AI-powered security analysis with structured prompts
- **MCP Server Integration**: Full Model Context Protocol implementation for VS Code/Claude Desktop
- **Encrypted PDF Support**: Handle password-protected PDF documents
- **Memory-Efficient Caching**: Automatic cache management with configurable timeout
- **Comprehensive Error Handling**: Structured error types and detailed logging
- **English Documentation**: Complete internationalization with professional documentation

### Technical Highlights
- **Framework**: FastMCP 2.0 for robust MCP server implementation
- **PDF Processing**: PyPDF2 for reliable PDF parsing and manipulation  
- **Architecture**: Modular design with clear separation of concerns
- **Configuration**: Environment variable-based configuration system
- **Python Support**: Compatible with Python 3.8+

## 📥 Download & Installation

### Package Files
- **Wheel Package**: `pdf_action_inspector-0.1.0-py3-none-any.whl` (23KB) - Recommended
- **Source Package**: `pdf_action_inspector-0.1.0.tar.gz` (972KB) - Includes examples

### Quick Installation
```bash
# Install from wheel (recommended)
pip install pdf_action_inspector-0.1.0-py3-none-any.whl

# Or install from source
pip install pdf_action_inspector-0.1.0.tar.gz
```

### Console Command
After installation, start the MCP server with:
```bash
pdf-action-inspector
```

## 🔧 Configuration

### Environment Variables
- `PDF_CACHE_TIMEOUT_SECONDS=120` - Cache timeout (default: 120 seconds)
- `LOG_LEVEL=INFO` - Logging level
- `MAX_PDF_FILE_SIZE_MB=50` - Maximum file size limit

### VS Code Integration
Add to Claude Desktop configuration:
```json
{
  "mcpServers": {
    "pdf-action-inspector": {
      "command": "pdf-action-inspector"
    }
  }
}
```

## 📋 Available Tools

1. **`analyze_pdf_actions_security(file_path)`** - Generate comprehensive security analysis prompts
2. **`extract_pdf_actions(file_path)`** - Extract raw Actions data in JSON format
3. **`get_document_overview(file_path)`** - Get document structure and metadata
4. **`load_all_annotations(file_path)`** - Load annotations with their Actions
5. **`get_page_text_content(file_path, page_number)`** - Extract page text content
6. **`get_fields_by_name(file_path, field_name)`** - Search form fields by name

## 🎯 Use Cases

### Security Analysis
- Detect malicious JavaScript in PDF documents
- Analyze suspicious form field behaviors
- Identify obfuscated code and automatic actions
- Audit PDF documents for security compliance

### Example Analysis Results
The tool can identify:
- **Malicious redirects**: JavaScript that opens external URLs
- **Hidden field modifications**: Actions that change form values without user knowledge
- **Obfuscated payloads**: Hex-encoded or eval-based malicious code
- **Clean documents**: Verification that PDFs contain no executable content

## 📚 Sample Files Included

The source package includes example PDFs for testing:
- `confuse_js_code.pdf` - Contains obfuscated malicious JavaScript
- `test-signature_action.pdf` - Signature field with hidden value modification
- `without_actions.pdf` - Clean ISO specification document

## 🚀 Getting Started

1. **Download** the release package from GitHub
2. **Install** using pip with the wheel or source package
3. **Configure** environment variables as needed
4. **Run** `pdf-action-inspector` to start the MCP server
5. **Integrate** with VS Code/Claude Desktop for AI-powered analysis

## 🔄 Dependencies

- **PyPDF2** >= 3.0.0 - PDF processing
- **fastmcp** >= 2.0.0 - MCP server framework

All dependencies are automatically installed with pip.

## 📖 Documentation

- **README**: https://github.com/foxitsoftware/PDFActionInspector#readme
- **Installation Guide**: See `INSTALLATION_GUIDE.md`
- **Changelog**: See `CHANGELOG.md`
- **PyPI Publishing**: See `PYPI_PUBLISHING_GUIDE.md`

## 🐛 Known Issues

None reported at this time. Please report any issues on GitHub.

## 🤝 Contributing

We welcome contributions! Please see our GitHub repository for:
- Issue reporting and feature requests
- Code contributions and pull requests
- Documentation improvements

## 📄 License

MIT License - Copyright (c) 2025 Foxit Software Inc.

## 🙏 Acknowledgments

Special thanks to the open source community and the Model Context Protocol project for making this integration possible.

---

**Repository**: https://github.com/foxitsoftware/PDFActionInspector
**Issues**: https://github.com/foxitsoftware/PDFActionInspector/issues
