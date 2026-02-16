"""PDF exporter for business plan documents."""

from io import BytesIO
from typing import Optional

import markdown as md


class PDFExporter:
    """Export business plan to PDF format.
    
    Converts Markdown to HTML, then to PDF with styled formatting.
    Falls back to HTML download if PDF generation is not available.
    """

    # CSS Styling
    CSS_STYLE = """
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    
    @page {
        size: A4;
        margin: 20mm;
        @bottom-center {
            content: "- " counter(page) " -";
            font-family: 'Noto Sans JP', sans-serif;
            font-size: 10pt;
        }
    }
    
    body {
        font-family: 'Noto Sans JP', sans-serif;
        font-size: 11pt;
        line-height: 1.8;
        color: #333;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: bold;
        margin-top: 24pt;
        margin-bottom: 12pt;
        page-break-after: avoid;
        color: #1a3a52;
    }
    
    h2 {
        font-size: 18pt;
        font-weight: bold;
        margin-top: 18pt;
        margin-bottom: 10pt;
        page-break-after: avoid;
        color: #2c5282;
        border-left: 4pt solid #2c5282;
        padding-left: 10pt;
    }
    
    h3 {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 12pt;
        margin-bottom: 8pt;
        page-break-after: avoid;
        color: #2d3748;
    }
    
    p {
        margin: 8pt 0;
    }
    
    ul, ol {
        margin: 8pt 0;
        padding-left: 20pt;
    }
    
    li {
        margin: 4pt 0;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 12pt 0;
        page-break-inside: avoid;
    }
    
    thead {
        background-color: #2c5282;
        color: white;
    }
    
    th, td {
        border: 1pt solid #ccc;
        padding: 8pt;
        text-align: left;
    }
    
    th {
        font-weight: bold;
        background-color: #2c5282;
        color: white;
    }
    
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    td {
        padding: 8pt;
    }
    
    code {
        background-color: #f0f0f0;
        padding: 2pt 4pt;
        font-family: 'Courier New', monospace;
        font-size: 10pt;
    }
    
    pre {
        background-color: #f5f5f5;
        padding: 12pt;
        border-left: 3pt solid #2c5282;
        overflow-x: auto;
        margin: 12pt 0;
    }
    
    blockquote {
        border-left: 4pt solid #ccc;
        padding-left: 12pt;
        margin: 12pt 0;
        color: #666;
    }
    """

    def __init__(self) -> None:
        """Initialize PDFExporter."""
        self._weasyprint_available = self._check_weasyprint()

    def _check_weasyprint(self) -> bool:
        """Check if weasyprint is available.
        
        Returns:
            True if weasyprint can be imported, False otherwise
        """
        try:
            import weasyprint  # noqa: F401
            return True
        except Exception:
            # weasyprint may fail on import due to missing system libraries
            return False

    def export(self, result: dict, filename_prefix: str = "business_plan") -> str:
        """Export business plan to PDF or HTML.
        
        If weasyprint is not available, exports as HTML instead.
        
        Args:
            result: Result dictionary from AgentOrchestrator.run_all()
                   Contains 'business_plan' key
            filename_prefix: Prefix for output filename (without extension)
            
        Returns:
            Path to created PDF or HTML file
        """
        business_plan = result.get("business_plan", "")
        
        # Convert Markdown to HTML
        md_extensions = ['tables', 'toc', 'fenced_code']
        html_content = md.markdown(business_plan, extensions=md_extensions)
        
        # Create complete HTML document
        html_document = self._create_html_document(html_content)
        
        # Try to export as PDF, fall back to HTML
        if self._weasyprint_available:
            return self._export_pdf(html_document, filename_prefix)
        else:
            return self._export_html(html_document, filename_prefix)

    def _create_html_document(self, html_content: str) -> str:
        """Create complete HTML document with CSS.
        
        Args:
            html_content: HTML content converted from Markdown
            
        Returns:
            Complete HTML document as string
        """
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>事業計画書</title>
    <style>
        {self.CSS_STYLE}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

    def _export_pdf(self, html_document: str, filename_prefix: str) -> str:
        """Export HTML document to PDF using weasyprint.
        
        Args:
            html_document: Complete HTML document
            filename_prefix: Prefix for output filename
            
        Returns:
            Path to PDF file
        """
        try:
            from weasyprint import HTML as WeasyprintHTML
            
            filename = f"{filename_prefix}.pdf"
            # Create PDF from HTML string
            WeasyprintHTML(string=html_document).write_pdf(filename)
            return filename
        except Exception as e:
            # If PDF generation fails, fall back to HTML
            print(f"⚠️ PDF生成失敗（{type(e).__name__}）。HTMLで出力します。")
            return self._export_html(html_document, filename_prefix)

    def _export_html(self, html_document: str, filename_prefix: str) -> str:
        """Export as HTML document (fallback).
        
        Args:
            html_document: Complete HTML document
            filename_prefix: Prefix for output filename
            
        Returns:
            Path to HTML file
        """
        filename = f"{filename_prefix}.html"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_document)
        return filename

    def get_export_format(self) -> str:
        """Get the export format that will be used.
        
        Returns:
            "PDF" if weasyprint is available, "HTML" otherwise
        """
        return "PDF" if self._weasyprint_available else "HTML"
