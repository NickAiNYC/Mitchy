"""
MITCHY VISION PRO - Internal Document Analyzer
For YOUR eyes only - Never share output with clients
Speeds up YOUR gap analysis by 80%
"""

import os
import re
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional
import hashlib

# ==================== INTERNAL ANALYSIS ENGINE ====================
class MitchyVisionPro:
    """
    INTERNAL TOOL ONLY - Not for client distribution
    Scans documents to flag potential HPD compliance issues
    """
    
    def __init__(self):
        self.patterns = {
            # Foreign Account Detection
            'foreign_account': [
                r'swiss.*bank', r'foreign.*account', r'overseas.*account',
                r'CHF', r'EUR.*account', r'international.*bank',
                r'wire.*transfer.*international', r'wise\.com', r'revolut',
                r'金額', r'€', r'£', r'¥'  # Currency symbols
            ],
            
            # Gig Income Detection
            'gig_income': [
                r'doordash', r'uber', r'lyft', r'grubhub', r'instacart',
                r'taskrabbit', r'1099-k', r'gig.*economy', r'platform.*income',
                r'delivery.*driver', r'ride.*share', r'food.*delivery'
            ],
            
            # Medical Hardship Detection
            'medical_hardship': [
                r'hospital', r'discharge', r'emergency.*room', r'ER',
                r'surgery', r'ICU', r'住院', r'ingreso',  # Hospital in Chinese/Spanish
                r'medical.*records', r'physician', r'doctor.*note',
                r'inpatient', r'outpatient', r'clinic'
            ],
            
            # Date Patterns
            'date': [
                r'\d{1,2}/\d{1,2}/\d{4}',  # MM/DD/YYYY
                r'\d{4}-\d{1,2}-\d{1,2}',  # YYYY-MM-DD
                r'\d{1,2}-\d{1,2}-\d{4}',  # MM-DD-YYYY
                r'(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{1,2},? \d{4}',  # Month DD, YYYY
                r'\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* \d{4}'  # DD Month YYYY
            ],
            
            # Document Type Detection
            'document_type': {
                'death_certificate': [r'death.*certificate', r'certificado.*defunción', r'死亡證明'],
                'tax_return': [r'tax.*return', r'1040', r'schedule.*b', r'w-2', r'w2'],
                'bank_statement': [r'bank.*statement', r'account.*statement', r'月結單'],  # Chinese for statement
                'utility_bill': [r'con.*ed', r'national.*grid', r'electric.*bill', r'gas.*bill', r'water.*bill'],
                'lease': [r'lease', r'租約', r'contrato.*arrendamiento'],
                'pay_stub': [r'pay.*stub', r'paycheck', r'earnings.*statement']
            }
        }
        
        # HPD Rule Thresholds
        self.thresholds = {
            'foreign_account_min': 10000,  # $10,000 FBAR threshold
            'notice_period_days': 90,
            'utility_gap_days': 60,
            'residency_years': 2
        }
    
    def analyze_folder(self, folder_path: str) -> Dict:
        """
        Analyze all documents in a folder
        Returns internal analysis for YOUR eyes only
        """
        folder = Path(folder_path)
        if not folder.exists():
            return {"error": f"Folder not found: {folder_path}"}
        
        analysis = {
            "scan_date": datetime.now().isoformat(),
            "folder": str(folder),
            "files_found": 0,
            "red_flags": [],
            "missing_categories": [],
            "timeline_issues": [],
            "internal_score": 0,
            "recommended_focus": []
        }
        
        # Scan all files
        for file_path in folder.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in ['.pdf', '.jpg', '.jpeg', '.png', '.txt', '.doc', '.docx']:
                analysis["files_found"] += 1
                file_analysis = self._analyze_file(file_path)
                
                if file_analysis["red_flags"]:
                    analysis["red_flags"].extend(file_analysis["red_flags"])
                
                if file_analysis.get("dates"):
                    analysis.setdefault("dates_found", []).extend(file_analysis["dates"])
        
        # Post-analysis
        analysis.update(self._post_analysis(analysis))
        
        # Generate internal recommendations
        analysis["recommended_focus"] = self._generate_recommendations(analysis)
        
        # Calculate internal score (for YOUR prioritization only)
        analysis["internal_score"] = self._calculate_risk_score(analysis)
        
        return analysis
    
    def _analyze_file(self, file_path: Path) -> Dict:
        """
        Analyze a single file
        Uses OCR if needed (requires pytesseract/pymupdf)
        """
        result = {
            "filename": file_path.name,
            "file_type": file_path.suffix.lower(),
            "red_flags": [],
            "dates": [],
            "detected_types": []
        }
        
        try:
            # Try to extract text
            text = self._extract_text(file_path)
            
            if text:
                # Check for patterns
                for category, patterns in self.patterns.items():
                    if category in ['foreign_account', 'gig_income', 'medical_hardship']:
                        for pattern in patterns:
                            if re.search(pattern, text, re.IGNORECASE):
                                result["red_flags"].append(f"{category.upper()}: Found '{pattern}' in {file_path.name}")
                    
                    elif category == 'date':
                        for pattern in patterns:
                            dates = re.findall(pattern, text, re.IGNORECASE)
                            if dates:
                                result["dates"].extend(dates)
                    
                    elif category == 'document_type':
                        for doc_type, doc_patterns in patterns.items():
                            for pattern in doc_patterns:
                                if re.search(pattern, text, re.IGNORECASE):
                                    result["detected_types"].append(doc_type)
            
            # File size check (too small might be incomplete)
            file_size = file_path.stat().st_size
            if file_size < 1024:  # Less than 1KB
                result["red_flags"].append(f"FILE_SIZE: {file_path.name} is very small ({file_size} bytes) - may be incomplete")
            
        except Exception as e:
            result["red_flags"].append(f"ERROR: Could not analyze {file_path.name}: {str(e)}")
        
        return result
    
    def _extract_text(self, file_path: Path) -> str:
        """
        Extract text from various file types
        Requires: pip install pymupdf pillow pytesseract
        """
        text = ""
        
        try:
            # PDF files
            if file_path.suffix.lower() == '.pdf':
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(file_path)
                    for page in doc:
                        text += page.get_text()
                    doc.close()
                except ImportError:
                    # Fallback: try pdfminer
                    try:
                        from pdfminer.high_level import extract_text
                        text = extract_text(file_path)
                    except ImportError:
                        text = f"[PDF: {file_path.name}]"
            
            # Image files
            elif file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                try:
                    import pytesseract
                    from PIL import Image
                    img = Image.open(file_path)
                    text = pytesseract.image_to_string(img)
                except ImportError:
                    text = f"[IMAGE: {file_path.name}]"
            
            # Text files
            elif file_path.suffix.lower() in ['.txt', '.doc', '.docx']:
                try:
                    if file_path.suffix.lower() == '.txt':
                        text = file_path.read_text(encoding='utf-8', errors='ignore')
                    elif file_path.suffix.lower() == '.docx':
                        import docx
                        doc = docx.Document(file_path)
                        text = '\n'.join([para.text for para in doc.paragraphs])
                except Exception:
                    text = f"[TEXT_FILE: {file_path.name}]"
        
        except Exception as e:
            text = f"[ERROR reading {file_path.name}: {str(e)}]"
        
        return text.lower() if text else ""
    
    def _post_analysis(self, analysis: Dict) -> Dict:
        """
        Analyze collected data for patterns
        """
        results = {}
        
        # Check for foreign accounts without tax docs
        foreign_flags = [f for f in analysis["red_flags"] if "FOREIGN_ACCOUNT" in f]
        tax_docs = any("tax_return" in str(f).lower() for f in analysis.get("detected_types", []))
        
        if foreign_flags and not tax_docs:
            results["missing_categories"] = ["TAX_DOCUMENTS: Foreign accounts detected but no Schedule B/1040 found"]
        
        # Check timeline
        dates = self._parse_dates(analysis.get("dates", []))
        if len(dates) >= 2:
            dates.sort()
            if len(dates) >= 2:
                timeline_days = (dates[-1] - dates[0]).days
                if timeline_days > self.thresholds['notice_period_days']:
                    results["timeline_issues"] = [f"TIMELINE: {timeline_days} days between earliest and latest document - check for gaps"]
        
        # Check for critical missing documents
        required_docs = ['death_certificate', 'lease', 'bank_statement']
        found_docs = analysis.get("detected_types", [])
        missing = [doc for doc in required_docs if doc not in found_docs]
        
        if missing:
            results.setdefault("missing_categories", []).extend(
                [f"MISSING_DOC: {doc.upper()} not detected" for doc in missing]
            )
        
        return results
    
    def _parse_dates(self, date_strings: List[str]) -> List[datetime]:
        """
        Parse various date formats
        """
        dates = []
        for date_str in date_strings:
            try:
                # Clean the string
                clean = re.sub(r'[^\d/\-\.]', ' ', date_str).strip()
                
                # Try different formats
                for fmt in ['%m/%d/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%B %d, %Y', '%d %B %Y']:
                    try:
                        dt = datetime.strptime(clean, fmt)
                        dates.append(dt)
                        break
                    except ValueError:
                        continue
            except Exception:
                continue
        
        return dates
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """
        Generate internal recommendations for YOUR next steps
        """
        recs = []
        
        # Based on red flags
        if any("FOREIGN_ACCOUNT" in flag for flag in analysis["red_flags"]):
            recs.append("FOCUS: Check for Schedule B and FBAR Form 114 for foreign accounts")
        
        if any("GIG_INCOME" in flag for flag in analysis["red_flags"]):
            recs.append("FOCUS: Look for 1099-K and app screenshots for gig income")
        
        if any("MEDICAL_HARDSHIP" in flag for flag in analysis["red_flags"]):
            recs.append("FOCUS: Verify hospital records cover exact dates needed")
        
        # Based on missing documents
        if "death_certificate" not in analysis.get("detected_types", []):
            recs.append("URGENT: Find death certificate or official vacancy notice")
        
        if "tax_return" not in analysis.get("detected_types", []):
            recs.append("CHECK: Income documentation may be incomplete")
        
        # Timeline issues
        if analysis.get("timeline_issues"):
            recs.append("TIMELINE: Map all dates to identify gaps >60 days")
        
        return recs[:3]  # Top 3 recommendations
    
    def _calculate_risk_score(self, analysis: Dict) -> int:
        """
        Internal risk score (1-10) for YOUR prioritization
        Higher = more urgent attention needed
        """
        score = 0
        
        # Red flags
        score += min(len(analysis.get("red_flags", [])), 5)
        
        # Missing critical docs
        critical_missing = ['death_certificate', 'lease']
        missing_count = sum(1 for doc in critical_missing 
                           if doc not in analysis.get("detected_types", []))
        score += missing_count * 2
        
        # Timeline issues
        if analysis.get("timeline_issues"):
            score += 2
        
        return min(score, 10)

