#!/usr/bin/env python3
"""
PDF Processing Utility Functions
"""

import json
import logging
from typing import Dict, Any, List, Optional

from PyPDF2 import PdfReader
from PyPDF2.generic import (
    ArrayObject,
    DictionaryObject,
    IndirectObject,
    NameObject,
    TextStringObject,
)


class PDFUtils:
    """PDF Processing Utility Class"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def get_document_basic_info(self, reader: PdfReader, file_path: str) -> Dict[str, Any]:
        """Get document basic information"""
        try:
            metadata = reader.metadata or {}
            
            return {
                "filename": file_path.split("/")[-1] if "/" in file_path else file_path.split("\\")[-1],
                "pages": len(reader.pages),
                "encrypted": reader.is_encrypted,
                "pdf_version": getattr(reader, 'pdf_header', 'Unknown'),
                "title": str(metadata.get('/Title', '')) if metadata.get('/Title') else '',
                "author": str(metadata.get('/Author', '')) if metadata.get('/Author') else '',
                "creator": str(metadata.get('/Creator', '')) if metadata.get('/Creator') else '',
                "producer": str(metadata.get('/Producer', '')) if metadata.get('/Producer') else '',
                "creation_date": str(metadata.get('/CreationDate', '')) if metadata.get('/CreationDate') else '',
                "modification_date": str(metadata.get('/ModDate', '')) if metadata.get('/ModDate') else ''
            }
        except Exception as e:
            self.logger.error(f"Failed to get document basic information: {e}")
            return {"error": str(e)}
    
    def extract_text_from_page(self, reader: PdfReader, page_number: int) -> Dict[str, Any]:
        """Extract text from specified page"""
        try:
            if page_number >= len(reader.pages):
                return {"error": f"Page number out of range: {page_number}"}
            
            page = reader.pages[page_number]
            text_content = page.extract_text()
            
            # Get page information
            mediabox = page.mediabox if hasattr(page, 'mediabox') else None
            rotation = page.get('/Rotate', 0)
            
            return {
                "page_number": page_number,
                "text_content": text_content,
                "text_length": len(text_content),
                "metadata": {
                    "mediabox": [float(x) for x in mediabox] if mediabox else None,
                    "rotation": rotation
                }
            }
        except Exception as e:
            self.logger.error(f"Failed to extract page text: {e}")
            return {"error": str(e)}
    
    def parse_trailer_object(self, reader: PdfReader) -> Dict[str, Any]:
        """Parse PDF Trailer object"""
        try:
            trailer = reader.trailer
            
            result = {
                "trailer_keys": list(trailer.keys()) if trailer else [],
                "analysis": {
                    "has_root": "/Root" in trailer if trailer else False,
                    "has_info": "/Info" in trailer if trailer else False,
                    "encrypted": "/Encrypt" in trailer if trailer else False,
                    "has_previous_xref": "/Prev" in trailer if trailer else False
                }
            }
            
            # Safely extract trailer content
            if trailer:
                safe_trailer = {}
                for key, value in trailer.items():
                    try:
                        if isinstance(value, (str, int, float, bool)):
                            safe_trailer[str(key)] = value
                        elif isinstance(value, IndirectObject):
                            safe_trailer[str(key)] = f"IndirectObject({value.idnum}, {value.generation})"
                        else:
                            safe_trailer[str(key)] = str(type(value).__name__)
                    except:
                        safe_trailer[str(key)] = "UnparsableValue"
                
                result["trailer_content"] = safe_trailer
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to parse Trailer object: {e}")
            return {"error": str(e)}
    
    def find_form_fields_by_name(self, reader: PdfReader, field_name: str) -> Dict[str, Any]:
        """Find form fields by name"""
        try:
            result = {
                "field_name": field_name,
                "found_fields": [],
                "total_found": 0
            }
            
            # Check if there are forms
            if "/AcroForm" not in reader.trailer.get("/Root", {}):
                return result
            
            # Recursively search fields
            def search_fields(fields, parent_name=""):
                if not fields:
                    return
                
                for field in fields:
                    if isinstance(field, IndirectObject):
                        field = field.get_object()
                    
                    if not isinstance(field, DictionaryObject):
                        continue
                    
                    # Get field name
                    current_name = field.get("/T", "")
                    if isinstance(current_name, TextStringObject):
                        current_name = str(current_name)
                    
                    full_name = f"{parent_name}.{current_name}" if parent_name else current_name
                    
                    # Check if it matches
                    if field_name.lower() in full_name.lower():
                        field_info = {
                            "name": full_name,
                            "type": str(field.get("/FT", "Unknown")),
                            "value": str(field.get("/V", "")),
                            "flags": field.get("/Ff", 0)
                        }
                        result["found_fields"].append(field_info)
                    
                    # Recursively search child fields
                    kids = field.get("/Kids")
                    if kids:
                        search_fields(kids, full_name)
            
            # Start searching
            acro_form = reader.trailer["/Root"].get("/AcroForm")
            if acro_form:
                acro_form = acro_form.get_object() if isinstance(acro_form, IndirectObject) else acro_form
                fields = acro_form.get("/Fields", [])
                search_fields(fields)
            
            result["total_found"] = len(result["found_fields"])
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to find form fields: {e}")
            return {"error": str(e)}
    
    def get_pdf_object_info(self, reader: PdfReader, object_number: int) -> Dict[str, Any]:
        """Get PDF object information"""
        try:
            result = {
                "object_number": object_number,
                "found": False,
                "object_info": {}
            }
            
            # Try to get object
            try:
                obj = reader.get_object((object_number, 0))
                result["found"] = True
                result["object_info"] = {
                    "type": type(obj).__name__,
                    "keys": list(obj.keys()) if hasattr(obj, 'keys') else [],
                    "size": len(obj) if hasattr(obj, '__len__') else "Unknown"
                }
                
                # If it's a dictionary object, try to get some safe key-values
                if isinstance(obj, DictionaryObject):
                    safe_content = {}
                    for key, value in obj.items():
                        try:
                            if isinstance(value, (str, int, float, bool)):
                                safe_content[str(key)] = value
                            elif isinstance(value, NameObject):
                                safe_content[str(key)] = str(value)
                            else:
                                safe_content[str(key)] = type(value).__name__
                        except:
                            safe_content[str(key)] = "UnparsableValue"
                    
                    result["object_info"]["content_sample"] = safe_content
                
            except Exception:
                result["found"] = False
                result["error"] = f"Object {object_number} does not exist or cannot be accessed"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to get PDF object information: {e}")
            return {"error": str(e)}
    
    def parse_page_spans(self, page_spans: str, total_pages: int) -> List[int]:
        """Parse page range string"""
        try:
            pages = []
            parts = page_spans.split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range format: 0-2
                    start, end = part.split('-', 1)
                    start = int(start.strip())
                    end = int(end.strip())
                    pages.extend(range(max(0, start), min(total_pages, end + 1)))
                else:
                    # Single page format: 5
                    page_num = int(part.strip())
                    if 0 <= page_num < total_pages:
                        pages.append(page_num)
            
            return sorted(list(set(pages)))  # Remove duplicates and sort
            
        except Exception as e:
            self.logger.error(f"Failed to parse page range: {e}")
            return []


# Global PDF utils instance
pdf_utils = PDFUtils()
