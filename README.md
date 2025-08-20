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

Here's a complete example of analyzing a malicious PDF using the MCP server in VS Code with GitHub Copilot:

### Step 1: Extract Document Overview

```bash
# Using MCP tool: get_document_overview
File: examples/pdf_samples/confuse_js_code.pdf
```

**Result:**
```json
{
  "filename": "confuse_js_code.pdf",
  "basic_info": {
    "pages": 1,
    "encrypted": false,
    "pdf_version": "%PDF-1.1",
    "file_size": 850
  },
  "actions_summary": {
    "document_level_actions": {
      "DocumentOpenAction": {
        "actions": {
          "OpenAction": {
            "S": "/JavaScript",
            "JS": "var enc = \"x61x70x70x2Ex6Cx61x75x6Ex63x68x55x52x4Cx28x22x68x74x74x70x3Ax2Fx2Fx65x76x69x6Cx2Ex63x6Fx6Dx22x29\";\r\neval(unescape(enc.replace(/x/g,\"%\")));"
          }
        }
      }
    }
  }
}
```

### Step 2: Generate Security Analysis Prompt

```bash
# Using MCP tool: analyze_pdf_actions_security
```

This generates a comprehensive analysis prompt that can be used with GitHub Copilot Chat:

**Generated Analysis Prompt:**
```
# PDF Security Analysis Task

## Analysis Strategy

const char* PDF_ACTION_ANALYSIS_POLICY = R"(
- Role: PDF Security Analyst
- Background: Users are concerned about suspicious actions in PDF files that may pose security threats. They need help to inspect and assess these risks.
- Persona: You are a PDF security analyst versed in the PDF standard. You can analyze PDF actions, identify potential security risks, and provide recommendations.
- Objectives:
  - Explain action triggers and impacts.
  - Identify abuse risks and offer security advice.
  - Use tools to collect more info for risk assessment if needed.
  - Reference Adobe products vaguely in outputs.
- Workflow:
  1. Parse Events and Actions:
     - Determine if new document information is needed based on user intent and context.
     - Decode and explain obfuscated/encoded scripts. Classify as high risk if decoding fails.
     - For actions involving fields or annotations, retrieve detailed information using function calls.
  2. Verify Syntax:
     - Analyze whether the PDF supports this type of action or the current triggering event.
     - Check for syntax errors and verify the correctness of function calls and variable assignments.
     - If needed, retrieve the latest PDF JavaScript API standards and check the correctness of its usage.
  3. Behavior Analysis:
     - Explain the behavior of actions, especially those triggered by user interactions. Focus on the expected outcomes and potential risks.
     - Key Points of Behavior Analysis: 
        - 1. **Hidden Value Modification**: Modifying values outside the visible area may have hidden impacts on system logic or user behavior, and it's essential to assess whether it bypasses validation or triggers unexpected actions.
        - 2. **Dynamic Document Content Modification**: Dynamically altering document content (e.g., adding, deleting, or adjusting display status) may lead to content inconsistency or unauthorized actions, requiring a security assessment.
        - 3. **Action Chain Impact**: The execution path and final outcome of an Action chain must be analyzed to ensure compliance with expectations and to prevent unauthorized actions or data breaches.
        - 4. **Formatting vs. Content Modification**: Actions used for formatting purposes should be distinguished from those used for content modification. Actions used for formatting purposes should be considered as Info.  
  4. Security Analysis:
     - Explain the impact of actions on pages with fields or annotations.
     - If URLs are involved, verify whether the domains for data access or submission are on the trusted list.
  5. Risk Assessment:
     - Perform risk rating,benign scoring and confidence analysis based on action potential risks and evidence reliability.
  6. Summarize:
     - Summarize the analysis results, explain the confidence level, and provide actionable recommendations.
**User Input:**
Analyze the actions security of current document

**Output:**
# Actions Summary
the summary (triggers, actions types) of different level actions/dests

# Behavior Analysis
the behavior analysis of different level actions/dests, including triggers and impacts. Note: mark as the dest/goto actions which be triggered by annot/outline activated secure 

# Security Analysis
the security analysis of different level actions, furthur analysis and recommendations

# Conclusion
**Scenario Overview:** the overview of scenario
**Benign Level:** the benign level(Benign,Misuse,Abuse,Malicious) and reason
**Risk Level:** the risk level(Info,Low,Medium,High,Critical) and reason
**Confidence Score:** the confidence score (0-100) and reason
**Recommendation:** the recommendation
)";


## Document basic information
- Filename: confuse_js_code.pdf
- Pages: 1
- Encrypted: False
- PDF Version: %PDF-1.1
- File Size: 850 bytes

## Extracted Actions data
```json
{
  "document_level_actions": {
    "DocumentOpenAction": {
      "objnum": null,
      "actions": {
        "OpenAction": {
          "S": "/JavaScript",
          "JS": "var enc = \"x61x70x70x2Ex6Cx61x75x6Ex63x68x55x52x4Cx28x22x68x74x74x70x3Ax2Fx2Fx65x76x69x6Cx2Ex63x6Fx6Dx22x29\";\r\neval(unescape(enc.replace(/x/g,\"%\")));"
        }
      }
    }
  },
  "pages_level_actions": {},
  "annotations_level_actions": {},
  "field_level_actions": {}
}
```

## Analysis requirements
Please conduct a professional PDF security analysis of the Extracted Actions data based on the above strategy, focusing on:
1. Maliciousness assessment of JavaScript code
2. Risk analysis of Action triggering timing
3. Identification of potential attack vectors
4. Overall security risk level assessment
```

