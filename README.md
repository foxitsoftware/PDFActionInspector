# PDF Action Inspector

A Model Context Protocol (MCP) server for extracting and analyzing JavaScript Actions from PDF files. PDF Actions can trigger malicious scripts when documents are opened or interacted with, making this tool valuable for security analysis.

## Project Structure

```
├── mcp_server.py          # Main MCP server entry point
├── start.py               # Server startup script
├── src/
│   ├── core/              # Core PDF processing
│   ├── config/            # Configuration management
│   └── utils/             # Utility functions
└── examples/              # Sample PDFs for testing
```

## Setup

```bash
pip install PyPDF2 fastmcp
python mcp_server.py
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "pdf-action-inspector": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_server.py"]
    }
  }
}
```

## Tools

- `analyze_pdf_actions_security(file_path)` - Security analysis prompt
- `extract_pdf_actions(file_path)` - Raw Actions data
- `get_document_overview(file_path)` - Document info
- `load_all_annotations(file_path)` - Annotations with Actions

## Environment

- `PDF_CACHE_TIMEOUT_SECONDS=120` - Cache timeout
- `LOG_LEVEL=INFO` - Log level

## Example Analysis

Here are examples of analyzing different types of PDFs using the MCP server in VS Code with GitHub Copilot:

### Example 1: Malicious JavaScript Detection

**File:** `confuse_js_code.pdf`

**User:** Analyze the security of examples/pdf_samples/confuse_js_code.pdf

**AI Agent Analysis:**
```
# Actions Summary
- **Document Level**: One DocumentOpenAction with JavaScript execution
- **Trigger**: Automatic execution when PDF is opened
- **Action Type**: JavaScript execution with obfuscated payload

# Behavior Analysis
- **Obfuscated Code**: Hex-encoded string designed to hide malicious intent
- **Automatic Execution**: No user interaction required - runs immediately on document open
- **Decoded Payload**: `app.launchURL("http://evil.com")` - attempts to redirect user to external malicious site
- **Evasion Technique**: Uses eval() with dynamic string construction to bypass static analysis

# Security Analysis
- **Attack Vector**: Malicious URL redirection through PDF JavaScript
- **Social Engineering**: Disguised as innocent document, automatically executes on open
- **Network Impact**: Attempts unauthorized external network connection
- **User Privacy**: Potential data exfiltration through URL parameters
- **System Risk**: Could be first stage of multi-stage attack

# Conclusion
**Scenario Overview:** Malicious PDF containing obfuscated JavaScript designed to redirect users to potentially harmful external website

**Benign Level:** Malicious - Clear intent to redirect users without consent using obfuscation techniques

**Risk Level:** High - Automatic execution with external network access and obfuscation indicates sophisticated attack

**Confidence Score:** 95 - Clear evidence of malicious intent through obfuscation and unauthorized URL launch

**Recommendation:** 
- Block or quarantine this PDF immediately
- Do not open in environments with JavaScript enabled
- Investigate source and distribution method
- Consider this as potential indicator of targeted attack campaign
```

### Example 2: Signature Field with JavaScript Action

**File:** `test-signature_action.pdf`

**User:** Analyze the signature field actions in examples/pdf_samples/test-signature_action.pdf

**AI Agent Analysis:**
```
# Actions Summary
- **Annotation Level**: Widget annotation (Signature field) with mouse-down action on page 1
- **Trigger**: User clicks on signature field (AnnotMouseDown event)
- **Action Type**: JavaScript execution that modifies a "Price" field value

# Behavior Analysis
- **Field Interaction**: When user clicks on the signature field "Signature_0", it triggers JavaScript execution
- **Hidden Value Modification**: The JavaScript code `var field= this.getField("Price"); field.value=100` automatically sets a "Price" field to value 100
- **User Experience**: User expects to sign the document but unknowingly triggers modification of financial data
- **Timing**: Action executes immediately upon mouse-down on signature field, before actual signing

# Security Analysis
- **Integrity Risk**: The signature action modifies document content beyond the intended signing process
- **User Deception**: User is unaware that clicking to sign will also change a price value to 100
- **Data Manipulation**: Financial or business-critical data ("Price" field) is being altered without user consent
- **Audit Trail**: This hidden modification may not be visible in standard signature audit processes
- **Trust Violation**: Undermines the integrity expectation of digital signature workflows

# Conclusion
**Scenario Overview:** PDF with signature field that contains hidden JavaScript to modify a price field when user attempts to sign

**Benign Level:** Misuse - While not overtly malicious, this represents improper use of signature actions to modify document data

**Risk Level:** Medium - Unauthorized field modification during what should be a trusted signature process poses moderate security risk

**Confidence Score:** 90 - Clear evidence of undisclosed value modification tied to signature interaction

**Recommendation:** 
- Review signature workflows for unexpected side effects
- Implement validation to ensure signature actions only perform signing-related operations
- Consider this a potential indicator of document tampering or fraudulent intent
- Audit other documents from the same source for similar hidden behaviors
```

### Example 3: Clean Document Analysis

**File:** `without_actions.pdf` (ISO PDF 2.0 specification document)

**User:** Check examples/pdf_samples/without_actions.pdf for any malicious actions

**AI Agent Analysis:**
```
# Actions Summary
- **Document Level**: No actions detected at document level
- **Page Level**: No actions detected at page level  
- **Annotation Level**: No actions detected at annotation level
- **Field Level**: No actions detected at field level
- **Overall**: Complete absence of interactive Actions throughout the 21-page document

# Behavior Analysis
- **Static Document**: This is a purely static PDF document without any interactive elements or executable content
- **Content Type**: Technical specification document (ISO/DIS 32000-2 PDF 2.0) - appears to be official ISO documentation
- **Document Structure**: Standard PDF structure with 21 pages, no form fields, no annotations with actions
- **Publisher Context**: Created with "Adobe PDF Library 15.0" and "Acrobat PDFMaker 15 for Word" - legitimate authoring tools
- **File Size**: 1,011,774 bytes indicates substantial content typical of technical documentation

# Security Analysis
- **No JavaScript**: Document contains absolutely no executable JavaScript code at any level
- **No Interactive Forms**: No AcroForm fields present that could contain hidden actions
- **No Suspicious Annotations**: No widget annotations or other interactive elements that could harbor malicious code
- **Standard PDF Structure**: Follows standard PDF 1.7 specification without suspicious modifications
- **Legitimate Metadata**: Document metadata indicates creation through standard Adobe tools for technical documentation
- **File Integrity**: Large file size and multi-page structure consistent with legitimate technical specification document

# Conclusion
**Scenario Overview:** Clean technical specification document (ISO PDF 2.0 standard) with no interactive elements or security concerns

**Benign Level:** Benign - Standard documentation PDF created through legitimate authoring tools with no suspicious characteristics

**Risk Level:** Info - Document poses no security risk and is safe for all environments including those with JavaScript enabled

**Confidence Score:** 100 - Complete absence of any Actions or interactive elements provides absolute certainty of safety

**Recommendation:** 
- Safe to open and use in any environment without restrictions
- No special precautions needed when handling this document
- Can be distributed and shared without security concerns
- Suitable for use in high-security environments
```

These examples show how the tool handles different scenarios: malicious code, suspicious behavior, and clean documents.
