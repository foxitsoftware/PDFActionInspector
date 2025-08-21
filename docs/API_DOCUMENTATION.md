# PDF Action Inspector API Documentation

## Overview

The PDF Action Inspector provides a comprehensive API for analyzing PDF documents and extracting security-relevant Actions. The system uses a three-layer architecture for optimal performance and clean separation of concerns.

## Architecture Layers

### 1. Inspector Core Layer (`src.core.inspector.PDFActionInspector`)

The core business logic layer that handles all PDF processing operations.

**Return Type**: Python native types (dict, list)  
**Purpose**: High-performance PDF analysis with type safety  
**Usage**: Direct Python integration, testing, internal processing

#### Core Methods

##### `get_fields_by_name(file_path: str, field_name: str) -> dict`

Find form fields by name with fuzzy matching support.

**Parameters**:
- `file_path`: Absolute or relative path to PDF file
- `field_name`: Field name to search (supports partial matching)

**Returns**:
```python
{
    "field_name": "searched_name",
    "found_fields": [
        {
            "name": "field_full_name",
            "type": "field_type",
            "value": "current_value",
            "page": page_number,
            "actions": [...],
            "rect": [x1, y1, x2, y2]
        }
    ],
    "total_found": count
}
```

**Example**:
```python
from src.core.inspector import PDFActionInspector
inspector = PDFActionInspector()
result = inspector.get_fields_by_name("document.pdf", "signature")
print(f"Found {result['total_found']} signature fields")
```

##### `extract_pdf_actions(file_path: str) -> dict`

Extract all PDF Actions from document, page, annotation, and field levels.

**Parameters**:
- `file_path`: Absolute or relative path to PDF file

**Returns**:
```python
{
    "document_level_actions": [...],
    "pages_level_actions": [...],
    "annotations_level_actions": [...],
    "field_level_actions": [...],
    "total_actions": count,
    "has_javascript": boolean
}
```

##### `get_document_overview(file_path: str) -> dict`

Get comprehensive document structure and security-relevant features.

**Returns**:
```python
{
    "basic_info": {
        "pages": count,
        "file_size": bytes,
        "encrypted": boolean,
        "creator": "application",
        "producer": "library"
    },
    "structure": {
        "has_forms": boolean,
        "has_annotations": boolean,
        "has_javascript": boolean,
        "has_signatures": boolean
    },
    "features": {
        "actions_count": count,
        "annotations_count": count,
        "form_fields_count": count,
        "javascript_objects": count
    }
}
```

##### `load_all_annotations(file_path: str) -> dict`

Extract all annotations with their associated Actions.

**Returns**:
```python
{
    "total_annotations": count,
    "annotations": [
        {
            "subtype": "Widget|Text|Link|...",
            "page": page_number,
            "rect": [x1, y1, x2, y2],
            "actions": [...],
            "widget_info": {...}  # if Widget annotation
        }
    ]
}
```

##### `analyze_pdf_actions_security(file_path: str) -> str`

Generate comprehensive security analysis prompt with extracted Actions data.

**Returns**: Multi-section analysis prompt containing:
- Critical analysis instructions for AI systems
- Analysis strategy with investigation steps
- Complete extracted Actions data
- Security focus areas and risk assessment guidance

### 2. MCP Tools Layer (`mcp_server.py`)

The Model Context Protocol interface layer that provides external tool access.

**Return Type**: JSON strings  
**Purpose**: Standardized tool interface for MCP clients  
**Usage**: External integrations, Claude Desktop, VS Code extensions

#### Available Tools

All MCP tools follow the pattern:
```python
@server.call_tool
async def tool_name(arguments: ToolArguments) -> List[TextContent]:
    # Process arguments
    # Call Inspector core method
    # Return JSON string wrapped in TextContent
```

**Tool List**:
- `mcp_pdf_action_in_extract_pdf_actions`
- `mcp_pdf_action_in_get_fields_by_name`
- `mcp_pdf_action_in_get_document_overview`
- `mcp_pdf_action_in_load_all_annotations`
- `mcp_pdf_action_in_analyze_pdf_actions_security`
- `mcp_pdf_action_in_get_page_text_content`
- `mcp_pdf_action_in_get_pdf_object_information`
- `mcp_pdf_action_in_get_trailer_object`
- `mcp_pdf_action_in_load_all_annotations_in_page`
- `mcp_pdf_action_in_get_page_information_by_spans`
- `mcp_pdf_action_in_get_page_index_by_pdfobjnum`
- `mcp_pdf_action_in_set_pdf_password`
- `mcp_pdf_action_in_clear_pdf_cache`
- `mcp_pdf_action_in_get_cache_status`

### 3. FastMCP Framework Layer

The underlying MCP server hosting and communication layer.

**Purpose**: Network communication, protocol handling  
**Dependencies**: FastMCP library  
**Configuration**: Automatic tool registration and response formatting

## Usage Examples

### Direct Python Usage (Inspector Core)

```python
from src.core.inspector import PDFActionInspector

# Create inspector instance
inspector = PDFActionInspector()

# Analyze document security
result = inspector.extract_pdf_actions("suspicious.pdf")
if result["has_javascript"]:
    print("⚠️ Document contains JavaScript")

# Find specific fields
fields = inspector.get_fields_by_name("form.pdf", "price")
for field in fields["found_fields"]:
    print(f"Field: {field['name']}, Value: {field['value']}")

# Get document overview
overview = inspector.get_document_overview("document.pdf")
print(f"Pages: {overview['basic_info']['pages']}")
print(f"Encrypted: {overview['basic_info']['encrypted']}")

# Working with encrypted PDFs
if overview['basic_info']['encrypted']:
    # Set password for encrypted PDF
    inspector.cache_manager.set_password("encrypted.pdf", "password123")
    # Now you can analyze the encrypted PDF
    actions = inspector.extract_pdf_actions("encrypted.pdf")
```

