# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-08-21

### Added
- Initial release of PDF Action Inspector
- MCP server implementation with FastMCP 2.0
- Core PDF Actions extraction functionality
- Security analysis framework with policy-based prompts
- Comprehensive error handling with structured error types
- Memory-efficient caching system with automatic cleanup
- Support for encrypted PDF documents
- Multi-level Actions extraction (document, page, annotation, field)
- Form field analysis and search capabilities
- PDF structure analysis and metadata extraction
- Annotation processing with Widget annotation support
- English documentation and comments throughout codebase
- Example scripts for basic analysis and security assessment
- MIT license for open source distribution

### Features
- **PDF Actions Extraction**: Extract Actions from all levels of PDF documents
- **Security Analysis**: Generate structured analysis prompts for AI-powered security assessment
- **Cache Management**: Automatic cache management with configurable timeout (default 120 seconds)
- **Error Handling**: Comprehensive error handling for various PDF processing scenarios
- **MCP Integration**: Full Model Context Protocol server implementation
- **Encryption Support**: Handle encrypted PDFs with password attempts
- **Multi-format Support**: Support for various PDF versions and formats

### Technical Details
- **Framework**: FastMCP 2.0 for MCP server implementation
- **PDF Processing**: PyPDF2 for PDF parsing and manipulation
- **Architecture**: Modular design with separation of concerns
- **Caching**: Single-layer caching with background cleanup thread
- **Configuration**: Environment variable-based configuration system
- **Logging**: Comprehensive logging with configurable levels

### Documentation
- English README with comprehensive API documentation
- Code examples for common use cases
- Security considerations and best practices
- Installation and configuration instructions
- Contributing guidelines for open source development

### Dependencies
- PyPDF2 >= 3.0.0
- FastMCP >= 2.0.0
- Python >= 3.8

## [Unreleased]

### Planned
- Additional output formats (XML, CSV)
- Enhanced JavaScript analysis capabilities
- Support for more PDF specification features
- Performance optimizations for large files
- Additional example scripts and use cases
- Integration tests and automated testing framework
