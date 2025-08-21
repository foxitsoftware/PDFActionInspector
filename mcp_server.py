#!/usr/bin/env python3
"""
PDF Action Inspector MCP Server Main File
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastmcp import FastMCP
from src.core.inspector import PDFActionInspector
from src.core.cache_manager import CacheManager
from src.core.error_handler import ErrorHandler
from src.config.settings import Settings


# Initialize MCP application
mcp = FastMCP("PDF Action Inspector MCP Server")

# Initialize global components
settings = Settings()
cache_manager = CacheManager()
error_handler = ErrorHandler()
pdf_inspector = PDFActionInspector(cache_manager, error_handler)


# PDF analysis tools
@mcp.tool()
def analyze_pdf_actions_security(file_path: str) -> str:
    """
    Generate PDF Actions security analysis prompt
    
    Extract all Actions data from PDF file and combine with predefined 
    security analysis strategies to generate complete analysis prompt.
    The prompt contains analysis strategies, document basic information, 
    extracted Actions data and analysis requirements.
    
    Args:
        file_path: Absolute or relative path to the PDF file
        
    Returns:
        Complete analysis prompt containing analysis strategies and Actions data
        
    Example:
        prompt = analyze_pdf_actions_security("sample.pdf")
        # Provide prompt to AI for security analysis
        
    Note:
        - Returns analysis prompt, not analysis results
        - Contains complete analysis strategies and extracted Actions data
        - Requires AI to perform actual security analysis based on this prompt
    """
    return pdf_inspector.analyze_pdf_actions_security(file_path)


@mcp.tool()
def extract_pdf_actions(file_path: str) -> str:
    """
    Pure extraction of Actions data from PDF file
    
    Extract Actions from all levels of the PDF file and return structured JSON data,
    without any analysis or evaluation.
    
    Args:
        file_path: Absolute or relative path to the PDF file
        
    Returns:
        JSON format Actions data containing:
            - document_level_actions: Document level Actions
            - pages_level_actions: Page level Actions
            - annotations_level_actions: Annotation level Actions
            - field_level_actions: Field level Actions
            
    Example:
        actions = extract_pdf_actions("sample.pdf")
        data = json.loads(actions)
        
    Note:
        - This method only extracts data, does not perform any analysis
        - Returns raw PDF Actions structure
    """
    result = pdf_inspector.extract_pdf_actions(file_path)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_document_overview(file_path: str) -> str:
    """
    Get complete structural overview of PDF document
    
    Provides comprehensive information about PDF document, including basic info, 
    document structure, functional features and statistical data.
    
    Args:
        file_path: Absolute or relative path to PDF file
        
    Returns:
        JSON format document overview information containing:
            - basic_info: Basic information (pages, file size, encryption status, etc.)
            - structure: Document structure (whether contains forms, annotations, JavaScript, etc.)
            - features: Feature statistics (Actions count, annotations count, etc.)
            
    Example:
        overview = get_document_overview("sample.pdf")
        data = json.loads(overview)
        print(f"Pages: {data['basic_info']['pages']}")
        
    Note:
        - Returns JSON format string, needs parsing after use
        - Contains security-related feature statistics of document
    """
    result = pdf_inspector.get_document_overview(file_path)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def load_all_annotations(file_path: str) -> str:
    """
    Load all annotations in PDF file and analyze their Actions
    
    Extract all types of annotations in PDF, including Widget annotations (form fields), 
    text annotations, link annotations, etc., and analyze Actions associated with each annotation.
    
    Args:
        file_path: Absolute or relative path to PDF file
        
    Returns:
        JSON format annotation information containing:
            - total_annotations: Total number of annotations
            - annotations: List of annotations, each annotation containing:
                - subtype: Annotation type
                - page: Page location (starting from 0)
                - rect: Annotation position coordinates [x1, y1, x2, y2]
                - actions: List of associated Actions
                - widget_info: Form field information (if Widget annotation)
                
    Example:
        annotations = load_all_annotations("sample.pdf")
        data = json.loads(annotations)
        for annot in data['annotations']:
            print(f"Annotation type: {annot['subtype']}, Actions: {len(annot['actions'])}")
            
    Note:
        - Pay special attention to Widget annotations, these usually contain form fields and related JavaScript
        - Actions information contains trigger conditions and specific Action types
    """
    return pdf_inspector.load_all_annotations(file_path)


@mcp.tool()
def get_page_text_content(file_path: str, page_number: int = 0) -> str:
    """
    Extract text content and metadata from specified PDF page
    
    Extract all visible text content from specified page of PDF, 
    while providing basic information about the page.
    
    Args:
        file_path: Absolute or relative path to PDF file
        page_number: Page number starting from 0. Default is 0 (first page)
        
    Returns:
        JSON format page information containing:
            - page_number: Page number
            - text_content: Text content of the page
            - metadata: Page metadata (such as media box, rotation angle, etc.)
            
    Example:
        page_content = get_page_text_content("sample.pdf", 0)
        data = json.loads(page_content)
        print(f"Page {data['page_number']} text: {data['text_content']}")
        
    Note:
        - Page numbers start from 0, ensure not exceeding document page range
        - Text from some PDFs may not be extracted correctly (such as scanned PDFs)
        - Returned text maintains original format and line breaks
    """
    result = pdf_inspector.get_page_text_content(file_path, page_number)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_trailer_object(file_path: str) -> str:
    """
    Get PDF file Trailer object and document structure information
    
    Extract PDF file's Trailer dictionary, which is important structural information 
    of PDF file, containing root object references, encryption information, 
    document information and other key data.
    
    Args:
        file_path: Absolute or relative path to PDF file
        
    Returns:
        JSON format Trailer information containing:
            - trailer: Content of Trailer dictionary
            - analysis: Analysis results:
                - has_root: Whether has root object
                - has_info: Whether has info object
                - encrypted: Whether encrypted
                - has_previous_xref: Whether has previous cross-reference table
                
    Example:
        trailer = get_trailer_object("sample.pdf")
        data = json.loads(trailer)
        if data['analysis']['encrypted']:
            print("PDF file is encrypted")
            
    Note:
        - Trailer is key information of PDF internal structure
        - Encryption information is important for security analysis
        - Some object references may need further parsing
    """
    result = pdf_inspector.get_trailer_object(file_path)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_fields_by_name(file_path: str, field_name: str) -> str:
    """
    Get PDF form field information by field name
    
    Search for form fields with specified name in PDF document and return detailed 
    field information. Supports fuzzy matching, will find all fields whose names 
    contain the specified string.
    
    Args:
        file_path: Absolute or relative path to PDF file
        field_name: Field name to search for (supports partial matching)
        
    Returns:
        JSON format field information containing:
            - field_name: Searched field name
            - found_fields: List of matching fields
            - total_found: Number of fields found
            
    Example:
        fields = get_fields_by_name("sample.pdf", "signature")
        data = json.loads(fields)
        for field in data['found_fields']:
            print(f"Field: {field['name']}, Type: {field['type']}")
    """
    result = pdf_inspector.get_fields_by_name(file_path, field_name)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def get_pdf_object_information(file_path: str, object_number: int) -> str:
    """
    Get detailed information of specified object in PDF file
    
    Extract object content and type information for specific object number in PDF.
    Can be used for in-depth analysis of PDF internal structure and object relationships.
    
    Args:
        file_path: Absolute or relative path to PDF file
        object_number: PDF object number
        
    Returns:
        JSON format object information containing:
            - object_number: Object number
            - found: Whether the object was found
            - object_info: Detailed object information (type, key list, size, etc.)
            
    Example:
        obj_info = get_pdf_object_information("sample.pdf", 5)
        data = json.loads(obj_info)
        if data['found']:
            print(f"Object type: {data['object_info']['type']}")
    """
    result = pdf_inspector.get_pdf_object_information(file_path, object_number)
    return json.dumps(result, ensure_ascii=False, indent=2)


# Advanced analysis tools
@mcp.tool()
def load_all_annotations_in_page(file_path: str, page_index: int) -> str:
    """
    Load all annotations for specified page
    
    Args:
        file_path: PDF file path
        page_index: Page index (starting from 0)
        
    Returns:
        Annotation information for specified page
    """
    return pdf_inspector.load_all_annotations_in_page(file_path, page_index)


@mcp.tool()
def get_page_information_by_spans(file_path: str, page_spans: str) -> str:
    """
    Get information for multiple pages by page range
    
    Args:
        file_path: PDF file path
        page_spans: Page range, supported formats: "0", "0-2", "1,3,5", "0-2,5,7-9"
        
    Returns:
        Information for pages within specified range
    """
    return pdf_inspector.get_page_information_by_spans(file_path, page_spans)


@mcp.tool()
def get_page_index_by_pdfobjnum(file_path: str, obj_num: int) -> str:
    """
    Find the page containing object by PDF object number
    
    Args:
        file_path: PDF file path
        obj_num: PDF object number
        
    Returns:
        Information about page containing the object
    """
    return pdf_inspector.get_page_index_by_pdfobjnum(file_path, obj_num)


# Management tools
@mcp.tool()
def clear_pdf_cache(file_path: str = None) -> str:
    """
    Clear PDF cache
    
    Args:
        file_path: Optional specific file path, if not provided clears all cache
        
    Returns:
        Operation result
    """
    try:
        pdf_inspector.clear_cache(file_path)
        if file_path:
            return f"Cleared cache for file {file_path}"
        else:
            return "All cache cleared"
    except Exception as e:
        return f"Failed to clear cache: {str(e)}"


@mcp.tool()
def get_cache_status() -> str:
    """
    Get cache status information
    
    Returns:
        Cache status information
    """
    try:
        status = pdf_inspector.get_cache_status()
        return json.dumps(status, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Failed to get cache status: {str(e)}"


@mcp.tool()
def set_pdf_password(file_path: str, password: str) -> str:
    """
    Set and verify password for encrypted PDF file
    
    Store password for specific PDF file and immediately verify it works
    by attempting to open the PDF. This allows processing of encrypted PDFs
    by providing the correct password.
    
    Args:
        file_path: Absolute or relative path to the PDF file
        password: Password for the encrypted PDF file
        
    Returns:
        Success message if password is correct, error message if incorrect
        
    Example:
        set_pdf_password("encrypted.pdf", "mypassword123")
        
    Note:
        - Password is verified immediately by attempting to open the PDF
        - Only correct passwords are stored in memory for the current session
        - If password is incorrect, an error is returned and password is not stored
        - Successful password will be used automatically for subsequent operations
    """
    try:
        cache_manager.set_password(file_path, password)
        return json.dumps({
            "success": True,
            "message": f"Password verified and set for file: {file_path}",
            "file_path": file_path
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to set password: {str(e)}",
            "file_path": file_path
        }, ensure_ascii=False, indent=2)


def main():
    """Main entry point for console script"""
    # Set environment variables (if needed)
    if "PDF_CACHE_TIMEOUT_SECONDS" not in os.environ:
        os.environ["PDF_CACHE_TIMEOUT_SECONDS"] = "120"  # 120 seconds default timeout
    
    mcp.run()


if __name__ == "__main__":
    main()
