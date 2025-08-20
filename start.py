#!/usr/bin/env python3
"""
PDF Action Inspector Start Script
"""

import sys
import os
from pathlib import Path

# Add project root directory to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_functionality():
    """Test basic functionality"""
    try:
        from src.core.inspector import PDFActionInspector
        from src.core.cache_manager import CacheManager
        from src.core.error_handler import ErrorHandler
        
        print("Initializing components...")
        cache_manager = CacheManager()
        error_handler = ErrorHandler()
        inspector = PDFActionInspector(cache_manager, error_handler)
        
        print("Components initialized successfully!")
        
        # Test sample PDF
        sample_pdf = "sample.pdf"
        if os.path.exists(sample_pdf):
            print(f"Analyzing sample PDF: {sample_pdf}")
            overview = inspector.get_document_overview(sample_pdf)
            print("Document overview retrieved successfully")
            print(overview[:200] + "..." if len(overview) > 200 else overview)
        else:
            print(f"Sample PDF file {sample_pdf} does not exist")
            
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def start_mcp_server():
    """Start MCP server"""
    try:
        import subprocess
        print("Starting MCP server...")
        subprocess.run([sys.executable, "mcp_server.py"])
    except KeyboardInterrupt:
        print("\nServer stopped")
    except Exception as e:
        print(f"Failed to start server: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("=== PDF Action Inspector Functionality Test ===")
        success = test_basic_functionality()
        sys.exit(0 if success else 1)
    elif len(sys.argv) > 1 and sys.argv[1] == "server":
        start_mcp_server()
    else:
        print("Usage:")
        print("  python start.py test    - Run functionality test")
        print("  python start.py server  - Start MCP server")
        print("  python start.py         - Show this help message")
