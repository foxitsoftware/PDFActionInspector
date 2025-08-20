#!/usr/bin/env python3
"""
Configuration Management Module
Handle environment variables and system configuration
"""

import os
import logging
from typing import Optional


class Settings:
    """System Configuration Manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._load_settings()
    
    def _load_settings(self):
        """Load configuration settings"""
        # Cache configuration
        self.cache_timeout = int(os.getenv('PDF_CACHE_TIMEOUT_SECONDS', '120'))
        
        # Log configuration
        self.log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        # Password attempt configuration
        self.common_passwords = [
            "", "password", "123456", "admin", "user", "123", "000000"
        ]
        
        # File size limit (MB)
        self.max_file_size_mb = int(os.getenv('MAX_PDF_FILE_SIZE_MB', '100'))
        
        self.logger.info(f"Configuration loaded - cache timeout: {self.cache_timeout} seconds")
    
    def get_cache_timeout_seconds(self) -> int:
        """Get cache timeout (seconds)"""
        return self.cache_timeout
    
    def get_max_file_size_bytes(self) -> int:
        """Get maximum file size (bytes)"""
        return self.max_file_size_mb * 1024 * 1024
    
    def setup_logging(self):
        """Setup log configuration"""
        logging.basicConfig(
            level=getattr(logging, self.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )


# Global configuration instance
settings = Settings()
