#!/usr/bin/env python3
"""
PDF Action Extractor
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


class ActionExtractor:
    """PDF Action Extractor"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def extract_all_actions(self, reader: PdfReader) -> Dict[str, Any]:
        """Extract all Actions, returning data organized by hierarchy"""
        result = {
            "document_level_actions": {},
            "pages_level_actions": {},
            "annotations_level_actions": {},
            "field_level_actions": {}
        }
        
        try:
            # Extract Document level Actions
            doc_actions = self._extract_document_level_actions(reader)
            result["document_level_actions"] = doc_actions
            
            # Extract Page level Actions  
            page_actions = self._extract_pages_level_actions(reader)
            result["pages_level_actions"] = page_actions
            
            # Extract Annotation level Actions
            annotation_actions = self._extract_annotations_level_actions(reader)
            result["annotations_level_actions"] = annotation_actions
            
            # Extract Field level Actions
            field_actions = self._extract_field_level_actions(reader)
            result["field_level_actions"] = field_actions
            
        except Exception as e:
            self.logger.error(f"Failed to extract Actions: {e}")
            result["error"] = str(e)
        
        return result
    
    def _extract_document_level_actions(self, reader: PdfReader) -> Dict[str, Any]:
        """Extract Document level Actions"""
        document_actions = {}
        
        try:
            catalog = reader.trailer.get("/Root")
            if not catalog:
                return document_actions
            
            if isinstance(catalog, IndirectObject):
                catalog = catalog.get_object()
            
            # Check OpenAction
            open_action = catalog.get("/OpenAction")
            if open_action:
                action_data = self._parse_action_details(open_action)
                if action_data:
                    document_actions["DocumentOpenAction"] = {
                        "objnum": getattr(open_action, "idnum", None) if isinstance(open_action, IndirectObject) else None,
                        "actions": {"OpenAction": action_data}
                    }
            
            # Check Additional Actions
            aa = catalog.get("/AA")
            if aa:
                if isinstance(aa, IndirectObject):
                    aa = aa.get_object()
                
                aa_actions = {}
                for trigger in ["/WC", "/WS", "/DS", "/WP", "/DP"]:
                    if trigger in aa:
                        action_data = self._parse_action_details(aa[trigger])
                        if action_data:
                            aa_actions[trigger[1:]] = action_data
                
                if aa_actions:
                    document_actions["DocumentAdditionalActions"] = {
                        "objnum": getattr(aa, "idnum", None) if isinstance(catalog.get("/AA"), IndirectObject) else None,
                        "actions": aa_actions
                    }
                        
        except Exception as e:
            self.logger.error(f"Failed to extract Document level Actions: {e}")
        
        return document_actions
    
    def _extract_pages_level_actions(self, reader: PdfReader) -> Dict[str, Any]:
        """Extract Page level Actions"""
        pages_actions = {}
        
        try:
            for page_num, page in enumerate(reader.pages):
                page_actions = {}
                
                # Check page Additional Actions
                aa = page.get("/AA")
                if aa:
                    if isinstance(aa, IndirectObject):
                        aa = aa.get_object()
                    
                    for trigger in ["/O", "/C"]:  # Open/Close
                        if trigger in aa:
                            action_data = self._parse_action_details(aa[trigger])
                            if action_data:
                                page_actions[trigger[1:]] = action_data
                
                if page_actions:
                    pages_actions[f"page_{page_num}_actions"] = {
                        "objnum": getattr(page, "idnum", None) if hasattr(page, "idnum") else None,
                        "page_number": page_num,
                        "actions": page_actions
                    }
                        
        except Exception as e:
            self.logger.error(f"Failed to extract Page level Actions: {e}")
        
        return pages_actions
    
    def _extract_annotations_level_actions(self, reader: PdfReader) -> Dict[str, Any]:
        """Extract Annotation level Actions"""
        annotations_actions = {}
        
        try:
            for page_num, page in enumerate(reader.pages):
                annotations = page.get("/Annots", [])
                
                # Handle case where annotations might be an IndirectObject
                if isinstance(annotations, IndirectObject):
                    annotations = annotations.get_object()
                
                # Ensure annotations is a list/array
                if not isinstance(annotations, (list, ArrayObject)):
                    continue
                
                for annot_num, annot in enumerate(annotations):
                    if isinstance(annot, IndirectObject):
                        annot_obj = annot.get_object()
                        annot_objnum = annot.idnum
                    else:
                        annot_obj = annot
                        annot_objnum = None
                    
                    # Get annotation type and detailed info
                    subtype = str(annot_obj.get("/Subtype", "Unknown"))
                    annot_actions = {}
                    field_details = {}
                    
                    # If it's a Widget annotation, extract field info
                    if subtype == "/Widget":
                        field_details = self._extract_field_details(annot_obj)
                    
                    # Check Action (/A)
                    action = annot_obj.get("/A")
                    if action:
                        action_data = self._parse_action_details(action)
                        if action_data:
                            annot_actions["Action"] = action_data
                    
                    # Check Additional Actions (/AA)
                    aa = annot_obj.get("/AA")
                    if aa:
                        if isinstance(aa, IndirectObject):
                            aa = aa.get_object()
                        
                        # Common annotation triggers
                        for trigger in ["/E", "/X", "/D", "/U", "/Fo", "/Bl", "/PO", "/PC", "/PV", "/PI"]:
                            if trigger in aa:
                                action_data = self._parse_action_details(aa[trigger])
                                if action_data:
                                    trigger_name = {
                                        "/E": "AnnotMouseEnter",
                                        "/X": "AnnotMouseExit", 
                                        "/D": "AnnotMouseDown",
                                        "/U": "AnnotMouseUp",
                                        "/Fo": "AnnotFocus",
                                        "/Bl": "AnnotBlur",
                                        "/PO": "AnnotPageOpen",
                                        "/PC": "AnnotPageClose",
                                        "/PV": "AnnotPageVisible",
                                        "/PI": "AnnotPageInvisible"
                                    }.get(trigger, trigger[1:])
                                    annot_actions[trigger_name] = action_data
                    
                    if annot_actions:
                        key = f"actions of page_{page_num}_annot_{annot_num}({subtype.strip('/')})"
                        if field_details.get("name"):
                            key += f"[{field_details.get('type', '')} field]"
                        
                        annotations_actions[key] = {
                            "objnum": annot_objnum,
                            "page": page_num,
                            "annotation_type": subtype,
                            "actions": annot_actions
                        }
                        
                        if field_details:
                            annotations_actions[key]["field_details"] = field_details
                        
        except Exception as e:
            self.logger.error(f"Failed to extract Annotation level Actions: {e}")
        
        return annotations_actions
    
    def _extract_field_level_actions(self, reader: PdfReader) -> Dict[str, Any]:
        """Extract Field level Actions (form fields)"""
        field_actions = {}
        
        try:
            catalog = reader.trailer.get("/Root")
            if not catalog:
                return field_actions
            
            if isinstance(catalog, IndirectObject):
                catalog = catalog.get_object()
            
            acroform = catalog.get("/AcroForm")
            if not acroform:
                return field_actions
            
            if isinstance(acroform, IndirectObject):
                acroform = acroform.get_object()
            
            fields = acroform.get("/Fields", [])
            
            # Handle case where fields might be an IndirectObject
            if isinstance(fields, IndirectObject):
                fields = fields.get_object()
            
            # Ensure fields is a list/array
            if not isinstance(fields, (list, ArrayObject)):
                return field_actions
            
            for field_num, field in enumerate(fields):
                if isinstance(field, IndirectObject):
                    field_obj = field.get_object()
                    field_objnum = field.idnum
                else:
                    field_obj = field
                    field_objnum = None
                
                field_details = self._extract_field_details(field_obj)
                field_actions_dict = {}
                
                # Check field Actions
                aa = field_obj.get("/AA")
                if aa:
                    if isinstance(aa, IndirectObject):
                        aa = aa.get_object()
                    
                    # Field-specific triggers
                    for trigger in ["/K", "/F", "/V", "/C"]:
                        if trigger in aa:
                            action_data = self._parse_action_details(aa[trigger])
                            if action_data:
                                trigger_name = {
                                    "/K": "FieldKeystroke",
                                    "/F": "FieldFormat", 
                                    "/V": "FieldValidate",
                                    "/C": "FieldCalculate"
                                }.get(trigger, trigger[1:])
                                field_actions_dict[trigger_name] = action_data
                
                if field_actions_dict:
                    field_name = field_details.get("name", f"field_{field_num}")
                    field_type = field_details.get("type", "Unknown")
                    
                    key = f"field_{field_name}({field_type})"
                    field_actions[key] = {
                        "objnum": field_objnum,
                        "field_details": field_details,
                        "actions": field_actions_dict
                    }
                        
        except Exception as e:
            self.logger.error(f"Failed to extract Field level Actions: {e}")
        
        return field_actions
    
    def _extract_field_details(self, field_obj) -> Dict[str, Any]:
        """Extract field detailed information"""
        details = {}
        
        try:
            details["name"] = str(field_obj.get("/T", ""))
            details["type"] = str(field_obj.get("/FT", "")).strip("/")
            details["value"] = str(field_obj.get("/V", ""))
            details["default_value"] = str(field_obj.get("/DV", ""))
            details["flags"] = str(field_obj.get("/Ff", "0"))
            details["alternative_name "] = str(field_obj.get("/TU", ""))
                        
        except Exception as e:
            self.logger.error(f"Failed to extract field details: {e}")
        
        return details
    
    def _parse_action_details(self, action) -> Dict[str, Any]:
        """Parse Action detailed information"""
        if not action:
            return {}
        
        try:
            if isinstance(action, IndirectObject):
                action = action.get_object()
            
            if not isinstance(action, DictionaryObject):
                return {}
            
            action_details = {}
            
            # Action type
            s_type = action.get("/S")
            if s_type:
                action_details["S"] = str(s_type)
            
            # JavaScript code
            js_code = action.get("/JS")
            if js_code:
                if isinstance(js_code, IndirectObject):
                    js_code = js_code.get_object()
                action_details["JS"] = str(js_code)
            
            # URI
            uri = action.get("/URI")
            if uri:
                action_details["URI"] = str(uri)
            
            # File specification
            f = action.get("/F")
            if f:
                action_details["F"] = str(f)
            
            # Other common Action parameters
            for key in ["/D", "/NewWindow", "/Fields", "/Flags"]:
                if key in action:
                    action_details[key[1:]] = str(action[key])
            
            return action_details
            
        except Exception as e:
            self.logger.error(f"Failed to parse Action details: {e}")
            return {}
    
    def _extract_document_actions(self, reader: PdfReader) -> List[Dict[str, Any]]:
        """Extract Document level Actions"""
        actions = []
        
        try:
            catalog = reader.trailer.get("/Root")
            if not catalog:
                return actions
            
            if isinstance(catalog, IndirectObject):
                catalog = catalog.get_object()
            
            # Check OpenAction
            open_action = catalog.get("/OpenAction")
            if open_action:
                action_info = self._parse_action(open_action, "DocumentOpen")
                if action_info:
                    actions.append(action_info)
            
            # Check other Document level Actions
            for key in ["/AA", "/OpenAction"]:
                if key in catalog:
                    action_info = self._parse_action(catalog[key], f"Document{key[1:]}")
                    if action_info:
                        actions.append(action_info)
                        
        except Exception as e:
            self.logger.error(f"Failed to extract Document level Actions: {e}")
        
        return actions
    
    def _extract_page_actions(self, reader: PdfReader) -> List[Dict[str, Any]]:
        """Extract Page level Actions"""
        actions = []
        
        try:
            for page_num, page in enumerate(reader.pages):
                # Check page Actions
                if "/AA" in page:
                    aa_actions = page["/AA"]
                    if isinstance(aa_actions, IndirectObject):
                        aa_actions = aa_actions.get_object()
                    
                    if isinstance(aa_actions, DictionaryObject):
                        for trigger, action in aa_actions.items():
                            action_info = self._parse_action(action, f"Page{trigger}")
                            if action_info:
                                action_info["page_number"] = page_num
                                actions.append(action_info)
                
        except Exception as e:
            self.logger.error(f"Failed to extract Page level Actions: {e}")
        
        return actions
    
    def _extract_annotation_actions(self, reader: PdfReader) -> List[Dict[str, Any]]:
        """Extract annotation Actions"""
        actions = []
        
        try:
            for page_num, page in enumerate(reader.pages):
                annotations = page.get("/Annots", [])
                
                for annot in annotations:
                    if isinstance(annot, IndirectObject):
                        annot = annot.get_object()
                    
                    if not isinstance(annot, DictionaryObject):
                        continue
                    
                    # Check annotation Actions
                    for action_key in ["/A", "/AA"]:
                        if action_key in annot:
                            action_info = self._parse_action(annot[action_key], f"Annotation{action_key}")
                            if action_info:
                                action_info["page_number"] = page_num
                                action_info["annotation_type"] = str(annot.get("/Subtype", "Unknown"))
                                actions.append(action_info)
                
        except Exception as e:
            self.logger.error(f"Failed to extract annotation Actions: {e}")
        
        return actions
    
    def _extract_field_actions(self, reader: PdfReader) -> List[Dict[str, Any]]:
        """Extract field Actions"""
        actions = []
        
        try:
            # Check if there are forms
            catalog = reader.trailer.get("/Root")
            if not catalog:
                return actions
            
            if isinstance(catalog, IndirectObject):
                catalog = catalog.get_object()
            
            acro_form = catalog.get("/AcroForm")
            if not acro_form:
                return actions
            
            if isinstance(acro_form, IndirectObject):
                acro_form = acro_form.get_object()
            
            # Recursively extract field Actions
            def extract_from_fields(fields, parent_name=""):
                if not fields:
                    return
                
                for field in fields:
                    if isinstance(field, IndirectObject):
                        field = field.get_object()
                    
                    if not isinstance(field, DictionaryObject):
                        continue
                    
                    # Get field name
                    field_name = field.get("/T", "")
                    if isinstance(field_name, TextStringObject):
                        field_name = str(field_name)
                    
                    full_name = f"{parent_name}.{field_name}" if parent_name else field_name
                    
                    # Check field Actions
                    for action_key in ["/A", "/AA"]:
                        if action_key in field:
                            action_info = self._parse_action(field[action_key], f"Field{action_key}")
                            if action_info:
                                action_info["field_name"] = full_name
                                action_info["field_type"] = str(field.get("/FT", "Unknown"))
                                actions.append(action_info)
                    
                    # Recursively process child fields
                    kids = field.get("/Kids")
                    if kids:
                        extract_from_fields(kids, full_name)
            
            fields = acro_form.get("/Fields", [])
            extract_from_fields(fields)
            
        except Exception as e:
            self.logger.error(f"Failed to extract field Actions: {e}")
        
        return actions
    
    def _parse_action(self, action, context: str) -> Optional[Dict[str, Any]]:
        """Parse single Action"""
        try:
            if isinstance(action, IndirectObject):
                action = action.get_object()
            
            if not isinstance(action, DictionaryObject):
                return None
            
            action_info = {
                "context": context,
                "type": str(action.get("/S", "Unknown")),
                "raw_data": {}
            }
            
            # Safely extract Action data
            for key, value in action.items():
                try:
                    key_str = str(key)
                    if isinstance(value, (str, int, float, bool)):
                        action_info["raw_data"][key_str] = value
                    elif isinstance(value, (NameObject, TextStringObject)):
                        action_info["raw_data"][key_str] = str(value)
                    elif isinstance(value, ArrayObject):
                        action_info["raw_data"][key_str] = [str(item) for item in value]
                    else:
                        action_info["raw_data"][key_str] = type(value).__name__
                except:
                    action_info["raw_data"][key_str] = "UnparsableValue"
            
            # JavaScript detection
            if "/JS" in action:
                action_info["has_javascript"] = True
                js_code = action["/JS"]
                if isinstance(js_code, TextStringObject):
                    action_info["javascript_code"] = str(js_code)
                elif isinstance(js_code, IndirectObject):
                    try:
                        js_obj = js_code.get_object()
                        if hasattr(js_obj, 'get_data'):
                            action_info["javascript_code"] = js_obj.get_data().decode('utf-8', errors='ignore')
                    except:
                        action_info["javascript_code"] = "Could not extract JS code"
            
            return action_info
            
        except Exception as e:
            self.logger.error(f"Failed to parse Action ({context}): {e}")
            return None
    
    def _analyze_risk_indicators(self, actions: List[Dict[str, Any]]) -> List[str]:
        """Analyze risk indicators"""
        risk_indicators = []
        
        try:
            # Check JavaScript
            js_actions = [a for a in actions if a.get("has_javascript")]
            if js_actions:
                risk_indicators.append(f"Found {len(js_actions)} Actions containing JavaScript")
            
            # Check dangerous Action types
            dangerous_types = ["/Launch", "/ImportData", "/SubmitForm", "/GoToR"]
            for action_type in dangerous_types:
                type_actions = [a for a in actions if a.get("type") == action_type]
                if type_actions:
                    risk_indicators.append(f"Found {len(type_actions)} Actions of type {action_type}")
            
            # Check Actions executed on document open
            open_actions = [a for a in actions if "Open" in a.get("context", "")]
            if open_actions:
                risk_indicators.append(f"Found {len(open_actions)} Actions executed on document open")
            
        except Exception as e:
            self.logger.error(f"Failed to analyze risk indicators: {e}")
        
        return risk_indicators


# Global Action extractor instance
action_extractor = ActionExtractor()
