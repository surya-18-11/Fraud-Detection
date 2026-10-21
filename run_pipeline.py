"""
run_pipeline.py — Master pipeline runner for IEEE-CIS Fraud Detection
Executes all phases sequentially using nbconvert.
"""
import subprocess
import sys
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
VENV_PYTHON   = BASE_DIR / "venv" / "Scripts" / "python.exe"

# Phase definitions: (notebook_file, phase_name, estimated_minutes)
PHASES = [
    ("phase2_preprocessing.ipynb",       "Phase 2 — Preprocessing & Merging",       8),
    ("phase3_eda.ipynb",                 "Phase 3 — Exploratory Data Analysis",      5),
    ("phase4_feature_engineering.ipynb", "Phase 4 — Feature Engineering",            6),
    ("phase5_model_training.ipynb",      "Phase 5 — Model Training (LR + RF + XGB)", 30),
    ("phase6_evaluation.ipynb",          "Phase 6 — Evaluation & Metrics",           5),
    ("phase7_anomaly_detection.ipynb",   "Phase 7 — Anomaly Detection",              8),
]


def print_banner():
    print("=" * 70)
    print("  IEEE-CIS FRAUD DETECTION — Full ML Pipeline Runner")
    print("=" * 70)
    print(f"  Base dir      : {BASE_DIR}")
    print(f"  Notebooks dir : {NOTEBOOKS_DIR}")
    print(f"  Python        : {VENV_PYTHON}")
    print("=" * 70)
    print()


def run_notebook(notebook_path: Path, phase_name: str) -> bool:
    """Execute a Jupyter notebook in-place via nbconvert.

    Args:
        notebook_path: Path to the .ipynb file
        phase_name: Human-readable name for logging
    Returns:
        True if successful, False otherwise
    """
    print(f"\n{'='*70}")
    print(f"  RUNNING: {phase_name}")
    print(f"  File   : {notebook_path.name}")
    print(f"{'='*70}")

    if not notebook_path.exists():
        print(f"  ERROR: Notebook not found: {notebook_path}")
        return False

    start = time.time()

    cmd = [
        str(VENV_PYTHON), "-m", "nbconvert",
        "--to", "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=3600",
        "--ExecutePreprocessor.kernel_name=python3",
        str(notebook_path)
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(BASE_DIR)
        )

        elapsed = time.time() - start

        if result.returncode == 0:
            print(f"  SUCCESS: Completed in {elapsed/60:.1f} minutes")
            return True
        else:
            print(f"  FAILED after {elapsed/60:.1f} minutes")
            print(f"  STDOUT: {result.stdout[-2000:] if result.stdout else 'none'}")
            print(f"  STDERR: {result.stderr[-2000:] if result.stderr else 'none'}")
            return False

    except Exception as e:
        print(f"  EXCEPTION: {e}")
        return False


def check_prerequisites():
    """Check that nbconvert is installed and notebooks dir exists."""
    print("Checking prerequisites...")

    if not VENV_PYTHON.exists():
        print(f"  ERROR: Python not found at {VENV_PYTHON}")
        sys.exit(1)

    result = subprocess.run(
        [str(VENV_PYTHON), "-m", "nbconvert", "--version"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print("  ERROR: nbconvert not available. Run: pip install nbconvert")
        sys.exit(1)

    print(f"  nbconvert: OK ({result.stdout.strip()})")

    if not NOTEBOOKS_DIR.exists():
        print(f"  ERROR: Notebooks directory not found: {NOTEBOOKS_DIR}")
        sys.exit(1)

    print(f"  Notebooks dir: OK")
    print()


def run_all_phases(start_from: int = 2, stop_at: int = 7):
    """Run all pipeline phases sequentially.

    Args:
        start_from: Phase number to start from (2-7)
        stop_at: Phase number to stop at (inclusive)
    """
    print_banner()
    check_prerequisites()

    # Filter phases by range
    phases_to_run = []
    for nb_file, name, est_mins in PHASES:
        phase_num = int(nb_file[5])  # extract phase number from filename
        if start_from <= phase_num <= stop_at:
            phases_to_run.append((nb_file, name, est_mins, phase_num))

    total_est = sum(m for _, _, m, _ in phases_to_run)
    print(f"Phases to run: {len(phases_to_run)}")
    print(f"Estimated total time: ~{total_est} minutes")
    print()

    results = []
    pipeline_start = time.time()

    for nb_file, name, est_mins, phase_num in phases_to_run:
        nb_path = NOTEBOOKS_DIR / nb_file
        success = run_notebook(nb_path, name)
        results.append((phase_num, name, success))

        if not success:
            print(f"\n  PIPELINE STOPPED at Phase {phase_num} due to error.")
            print("  Fix the error and re-run with --start-from {phase_num}")
            break

    # Summary
    total_elapsed = time.time() - pipeline_start
    print(f"\n{'='*70}")
    print("  PIPELINE SUMMARY")
    print(f"{'='*70}")
    for phase_num, name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"  Phase {phase_num}: [{status}] {name}")
    print(f"\n  Total time: {total_elapsed/60:.1f} minutes")

    all_passed = all(s for _, _, s in results)
    if all_passed:
        print("\n  ALL PHASES COMPLETE!")
        print("  Launch the Streamlit app with:")
        print("  .\\venv\\Scripts\\streamlit run app\\app.py")
    else:
        print("\n  PIPELINE INCOMPLETE — check errors above")

    return all_passed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IEEE-CIS Fraud Detection Pipeline Runner")
    parser.add_argument("--start-from", type=int, default=2, metavar="N",
                        help="Start from phase N (default: 2)")
    parser.add_argument("--stop-at",    type=int, default=7, metavar="N",
                        help="Stop at phase N inclusive (default: 7)")
    args = parser.parse_args()

    success = run_all_phases(start_from=args.start_from, stop_at=args.stop_at)
    sys.exit(0 if success else 1)
