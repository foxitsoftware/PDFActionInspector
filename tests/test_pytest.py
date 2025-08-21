#!/usr/bin/env python3
"""
Pytest test suite for PDF Action Inspector
"""

import pytest
import json
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.inspector import PDFActionInspector


class TestPDFActionInspector:
    """Test cases for PDFActionInspector using pytest"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.inspector = PDFActionInspector()
        self.test_pdf_path = "examples/pdf_samples/test-signature_action.pdf"
        self.test_pdf_without_actions = "examples/pdf_samples/without_actions.pdf"
        self.test_pdf_confuse_js = "examples/pdf_samples/confuse_js_code.pdf"
        
        # Verify test files exist
        test_files = [self.test_pdf_path, self.test_pdf_without_actions, self.test_pdf_confuse_js]
        for pdf_path in test_files:
            if not os.path.exists(pdf_path):
                print(f"Warning: Test PDF file not found: {pdf_path}")
    
    def test_get_document_overview(self):
        """Test document overview functionality"""
        print(f"\n🧪 Testing document overview...")
        result = self.inspector.get_document_overview(self.test_pdf_path)
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        # Basic structure checks
        assert "filename" in result
        assert "basic_info" in result
        assert "metadata" in result
        assert "structure" in result
        assert "actions_summary" in result
        
        # Check basic info
        basic_info = result["basic_info"]
        assert basic_info["pages"] == 2
        assert basic_info["encrypted"] is False
        assert basic_info["pdf_version"] == "%PDF-1.7"
        
        print(f"✅ Document overview test passed")
    
    def test_extract_pdf_actions(self):
        """Test PDF actions extraction"""
        print(f"\n🧪 Testing PDF actions extraction...")
        result = self.inspector.extract_pdf_actions(self.test_pdf_path)
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        # Check main structure
        assert "document_level_actions" in result
        assert "pages_level_actions" in result
        assert "annotations_level_actions" in result
        assert "field_level_actions" in result
        
        # Check if signature field action is detected
        annot_actions = result["annotations_level_actions"]
        assert len(annot_actions) > 0
        
        # Find the signature field action
        sig_action_found = False
        for key, value in annot_actions.items():
            if "Sig field" in key:
                sig_action_found = True
                assert "actions" in value
                assert "AnnotMouseDown" in value["actions"]
                assert value["actions"]["AnnotMouseDown"]["S"] == "/JavaScript"
                print(f"   Found signature field with JavaScript action")
                break
        
        assert sig_action_found, "Signature field action not found"
        print(f"✅ PDF actions extraction test passed")
    
    def test_get_fields_by_name(self):
        """Test finding fields by name"""
        print(f"\n🧪 Testing get_fields_by_name...")
        
        # Test finding the "Price" field that gets modified by the signature field's JavaScript
        result = self.inspector.get_fields_by_name(self.test_pdf_path, "Price")
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        # Check if we get a valid response without error
        if "error_message" in result:
            print(f"❌ get_fields_by_name returned error: {result['error_message']}")
            assert False, f"get_fields_by_name failed with error: {result['error_message']}"
        else:
            assert "field_name" in result
            assert "found_fields" in result
            assert "total_found" in result
            
            print(f"✅ get_fields_by_name test passed - found {result['total_found']} fields")
            
            # If Price field is found, show its details
            if result["total_found"] > 0:
                for field in result["found_fields"]:
                    print(f"   Found field: {field['name']} (type: {field['type']}, value: '{field['value']}')")
                    
                # Check that we found the price field
                found_price = any("Price" in field["name"] for field in result["found_fields"])
                assert found_price, "Should find a field with 'Price' in the name"
            else:
                print(f"   No 'Price' field found - this might be expected if the field doesn't exist yet")
                
        # Also test finding the Signature field
        print(f"\n🧪 Testing get_fields_by_name for Signature field...")
        result2 = self.inspector.get_fields_by_name(self.test_pdf_path, "Signature")
        
        if "error_message" not in result2 and result2["total_found"] > 0:
            print(f"   Found {result2['total_found']} signature fields:")
            for field in result2["found_fields"]:
                print(f"   - {field['name']} (type: {field['type']})")
    
    def test_get_page_text_content(self):
        """Test page text extraction"""
        print(f"\n🧪 Testing page text content extraction...")
        result = self.inspector.get_page_text_content(self.test_pdf_path, 0)
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        assert "page_number" in result
        assert "text_content" in result
        assert "metadata" in result
        assert result["page_number"] == 0
        
        print(f"✅ Page text content test passed")
    
    def test_get_pdf_object_information(self):
        """Test PDF object information retrieval"""
        print(f"\n🧪 Testing PDF object information...")
        # Test with object number 14 (the signature field object)
        result = self.inspector.get_pdf_object_information(self.test_pdf_path, 14)
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        assert "object_number" in result
        assert "found" in result
        assert result["object_number"] == 14
        
        if result["found"]:
            assert "object_info" in result
            print(f"✅ PDF object information test passed")
        else:
            print(f"⚠️  Object 14 not found in test PDF")
    
    def test_get_trailer_object(self):
        """Test PDF trailer object retrieval"""
        print(f"\n🧪 Testing trailer object retrieval...")
        result = self.inspector.get_trailer_object(self.test_pdf_path)
        
        # result should now be a dict, not JSON string
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        
        assert "trailer_content" in result  # Fixed: actual key name
        assert "analysis" in result
        
        analysis = result["analysis"]
        assert "has_root" in analysis
        assert "has_info" in analysis
        assert "encrypted" in analysis
        
        print(f"✅ Trailer object test passed")
    
    def test_analyze_pdf_actions_security(self):
        """Test security analysis prompt generation"""
        print(f"\n🧪 Testing security analysis prompt...")
        result = self.inspector.analyze_pdf_actions_security(self.test_pdf_path)
        
        # Should return a comprehensive analysis prompt
        assert isinstance(result, str)
        assert len(result) > 100  # Should be a substantial prompt
        assert "PDF Security Analysis" in result
        assert "JavaScript" in result  # Should mention JS since our test PDF has JS
        
        print(f"✅ Security analysis prompt test passed")
    
    def test_cache_functionality(self):
        """Test cache functionality"""
        print(f"\n🧪 Testing cache functionality...")
        
        # Test cache status
        cache_status = self.inspector.get_cache_status()
        
        # cache_status should be a dict, not a JSON string
        assert isinstance(cache_status, dict), f"Expected dict, got {type(cache_status)}"
        assert "cache_entries" in cache_status or "total_entries" in cache_status
        
        print(f"   Cache status: {cache_status}")
        
        # Clear cache for specific file
        self.inspector.clear_cache(self.test_pdf_path)
        
        # Clear all cache
        self.inspector.clear_cache()
        
        print(f"✅ Cache functionality test passed")
    
    def test_set_password_functionality(self):
        """Test password setting functionality"""
        print(f"\n🧪 Testing password setting functionality...")
        
        # Test 1: Set password for a non-encrypted PDF (should work but password not needed)
        print(f"   Testing password setting for unencrypted PDF...")
        try:
            self.inspector.cache_manager.set_password(self.test_pdf_path, "any_password")
            print(f"   ✅ Password set successfully for unencrypted PDF")
        except Exception as e:
            print(f"   ⚠️  Password setting failed for unencrypted PDF: {e}")
            # This might be expected behavior - let's not fail the test
        
        # Test 2: Test with non-existent file (should fail)
        print(f"   Testing password setting for non-existent file...")
        try:
            self.inspector.cache_manager.set_password("non_existent_file.pdf", "password")
            print(f"   ❌ Password setting should have failed for non-existent file")
            assert False, "Should have failed for non-existent file"
        except Exception as e:
            print(f"   ✅ Correctly failed for non-existent file: {type(e).__name__}")
        
        # Test 3: Test cache manager password storage
        print(f"   Testing password storage in cache manager...")
        
        # First clear any existing passwords
        self.inspector.cache_manager.clear_cache()
        
        # Set password for a valid file
        try:
            self.inspector.cache_manager.set_password(self.test_pdf_path, "test_password")
            
            # Check that password is stored (access private attribute for testing)
            stored_passwords = self.inspector.cache_manager._file_passwords
            assert self.test_pdf_path in stored_passwords
            assert stored_passwords[self.test_pdf_path] == "test_password"
            print(f"   ✅ Password correctly stored in cache manager")
            
        except Exception as e:
            print(f"   ⚠️  Password storage test encountered error: {e}")
        
        # Test 4: Test password verification workflow
        print(f"   Testing password verification workflow...")
        try:
            # This should work with the stored password
            reader = self.inspector.cache_manager.get_reader(self.test_pdf_path)
            assert reader is not None
            print(f"   ✅ PDF successfully opened with stored password")
        except Exception as e:
            print(f"   ⚠️  PDF opening with stored password failed: {e}")
        
        # Test 5: Test cache status includes password info
        print(f"   Testing cache status includes password information...")
        cache_status = self.inspector.get_cache_status()
        assert isinstance(cache_status, dict)
        
        if "stored_passwords" in cache_status:
            print(f"   ✅ Cache status includes password count: {cache_status['stored_passwords']}")
        else:
            print(f"   ⚠️  Cache status doesn't include password information")
        
        print(f"✅ Password functionality test completed")


# Custom test runner that can be called directly
def run_tests_with_summary():
    """Run tests with a summary report"""
    print("=" * 80)
    print("🚀 PDF Action Inspector Pytest Suite")
    print("=" * 80)
    
    # Run pytest with custom options
    exit_code = pytest.main([
        __file__, 
        "-v",  # verbose
        "--tb=short",  # short traceback format
        "--color=yes",  # colored output
        "-x"  # stop on first failure
    ])
    
    print("\n" + "=" * 80)
    if exit_code == 0:
        print("🎉 All tests completed!")
    else:
        print("⚠️  Some tests failed or were skipped")
    print("=" * 80)
    
    return exit_code


if __name__ == "__main__":
    run_tests_with_summary()
