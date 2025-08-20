#!/usr/bin/env python3
"""
Unified Error Handling Module
"""

import json
import logging
from typing import Dict, Any, Optional
from enum import Enum


class PDFErrorType(Enum):
    """PDF error type enumeration"""
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    INVALID_PDF_FORMAT = "INVALID_PDF_FORMAT"
    ENCRYPTION_PASSWORD_REQUIRED = "ENCRYPTION_PASSWORD_REQUIRED"
    ENCRYPTION_INVALID_PASSWORD = "ENCRYPTION_INVALID_PASSWORD"
    CORRUPTED_DOCUMENT = "CORRUPTED_DOCUMENT"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    PROCESSING_ERROR = "PROCESSING_ERROR"


class PDFProcessingError(Exception):
    """PDF processing exception base class"""
    
    def __init__(
        self, 
        error_type: PDFErrorType, 
        message: str, 
        file_path: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        self.error_type = error_type
        self.message = message
        self.file_path = file_path
        self.original_error = original_error
        super().__init__(message)


class ErrorHandler:
    """Unified error handler"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_error_response(
        self, 
        error_type: PDFErrorType, 
        message: str, 
        file_path: Optional[str] = None
    ) -> str:
        """Create standardized error response"""
        error_response = {
            "success": False,
            "error_type": error_type.value,
            "error_message": message,
        }
        
        if file_path:
            error_response["file_path"] = file_path
        
        return json.dumps(error_response, ensure_ascii=False, indent=2)
    
    def handle_file_error(self, file_path: str, original_error: Exception) -> str:
        """Handle file-related errors"""
        if isinstance(original_error, FileNotFoundError):
            return self.create_error_response(
                PDFErrorType.FILE_NOT_FOUND,
                f"File does not exist: {file_path}",
                file_path
            )
        elif isinstance(original_error, PermissionError):
            return self.create_error_response(
                PDFErrorType.PERMISSION_DENIED,
                f"Insufficient file permissions: {file_path}",
                file_path
            )
        else:
            return self.create_error_response(
                PDFErrorType.PROCESSING_ERROR,
                f"File processing error: {str(original_error)}",
                file_path
            )
    
    def handle_pdf_error(self, file_path: str, original_error: Exception) -> str:
        """Handle PDF-related errors"""
        error_msg = str(original_error).lower()
        
        if "password" in error_msg or "decrypt" in error_msg:
            if "wrong password" in error_msg or "invalid password" in error_msg:
                return self.create_error_response(
                    PDFErrorType.ENCRYPTION_INVALID_PASSWORD,
                    "Provided password is incorrect",
                    file_path
                )
            else:
                return self.create_error_response(
                    PDFErrorType.ENCRYPTION_PASSWORD_REQUIRED,
                    "PDF document is encrypted, correct password required",
                    file_path
                )
        elif "invalid pdf" in error_msg or "not a pdf" in error_msg:
            return self.create_error_response(
                PDFErrorType.INVALID_PDF_FORMAT,
                "File format is not a valid PDF",
                file_path
            )
        elif "corrupted" in error_msg or "damaged" in error_msg:
            return self.create_error_response(
                PDFErrorType.CORRUPTED_DOCUMENT,
                "PDF document is corrupted or has structural anomalies",
                file_path
            )
        else:
            return self.create_error_response(
                PDFErrorType.PROCESSING_ERROR,
                f"PDF processing error: {str(original_error)}",
                file_path
            )
    
    def raise_pdf_error(
        self, 
        error_type: PDFErrorType, 
        message: str, 
        file_path: Optional[str] = None,
        original_error: Optional[Exception] = None
    ):
        """Raise PDF processing exception"""
        self.logger.error(f"{error_type.value}: {message} (File: {file_path})")
        raise PDFProcessingError(error_type, message, file_path, original_error)


# Global error handler instance
error_handler = ErrorHandler()
