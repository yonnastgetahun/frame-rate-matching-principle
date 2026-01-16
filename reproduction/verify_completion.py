#!/usr/bin/env python3
"""
Verify completion status of Study 0 and Study 1 signal extraction.
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict

def verify_study0(base_path: Path) -> dict:
    """Verify Study 0 signal files."""
    results_path = base_path / "data" / "results"

    json_files = list(results_path.rglob("*.json"))

    # Count by subdirectory
    by_dir = defaultdict(int)
    for f in json_files:
        rel = f.relative_to(results_path)
        by_dir[rel.parts[0] if len(rel.parts) > 1 else "root"] += 1

    return {
        "total_files": len(json_files),
        "expected": 4545,
        "by_directory": dict(by_dir),
        "status": "PASS" if len(json_files) >= 4500 else "WARN"
    }

def verify_study1(base_path: Path) -> dict:
    """Verify Study 1 signal files."""
    results_path = base_path / "experiments" / "analysis" / "study1_results" / "study1"

    brackets = {}
    total = 0

    for bracket in ["120fps", "48-50fps", "60fps"]:
        bracket_path = results_path / bracket
        if bracket_path.exists():
            files = list(bracket_path.rglob("*.json"))
            brackets[bracket] = len(files)
            total += len(files)
        else:
            brackets[bracket] = 0

    expected = {
        "120fps": 152,  # 38 clips × 4 FPS
        "48-50fps": 84,  # 21 clips × 4 FPS
        "60fps": 582,   # 163 clips × ~3.6 FPS (some timeouts)
    }

    status = "PASS"
    for bracket, count in brackets.items():
        if count < expected.get(bracket, 0) * 0.9:  # Allow 10% tolerance
            status = "WARN"

    return {
        "total_files": total,
        "expected": 818,
        "by_bracket": brackets,
        "expected_by_bracket": expected,
        "status": status
    }

def verify_analysis_outputs(base_path: Path) -> dict:
    """Verify analysis output files exist."""
    output_path = base_path / "experiments" / "analysis" / "output"

    required_files = [
        "all_results.csv",
        "scr_metrics.csv",
        "statistical_results.json",
        "table1_bracket_summary.csv",
        "fig1_scr_vs_fps_ratio.png",
    ]

    found = []
    missing = []

    for f in required_files:
        if (output_path / f).exists():
            found.append(f)
        else:
            missing.append(f)

    return {
        "found": found,
        "missing": missing,
        "status": "PASS" if not missing else "FAIL"
    }

def verify_documentation(base_path: Path) -> dict:
    """Verify documentation files exist."""
    docs_path = base_path / "docs"

    required_docs = [
        "reproducibility_package.md",
        "data_sources_acknowledgments.md",
        "osf_deviation_justification.md",
        "storage_exit_strategy.md",
    ]

    found = []
    missing = []

    for f in required_docs:
        if (docs_path / f).exists():
            found.append(f)
        else:
            missing.append(f)

    return {
        "found": found,
        "missing": missing,
        "status": "PASS" if not missing else "WARN"
    }

def verify_reproduction_materials(base_path: Path) -> dict:
    """Verify reproduction materials exist."""
    repro_path = base_path / "reproduction"

    required = [
        "study1/request_academic.md",
        "study1/video_manifest.csv",
    ]

    found = []
    missing = []

    for f in required:
        if (repro_path / f).exists():
            found.append(f)
        else:
            missing.append(f)

    return {
        "found": found,
        "missing": missing,
        "status": "PASS" if not missing else "WARN"
    }

def main():
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1]).resolve()
    else:
        base_path = Path.cwd()

    print("=" * 60)
    print("Research Completion Verification")
    print("=" * 60)
    print(f"\nBase path: {base_path}\n")

    # Run all verifications
    results = {
        "Study 0 Signals": verify_study0(base_path),
        "Study 1 Signals": verify_study1(base_path),
        "Analysis Outputs": verify_analysis_outputs(base_path),
        "Documentation": verify_documentation(base_path),
        "Reproduction Materials": verify_reproduction_materials(base_path),
    }

    # Print results
    all_pass = True
    for name, result in results.items():
        status = result.get("status", "UNKNOWN")
        icon = "✅" if status == "PASS" else "⚠️" if status == "WARN" else "❌"
        print(f"{icon} {name}: {status}")

        if "total_files" in result:
            print(f"   Files: {result['total_files']} (expected: {result['expected']})")

        if "by_bracket" in result:
            for bracket, count in result["by_bracket"].items():
                expected = result["expected_by_bracket"].get(bracket, "?")
                print(f"   - {bracket}: {count}/{expected}")

        if "missing" in result and result["missing"]:
            print(f"   Missing: {', '.join(result['missing'])}")

        if status != "PASS":
            all_pass = False

        print()

    # Summary
    print("=" * 60)
    if all_pass:
        print("✅ ALL VERIFICATIONS PASSED")
        print("\nReady for:")
        print("  1. Archive raw videos to external drive")
        print("  2. Upload OSF package")
        print("  3. Delete Modal volume")
        print("  4. Cancel Modal subscription")
    else:
        print("⚠️  SOME VERIFICATIONS HAD WARNINGS")
        print("\nReview warnings above before proceeding.")
    print("=" * 60)

    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(main())
