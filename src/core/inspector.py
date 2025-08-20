#!/usr/bin/env python3
"""
PDF Action Inspector Core Class
"""

import json
import logging
from typing import Dict, Any, Optional

from ..config.settings import settings
from ..config.policies import PDF_ACTION_ANALYSIS_POLICY
from ..core.cache_manager import cache_manager
from ..core.error_handler import error_handler, PDFProcessingError
from ..utils.pdf_utils import pdf_utils
from ..utils.action_extractor import action_extractor


class PDFActionInspector:
    """PDF Action analyzer core class"""
    
    def __init__(self, cache_manager_instance=None, error_handler_instance=None):
        self.logger = logging.getLogger(__name__)
        settings.setup_logging()
        
        # Use passed instances or default global instances
        self.cache_manager = cache_manager_instance or cache_manager
        self.error_handler = error_handler_instance or error_handler
        
        # Use built-in analysis policy
        self.policy_text = PDF_ACTION_ANALYSIS_POLICY
        
        self.logger.info("PDFActionInspector initialization complete")
    
    def analyze_pdf_actions_security(self, file_path: str, password: Optional[str] = None) -> str:
        """Generate PDF Actions security analysis prompt, containing policy and data"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            
            # Get document basic information
            basic_info = pdf_utils.get_document_basic_info(reader, file_path)
            
            # Extract all Actions data
            all_actions = action_extractor.extract_all_actions(reader)
            
            # Generate analysis prompt
            prompt = f"""# PDF Security Analysis Task

## Analysis Strategy
{self.policy_text}

## Document basic information
- Filename: {basic_info.get('filename', 'Unknown')}
- Pages: {basic_info.get('pages', 0)}
- Encrypted: {basic_info.get('encrypted', False)}
- PDF Version: {basic_info.get('pdf_version', 'Unknown')}
- File Size: {self._get_file_size(file_path)} bytes

## Extracted Actions data
```json
{json.dumps(all_actions, ensure_ascii=False, indent=2)}
```