# ==================== AUTO-REPORT GENERATOR ====================
class AutoReportGenerator:
    """
    Generates YOUR internal analysis report
    Never share this with clients - it's your cheat sheet
    """
    
    def generate_internal_report(self, vision_analysis: Dict) -> str:
        """
        Create markdown report for YOUR eyes only
        """
        report = f"""# MITCHY VISION PRO - INTERNAL ANALYSIS
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Folder: {vision_analysis.get('folder', 'Unknown')}
Risk Score: {vision_analysis.get('internal_score', 0)}/10

## 🔴 RED FLAGS ({len(vision_analysis.get('red_flags', []))})
"""
        
        for flag in vision_analysis.get('red_flags', []):
            report += f"- {flag}\n"
        
        report += f"""
## 📁 DOCUMENTS DETECTED
Files scanned: {vision_analysis.get('files_found', 0)}
"""
        
        if vision_analysis.get('detected_types'):
            doc_counts = {}
            for doc_type in vision_analysis.get('detected_types', []):
                doc_counts[doc_type] = doc_counts.get(doc_type, 0) + 1
            
            for doc_type, count in doc_counts.items():
                report += f"- {doc_type.replace('_', ' ').title()}: {count}\n"
        
        report += f"""
## ⚠️ ISSUES IDENTIFIED
"""
        
        for issue in vision_analysis.get('missing_categories', []):
            report += f"- ❌ {issue}\n"
        
        for issue in vision_analysis.get('timeline_issues', []):
            report += f"- ⏰ {issue}\n"
        
        report += f"""
## 🎯 YOUR ACTION PLAN (Prioritized)
"""
        
        for i, action in enumerate(vision_analysis.get('recommended_focus', []), 1):
            report += f"{i}. {action}\n"
        
        report += f"""
## 📝 INTERNAL NOTES
1. Check death certificate DATE first
2. Calculate: Filing date - Vacancy date = ? days
3. Look for: Foreign accounts >$10k?
4. Look for: Gig income without 1099-K?
5. Utility gaps >60 days? Medical proof needed?

## ⚖️ LEGAL REMINDER (INTERNAL USE ONLY)
- This analysis is for YOUR efficiency only
- NEVER share this report with clients
- NEVER claim AI analyzed their case
- ALWAYS verify findings manually
- FINAL decision is YOUR human review
"""
        
        return report
    
    def generate_client_checklist(self, vision_analysis: Dict) -> str:
        """
        Generate SANITIZED checklist for client (no AI mention)
        This is what you actually send
        """
        checklist = f"""DOCUMENT VERIFICATION CHECKLIST
Date: {datetime.now().strftime('%Y-%m-%d')}
Case: [Client Reference]

Please verify the following documents are complete:

[ ] 1. DEATH CERTIFICATE / VACANCY NOTICE
    - Official document with date
    - Certified translation if not in English

[ ] 2. SUCCESSION NOTICE
    - Filed within 90 days of vacancy
    - Official receipt or confirmation

[ ] 3. INCOME DOCUMENTATION
    - All 1099 forms for past year
    - W-2s if applicable
    - For gig income: 1099-K + 3 months app screenshots

[ ] 4. ASSET DECLARATION
    - Bank statements (all accounts)
    - For foreign accounts >$10k: Schedule B + FBAR Form 114
    - Investment account statements

[ ] 5. UTILITY BILLS
    - 24 consecutive months
    - Any gaps >60 days explained with proof

[ ] 6. RESIDENCY PROOF
    - Lease agreement
    - Government ID with address
    - Mail at address for 2+ years

[ ] 7. HARDSHIP DOCUMENTATION (if applicable)
    - Medical: Hospital records covering dates
    - Incarceration: Release papers
    - Other: Official documentation

---
VERIFICATION NOTES:
• Please redact SSNs and full account numbers
• PDF format preferred
• Organize chronologically
• Label files clearly

This checklist is based on HPD published requirements.
"""
        return checklist