### MCP Client Usage (External Tools)

```python
# Through MCP client (e.g., Claude Desktop)
# Tools automatically return JSON strings

# For encrypted PDFs, set password first
await call_tool("mcp_pdf_action_in_set_pdf_password", {
    "file_path": "encrypted.pdf",
    "password": "your_password"
})

# Then analyze the PDF
result = await call_tool("mcp_pdf_action_in_extract_pdf_actions", {
    "file_path": "encrypted.pdf"
})

# Parse JSON response
import json
data = json.loads(result.content[0].text)
print(f"Total actions found: {data['total_actions']}")
```

### VS Code Extension Usage

```typescript
// Call through VS Code MCP extension
const result = await mcp.callTool('mcp_pdf_action_in_get_document_overview', {
    file_path: '/path/to/document.pdf'
});

const overview = JSON.parse(result);
console.log(`Document has ${overview.basic_info.pages} pages`);
```

## Error Handling

### Inspector Core Errors

The Inspector core uses the `ErrorHandler` class to provide consistent error responses:

```python
# Success response (dict)
{
    "field_name": "search_term",
    "found_fields": [...],
    "total_found": 2
}

# Error response (dict)
{
    "error": "File not found",
    "error_type": "FileNotFoundError",
    "file_path": "/path/to/missing.pdf"
}
```

### MCP Tools Errors

MCP tools return JSON strings with error information:

```json
{
    "error": "Invalid PDF file",
    "error_type": "PDFError", 
    "file_path": "/path/to/corrupt.pdf",
    "details": "Unable to parse PDF structure"
}
```

## Performance Considerations

### Caching System

The Inspector includes an intelligent caching system:

- **Cache Key**: File path + modification time
- **Cache Duration**: 120 seconds (configurable via `PDF_CACHE_TIMEOUT_SECONDS`)
- **Cache Scope**: Document overview, Actions data, annotations
- **Memory Management**: Automatic cleanup of expired entries

### Optimization Tips

1. **Batch Operations**: Process multiple files in sequence to benefit from cache warming
2. **File Stability**: Avoid modifying PDFs during analysis to maintain cache efficiency
3. **Memory Usage**: Clear cache periodically for long-running processes
4. **Path Consistency**: Use consistent path formats (absolute vs relative) for better cache hits

## Security Considerations

### File Access

- **Path Validation**: All file paths are validated before processing
- **Sandboxing**: No execution of extracted JavaScript code
- **Read-Only**: All operations are read-only, no PDF modification

### Data Handling

- **No Persistence**: Extracted Actions are not stored permanently
- **Memory Safety**: Objects are properly dereferenced to prevent memory leaks
- **Error Isolation**: Failures in one document don't affect others

## Testing

### Pytest Integration

The system includes comprehensive test coverage:

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_pytest.py::TestPDFActionInspector::test_get_fields_by_name -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Test Categories

1. **Core Functionality**: PDF parsing, Action extraction
2. **Error Handling**: Invalid files, corrupt PDFs
3. **Edge Cases**: Empty documents, encrypted files
4. **Performance**: Cache behavior, memory usage
5. **Integration**: MCP tools layer, JSON serialization

## Configuration

### Environment Variables

```bash
# Cache timeout (seconds)
export PDF_CACHE_TIMEOUT_SECONDS=120

# Logging level
export LOG_LEVEL=INFO

# Cache directory (optional)
export PDF_CACHE_DIR="/tmp/pdf_cache"
```

### Runtime Configuration

```python
from src.core.inspector import PDFActionInspector
from src.config.settings import Settings

# Configure cache timeout
Settings.PDF_CACHE_TIMEOUT_SECONDS = 300

# Create inspector with custom config
inspector = PDFActionInspector()
```

## Migration Guide

### From v0.0.x to v0.1.0

**Breaking Changes**:
- Inspector core methods now return Python dicts instead of JSON strings
- MCP tools layer handles JSON serialization
- Enhanced error handling with structured error objects

**Migration Steps**:

1. **Direct Python Usage**:
   ```python
   # Old (v0.0.x)
   result_json = inspector.get_fields_by_name("file.pdf", "name")
   result = json.loads(result_json)
   
   # New (v0.1.0)
   result = inspector.get_fields_by_name("file.pdf", "name")
   # result is already a dict
   ```

2. **MCP Tool Usage**:
   ```python
   # No changes needed - MCP tools still return JSON strings
   result = await call_tool("mcp_pdf_action_in_get_fields_by_name", args)
   data = json.loads(result.content[0].text)
   ```

3. **Testing Updates**:
   ```python
   # Update test assertions for dict returns
   result = inspector.get_document_overview("test.pdf")
   assert isinstance(result, dict)  # Not JSON string
   assert result["basic_info"]["pages"] > 0
   ```

## API Reference Summary

| Method | Layer | Returns | Use Case |
|--------|-------|---------|----------|
| `inspector.get_fields_by_name()` | Core | `dict` | Direct Python integration |
| `inspector.extract_pdf_actions()` | Core | `dict` | High-performance analysis |
| `inspector.get_document_overview()` | Core | `dict` | Document metadata |
| `mcp_pdf_action_in_*` tools | MCP | JSON string | External integrations |
| FastMCP framework | Framework | MCP response | Network communication |

This architecture provides flexibility for both direct Python usage and external tool integration while maintaining optimal performance and type safety.