### Step 3: AI Analysis Result (Generated by GitHub Copilot)

**When this prompt is provided to GitHub Copilot Chat in VS Code, it generates:**

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

---

This example demonstrates how PDF Action Inspector integrates with VS Code and GitHub Copilot to provide comprehensive PDF security analysis.

## Additional Analysis Examples

### Example 2: Signature Field with JavaScript Action

**File:** `test-signature_action.pdf`

**User:** Analyze the signature field actions in this PDF

**AI Agent Analysis:**
```
# Actions Summary
- **Annotation Level**: Widget annotation (Signature field) with mouse-down action
- **Trigger**: User clicks on signature field
- **Action Type**: JavaScript execution that modifies a "Price" field value

# Behavior Analysis
- **Field Interaction**: Signature field triggers JavaScript when clicked
- **Value Modification**: Sets "Price" field to value 100 automatically
- **User Experience**: Signing action has side effect of modifying document data

# Security Analysis
- **Integrity Risk**: Signature action modifies document content beyond signing
- **User Deception**: User expects to sign but unknowingly changes financial data
- **Audit Trail**: Hidden modification may not be visible in signature process

# Conclusion
**Risk Level:** Medium - Unauthorized field modification during signature process
**Recommendation:** Review signature workflows for unexpected side effects
```

### Example 3: Clean Document Analysis

**File:** `without_actions.pdf` (ISO PDF 2.0 specification document)

**User:** Check this PDF for any malicious actions

**AI Agent Analysis:**
```
# Actions Summary
- **Document Level**: No actions detected
- **Page Level**: No actions detected  
- **Annotation Level**: No actions detected
- **Field Level**: No actions detected

# Behavior Analysis
- **Static Document**: Standard PDF document without interactive elements
- **Content Type**: Technical specification document (ISO/DIS 32000-2 PDF 2.0)
- **Publisher**: Official ISO document from Adobe/industry sources

# Security Analysis
- **No JavaScript**: Document contains no executable code
- **No Forms**: No interactive form fields present
- **Standard Structure**: Follows standard PDF specification

# Conclusion
**Risk Level:** Info - Clean document with no security concerns
**Benign Level:** Benign - Standard documentation PDF
**Recommendation:** Safe to open and use in any environment
```

These examples show how the tool handles different scenarios: malicious code, suspicious behavior, and clean documents.