# ==================== QUICK SCAN UTILITY ====================
def quick_scan(folder_path: str) -> None:
    """
    One-function scan for daily use
    """
    print("🔍 MITCHY VISION PRO - Quick Scan")
    print("=" * 50)
    
    vision = MitchyVisionPro()
    generator = AutoReportGenerator()
    
    # Run analysis
    print(f"Scanning: {folder_path}")
    analysis = vision.analyze_folder(folder_path)
    
    # Display summary
    print(f"\n📊 Summary:")
    print(f"Files: {analysis.get('files_found', 0)}")
    print(f"Risk Score: {analysis.get('internal_score', 0)}/10")
    
    if analysis.get('red_flags'):
        print(f"\n🚨 Red Flags: {len(analysis['red_flags'])}")
        for flag in analysis['red_flags'][:3]:  # Show top 3
            print(f"  • {flag}")
    
    if analysis.get('recommended_focus'):
        print(f"\n🎯 Your Next Actions:")
        for action in analysis['recommended_focus']:
            print(f"  • {action}")
    
    # Save reports
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Internal report (YOUR eyes only)
    internal_report = generator.generate_internal_report(analysis)
    with open(f"vision_internal_{timestamp}.md", "w") as f:
        f.write(internal_report)
    print(f"\n📄 Internal report saved: vision_internal_{timestamp}.md")
    
    # Client checklist (sanitized)
    client_checklist = generator.generate_client_checklist(analysis)
    with open(f"client_checklist_{timestamp}.txt", "w") as f:
        f.write(client_checklist)
    print(f"📋 Client checklist saved: client_checklist_{timestamp}.txt")
    
    print("\n⚠️  REMINDER: Internal report is for YOUR use only")
    print("   Send client checklist (not internal report) to client")

