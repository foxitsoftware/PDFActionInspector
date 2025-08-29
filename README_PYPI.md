# PDF Action Inspector

A Model Context Protocol (MCP) server for extracting and analyzing JavaScript Actions from PDF files. This tool provides structured access to PDF Actions data for security analysis and research purposes.

## What is PDF Action Inspector?

PDF Action Inspector is an MCP server that extracts JavaScript Actions embedded in PDF documents. It's designed to work with MCP-compatible clients (such as Claude Desktop) and hosts that support the Model Context Protocol, allowing you to analyze PDF files using natural language queries.

## Features

- **PDF Action Extraction**: Extract JavaScript Actions from document, page, annotation, and field levels
- **Structured Analysis**: Apply security policies to identify potentially suspicious patterns
- **Password Support**: Handle encrypted PDF files
- **Comprehensive Coverage**: Analyze forms, annotations, and embedded scripts

## Installation

### Quick Start with uvx (Recommended)

```bash
uvx pdf-action-inspector
```

This automatically downloads and runs the MCP server without permanent installation.

### Traditional Installation

```bash
pip install pdf-action-inspector
```

## Setup for MCP Clients

### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "pdf-action-inspector": {
      "command": "uvx",
      "args": ["pdf-action-inspector"]
    }
  }
}
```

Or if you installed via pip:

```json
{
  "mcpServers": {
    "pdf-action-inspector": {
      "command": "pdf-action-inspector",
      "args": []
    }
  }
}
```

### Other MCP Clients

For other MCP-compatible hosts and clients, configure the server using the appropriate method for your client. The server uses STDIO transport and requires no additional arguments.

## Usage

After setup, you can use natural language to analyze PDFs through your MCP client:

```
Extract all JavaScript Actions from this PDF: /path/to/document.pdf
Analyze the security implications of Actions in this file: /path/to/suspicious.pdf
```

## Available MCP Tools

| Tool | Purpose |
|------|---------|
| `extract_pdf_actions` | Extract all JavaScript Actions from PDF |
| `analyze_pdf_actions_security` | Analyze Actions using security policies |
| `get_document_overview` | Get PDF structure and metadata |
| `load_all_annotations` | Analyze PDF annotations |
| `get_page_text_content` | Extract text from specific pages |
| `get_fields_by_name` | Search form fields by name |
| `set_pdf_password` | Handle encrypted PDFs |
| `clear_pdf_cache` | Clear cache for specific or all files |
| `get_cache_status` | Get current cache status |

## Security Analysis

The tool applies security policies to identify patterns such as:

- JavaScript code execution
- Form field manipulation
- Network requests
- File system access attempts
- Suspicious user interactions

## Use Cases

- **Security Research**: Extract and analyze PDF Actions for research
- **Document Analysis**: Understand PDF structure and embedded scripts
- **Educational**: Learn about PDF security mechanisms
- **Forensics**: Investigate PDF-based incidents

## Requirements

- Python 3.10+
- PyPDF2 for PDF parsing
- FastMCP for MCP protocol support

## License

MIT License

## Support

[GitHub Repository](https://github.com/foxitsoftware/PDFActionInspector)
