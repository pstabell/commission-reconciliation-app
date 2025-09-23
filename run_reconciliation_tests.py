#!/usr/bin/env python3
"""
Master Test Runner for Reconciliation Security Tests
Runs all reconciliation-related security tests and generates a report
"""

import subprocess
import sys
import datetime

def run_test_script(script_name):
    """Run a test script and capture the results"""
    print(f"\n🏃 Running {script_name}...")
    print("-" * 60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, 
                              text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False

def generate_report(results):
    """Generate a test report"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report = f"""
{'='*80}
RECONCILIATION SECURITY TEST REPORT
Generated: {timestamp}
{'='*80}

TEST RESULTS:
"""
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        report += f"\n{test_name}: {status}"
        if not passed:
            all_passed = False
    
    report += f"""

{'='*80}
OVERALL RESULT: {"✅ ALL TESTS PASSED" if all_passed else "❌ SOME TESTS FAILED"}
{'='*80}

SECURITY FEATURES TESTED:
1. Row-Level Security (RLS) enforcement
2. User data isolation in reconciliation imports
3. Proper handling of -STMT-, -VOID-, -ADJ- entries
4. Merge operation security
5. Cross-user data leakage prevention

"""
    
    if all_passed:
        report += """
CONCLUSION:
The reconciliation feature is secure and properly implements user isolation.
All security measures are working as expected.
"""
    else:
        report += """
⚠️  SECURITY ISSUES DETECTED ⚠️
Please review the failed tests and fix security vulnerabilities before deploying.
"""
    
    return report

def main():
    """Main test runner"""
    print("="*80)
    print("RECONCILIATION SECURITY TEST SUITE")
    print("="*80)
    
    # Define test scripts
    test_scripts = {
        "Comprehensive Security Test": "test_reconciliation_security.py",
        "Import Fix Verification": "test_reconciliation_import_fix.py"
    }
    
    # Run tests
    results = {}
    for test_name, script_path in test_scripts.items():
        results[test_name] = run_test_script(script_path)
    
    # Generate and display report
    report = generate_report(results)
    print(report)
    
    # Save report to file
    report_filename = f"reconciliation_test_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_filename, 'w') as f:
        f.write(report)
    print(f"\n📄 Report saved to: {report_filename}")
    
    # Return appropriate exit code
    return 0 if all(results.values()) else 1

if __name__ == "__main__":
    sys.exit(main())