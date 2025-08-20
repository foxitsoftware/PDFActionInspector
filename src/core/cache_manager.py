#!/usr/bin/env python3
"""
Cache Management Module
"""

import time
import threading
import logging
from typing import Dict, Any, Optional
from io import BytesIO

from PyPDF2 import PdfReader

from ..config.settings import settings
from ..core.error_handler import ErrorHandler, PDFErrorType


class CacheEntry:
    """Cache Entry"""
    
    def __init__(self, reader: PdfReader, file_path: str):
        self.reader = reader
        self.file_path = file_path
        self.created_at = time.time()
        self.last_accessed = time.time()
        self.access_count = 0
    
    def touch(self):
        """Update last access time"""
        self.last_accessed = time.time()
        self.access_count += 1
    
    def is_expired(self, timeout_seconds: int) -> bool:
        """Check if expired"""
        return (time.time() - self.last_accessed) > timeout_seconds


class CacheManager:
    """PDF Reader Cache Manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
        
        # Cache storage
        self._cache: Dict[str, CacheEntry] = {}
        self._file_passwords: Dict[str, str] = {}
        
        # Thread lock
        self._lock = threading.RLock()
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def _start_cleanup_thread(self):
        """Start cache cleanup thread"""
        def cleanup_loop():
            while True:
                try:
                    time.sleep(30)  # Check every 30 seconds
                    self._cleanup_expired_entries()
                except Exception as e:
                    self.logger.error(f"Cache cleanup thread error: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
        self.logger.info("Cache cleanup thread started")
    
    def _cleanup_expired_entries(self):
        """Clean up expired Cache Entries"""
        timeout_seconds = settings.get_cache_timeout_seconds()
        
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired(timeout_seconds)
            ]
            
            for key in expired_keys:
                self.logger.info(f"Cleaning expired cache: {key}")
                del self._cache[key]
    
    def _generate_cache_key(self, file_path: str, password: Optional[str] = None) -> str:
        """Generate cache key"""
        return f"{file_path}:{password or ''}"
    
    def _load_pdf_reader(self, file_path: str, password: Optional[str] = None) -> PdfReader:
        """Load PDF Reader"""
        try:
            # Check file size
            import os
            file_size = os.path.getsize(file_path)
            max_size = settings.get_max_file_size_bytes()
            
            if file_size > max_size:
                self.error_handler.raise_pdf_error(
                    PDFErrorType.FILE_TOO_LARGE,
                    f"File size exceeds limit ({file_size / 1024 / 1024:.1f}MB > {settings.max_file_size_mb}MB)",
                    file_path
                )
            
            # Read file into memory
            with open(file_path, "rb") as file:
                file_content = file.read()
            
            # Create PDF Reader
            reader = PdfReader(BytesIO(file_content))
            
            # Handle encrypted documents
            if reader.is_encrypted:
                self._handle_encryption(reader, file_path, password)
            
            return reader
            
        except FileNotFoundError as e:
            self.error_handler.raise_pdf_error(
                PDFErrorType.FILE_NOT_FOUND,
                f"File does not exist: {file_path}",
                file_path,
                e
            )
        except PermissionError as e:
            self.error_handler.raise_pdf_error(
                PDFErrorType.PERMISSION_DENIED,
                f"Insufficient file permissions: {file_path}",
                file_path,
                e
            )
        except Exception as e:
            if "password" in str(e).lower() or "decrypt" in str(e).lower():
                self.error_handler.raise_pdf_error(
                    PDFErrorType.ENCRYPTION_PASSWORD_REQUIRED,
                    "PDF document is encrypted, correct password required",
                    file_path,
                    e
                )
            else:
                self.error_handler.raise_pdf_error(
                    PDFErrorType.INVALID_PDF_FORMAT,
                    f"PDF format error: {str(e)}",
                    file_path,
                    e
                )
    
    def _handle_encryption(self, reader: PdfReader, file_path: str, password: Optional[str] = None):
        """Handle encrypted PDF document"""
        # Try using provided password
        if password:
            if reader.decrypt(password):
                self.logger.info("Successfully decrypted with provided password")
                return
            else:
                self.error_handler.raise_pdf_error(
                    PDFErrorType.ENCRYPTION_INVALID_PASSWORD,
                    "Provided password is incorrect",
                    file_path
                )
        
        # Try using preset password
        stored_password = self._file_passwords.get(file_path)
        if stored_password and reader.decrypt(stored_password):
            self.logger.info("Successfully decrypted with preset password")
            return
        
        # Try common passwords
        for common_pwd in settings.common_passwords:
            if reader.decrypt(common_pwd):
                self.logger.info(f"Successfully decrypted with common password: {common_pwd}")
                self._file_passwords[file_path] = common_pwd
                return
        
        # All attempts failed
        self.error_handler.raise_pdf_error(
            PDFErrorType.ENCRYPTION_PASSWORD_REQUIRED,
            "Cannot decrypt PDF document, please provide correct password",
            file_path
        )
    
    def get_reader(self, file_path: str, password: Optional[str] = None) -> PdfReader:
        """Get PDF Reader (with cache)"""
        cache_key = self._generate_cache_key(file_path, password)
        
        with self._lock:
            # Check cache
            if cache_key in self._cache:
                entry = self._cache[cache_key]
                entry.touch()
                self.logger.debug(f"Cache hit: {file_path}")
                return entry.reader
            
            # Load new Reader
            self.logger.info(f"Loading new PDF: {file_path}")
            reader = self._load_pdf_reader(file_path, password)
            
            # Cache Reader
            self._cache[cache_key] = CacheEntry(reader, file_path)
            
            return reader
    
    def set_password(self, file_path: str, password: str):
        """Set password for file"""
        with self._lock:
            self._file_passwords[file_path] = password
            self.logger.info(f"File password set: {file_path}")
    
    def clear_cache(self, file_path: Optional[str] = None):
        """Clear cache"""
        with self._lock:
            if file_path:
                # Clear specific file cache
                keys_to_remove = [key for key in self._cache.keys() if key.startswith(file_path + ":")]
                for key in keys_to_remove:
                    del self._cache[key]
                self.logger.info(f"File cache cleared: {file_path}")
            else:
                # Clear all cache
                self._cache.clear()
                self._file_passwords.clear()
                self.logger.info("All cache cleared")
    
    def get_cache_status(self) -> Dict[str, Any]:
        """Get cache status"""
        with self._lock:
            return {
                "total_entries": len(self._cache),
                "cache_entries": [
                    {
                        "file_path": entry.file_path,
                        "created_at": entry.created_at,
                        "last_accessed": entry.last_accessed,
                        "access_count": entry.access_count
                    }
                    for entry in self._cache.values()
                ],
                "stored_passwords": len(self._file_passwords)
            }


# Global cache manager instance
cache_manager = CacheManager()
