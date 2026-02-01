# calibration_workflow.py (27 lines)
def manual_calibration(file_path: str) -> dict:
    """
    Manual HPD calibration workflow - NO AI, NO APIs
    Run this after you have 5 paying clients demanding automation
    """
    findings = []
    
    # Rule INC-03: Gig income verification
    if "gig income" in file_path.lower() and "1099-k" not in file_path.lower():
        findings.append({
            "rule": "INC-03",
            "failure": "Gig income missing 1099-K + app screenshots",
            "remediation": "Obtain 2025 1099-K + 3 months DoorDash screenshots",
            "source": "HPD Form-1 Audit Checklist §3.2"
        })
    
    # Rule AST-01: Foreign asset declaration
    if "foreign account" in file_path.lower() and "schedule b" not in file_path.lower():
        findings.append({
            "rule": "AST-01",
            "failure": "Foreign accounts >$10k not declared on Schedule B",
            "remediation": "File amended 2024 tax return with Schedule B + FBAR",
            "warning": "Undeclared foreign assets = automatic rejection + 2-yr ban",
            "source": "IRS/HPD Data Share Agreement"
        })
    
    return {"findings": findings, "risk_score": len(findings) * 7}