## Analysis requirements
Please conduct a professional PDF security analysis of the Extracted Actions data based on the above strategy, focusing on:
1. Maliciousness assessment of JavaScript code
2. Risk analysis of Action triggering timing
3. Identification of potential attack vectors
4. Overall security risk level assessment
"""
            
            return prompt
            
        except PDFProcessingError as e:
            self.logger.error(f"PDF processing error: {e}")
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            self.logger.error(f"Failed to generate analysis prompt: {e}")
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def extract_pdf_actions(self, file_path: str, password: Optional[str] = None) -> str:
        """Pure PDF Actions data extraction, no analysis"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            
            # Extract all Actions - return complete structured data
            all_actions = action_extractor.extract_all_actions(reader)
            
            return json.dumps(all_actions, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            self.logger.error(f"PDF processing error: {e}")
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            self.logger.error(f"Failed to extract PDF Actions: {e}")
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_document_overview(self, file_path: str, password: Optional[str] = None) -> str:
        """Get PDF document overview"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            
            # Basic information
            basic_info = pdf_utils.get_document_basic_info(reader, file_path)
            
            # Structure information
            structure_info = self._analyze_document_structure(reader)
            
            # Actions raw data
            actions_data = action_extractor.extract_all_actions(reader)
            
            overview = {
                "filename": basic_info.get("filename", ""),
                "basic_info": {
                    "pages": basic_info.get("pages", 0),
                    "encrypted": basic_info.get("encrypted", False),
                    "pdf_version": basic_info.get("pdf_version", ""),
                    "file_size": self._get_file_size(file_path)
                },
                "metadata": {
                    "title": basic_info.get("title", ""),
                    "author": basic_info.get("author", ""),
                    "creator": basic_info.get("creator", ""),
                    "producer": basic_info.get("producer", ""),
                    "creation_date": basic_info.get("creation_date", ""),
                    "modification_date": basic_info.get("modification_date", "")
                },
                "structure": structure_info,
                "actions_summary": {
                    "document_level_actions": actions_data.get("document_level_actions", {}),
                    "pages_level_actions": actions_data.get("pages_level_actions", {}),
                    "annotations_level_actions": actions_data.get("annotations_level_actions", {}),
                    "field_level_actions": actions_data.get("field_level_actions", {}),
                    "total_actions": actions_data.get("total_actions", 0),
                    "action_types": actions_data.get("action_types", {})
                }
            }
            
            return json.dumps(overview, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_page_text_content(self, file_path: str, page_number: int = 0, password: Optional[str] = None) -> str:
        """Get page text content"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            result = pdf_utils.extract_text_from_page(reader, page_number)
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def load_all_annotations(self, file_path: str, password: Optional[str] = None) -> str:
        """Load all annotations"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            annotations = self._extract_all_annotations(reader)
            return json.dumps(annotations, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_trailer_object(self, file_path: str, password: Optional[str] = None) -> str:
        """Get Trailer object"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            result = pdf_utils.parse_trailer_object(reader)
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_fields_by_name(self, file_path: str, field_name: str, password: Optional[str] = None) -> str:
        """Find fields by name"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            result = pdf_utils.find_form_fields_by_name(reader, field_name)
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_pdf_object_information(self, file_path: str, object_number: int, password: Optional[str] = None) -> str:
        """Get PDF object information"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            result = pdf_utils.get_pdf_object_info(reader, object_number)
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def load_all_annotations_in_page(self, file_path: str, page_index: int, password: Optional[str] = None) -> str:
        """Load annotations from specified page"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            annotations = self._extract_page_annotations(reader, page_index)
            return json.dumps(annotations, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_page_information_by_spans(self, file_path: str, page_spans: str, password: Optional[str] = None) -> str:
        """Get information by page ranges"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            
            # Parse page ranges
            pages = pdf_utils.parse_page_spans(page_spans, len(reader.pages))
            
            result = {
                "page_spans": page_spans,
                "parsed_indices": pages,
                "total_pages": len(reader.pages),
                "pages_info": []
            }
            
            for page_num in pages:
                page_info = pdf_utils.extract_text_from_page(reader, page_num)
                result["pages_info"].append(page_info)
            
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    def get_page_index_by_pdfobjnum(self, file_path: str, obj_num: int, password: Optional[str] = None) -> str:
        """Find page by object number"""
        try:
            reader = self.cache_manager.get_reader(file_path, password)
            
            result = {
                "object_number": obj_num,
                "found_pages": [],
                "total_matches": 0
            }
            
            # Iterate through all pages to find object references
            for page_num, page in enumerate(reader.pages):
                if hasattr(page, 'indirect_reference'):
                    if page.indirect_reference.idnum == obj_num:
                        result["found_pages"].append(page_num)
            
            result["total_matches"] = len(result["found_pages"])
            return json.dumps(result, ensure_ascii=False, indent=2)
            
        except PDFProcessingError as e:
            return self.error_handler.create_error_response(e.error_type, e.message, file_path)
        except Exception as e:
            return self.error_handler.handle_pdf_error(file_path, e)
    
    # Management methods
    def set_password(self, file_path: str, password: str):
        """Set file password"""
        cache_manager.set_password(file_path, password)
    
    def clear_cache(self, file_path: Optional[str] = None):
        """Clear cache"""
        cache_manager.clear_cache(file_path)
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get cache status"""
        return cache_manager.get_cache_status()
    
    # Private methods
    def _analyze_document_structure(self, reader) -> Dict[str, Any]:
        """Analyze document structure"""
        try:
            catalog = reader.trailer.get("/Root", {})
            if hasattr(catalog, 'get_object'):
                catalog = catalog.get_object()
            
            return {
                "has_acroform": "/AcroForm" in catalog,
                "has_bookmarks": "/Outlines" in catalog,
                "has_javascript": "/JavaScript" in catalog or "/JS" in catalog,
                "page_count": len(reader.pages)
            }
        except:
            return {"error": "Unable to analyze document structure"}
    
    def _get_file_size(self, file_path: str) -> int:
        """Get file size"""
        try:
            import os
            return os.path.getsize(file_path)
        except:
            return 0
    
    def _extract_all_annotations(self, reader) -> Dict[str, Any]:
        """Extract all annotations"""
        # Can reuse annotation extraction logic from action_extractor
        annotations_data = action_extractor.extract_annotation_actions(reader)
        return {
            "total_annotations": len(annotations_data),
            "annotations": annotations_data
        }
    
    def _extract_page_annotations(self, reader, page_index: int) -> Dict[str, Any]:
        """Extract annotations from specified page"""
        try:
            if page_index >= len(reader.pages):
                return {"error": f"Page index out of range: {page_index}"}
            
            page = reader.pages[page_index]
            annotations = page.get("/Annots", [])
            
            result = {
                "page_index": page_index,
                "annotations_count": len(annotations),
                "annotations": []
            }
            
            for annot in annotations:
                if hasattr(annot, 'get_object'):
                    annot = annot.get_object()
                
                annot_info = {
                    "subtype": str(annot.get("/Subtype", "Unknown")),
                    "rect": [float(x) for x in annot.get("/Rect", [])],
                    "contents": str(annot.get("/Contents", "")),
                    "has_action": "/A" in annot or "/AA" in annot
                }
                result["annotations"].append(annot_info)
            
            return result
            
        except Exception as e:
            return {"error": str(e)}


# Global Inspector instance
pdf_inspector = PDFActionInspector()