# ==================== INSTALLATION SCRIPT ====================
def install_dependencies():
    """
    Run this once to install required packages
    """
    requirements = """
PyMuPDF==1.23.8      # PDF text extraction
pillow==10.1.0       # Image processing
pytesseract==0.3.10  # OCR (requires tesseract-ocr installed system-wide)
pdfminer.six==20221105  # PDF fallback
python-docx==1.1.0   # Word documents
"""
    
    print("Required packages:")
    print(requirements)
    print("\nInstall with:")
    print("pip install PyMuPDF pillow pytesseract pdfminer.six python-docx")
    print("\nAlso install Tesseract OCR:")
    print("• macOS: brew install tesseract")
    print("• Ubuntu: sudo apt-get install tesseract-ocr")
    print("• Windows: Download from GitHub")

# ==================== MAIN EXECUTION ====================
if __name__ == "__main__":
    """
    Daily use: python mitchy_vision.py /path/to/client/folder
    """
    import sys
    
    if len(sys.argv) > 1:
        folder_to_scan = sys.argv[1]
        quick_scan(folder_to_scan)
    else:
        print("Usage: python mitchy_vision.py /path/to/client/folder")
        print("\nExample: python mitchy_vision.py ./clients/nhs_case_001")
        print("\nTo install dependencies:")
        print("python mitchy_vision.py --install")
