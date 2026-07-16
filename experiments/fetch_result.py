"""Fetch a finished IBM Quantum job by ID and compute its measured advantage.

Use this to recover a run whose CLIENT died (network drop, sleep, Ctrl-C)
AFTER the job was already submitted -- the job keeps running on IBM's servers,
so re-submitting would only waste credits and queue time. The job_id is stable;
re-run this whenever you like.

    python experiments/fetch_result.py d9br6l66hjac73fg3g7g

Reuses the exact account/auth and the counts->advantage + save logic from
hardware_n3_ghz.py, so the result.json it writes is identical to what the
original --hardware run would have produced.
"""

import os
import sys

# Ensure this file's directory is importable whatever the caller's CWD, so the
# hardware_n3_ghz import below resolves. That module defines load_service /
# counts_to_advantage / save_run and only runs main() under __main__, so
# importing it here has no side effects.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hardware_n3_ghz import load_service, counts_to_advantage, save_run


def main():
    if len(sys.argv) != 2:
        print("usage: python experiments/fetch_result.py <job_id>")
        sys.exit(2)
    job_id = sys.argv[1]

    service = load_service()
    job = service.job(job_id)
    status = job.status()
    print(f"job {job_id} status: {status}")

    # status is a string ('DONE','QUEUED','RUNNING','ERROR','CANCELLED') in
    # qiskit-ibm-runtime; guard against still-pending or failed jobs.
    if str(status) not in ("DONE", "JobStatus.DONE"):
        if str(status) in ("ERROR", "CANCELLED", "JobStatus.ERROR",
                            "JobStatus.CANCELLED"):
            print(f"job did not complete ({status}). error message:")
            print(" ", job.error_message())
            sys.exit(1)
        print("job is not finished yet -- re-run this script later "
              "(the job_id stays valid).")
        sys.exit(0)

    result = job.result()
    counts = result[0].data.meas.get_counts()
    shots = sum(counts.values())
    print("counts:", counts)

    try:
        backend_name = job.backend().name
    except Exception:  # noqa: BLE001
        backend_name = str(getattr(job, "backend", lambda: None)())

    probs, measured, measured_q, measured_adv, ref = counts_to_advantage(
        counts, shots)
    # depth / 2q are transpilation-time facts not recoverable from a finished
    # job; record None. Everything else matches the live-run result.json.
    save_run(counts, shots, backend_name, job_id, None, None,
             measured, measured_q, measured_adv, ref)
    print(f"\nHardware advantage = {measured_adv:.6f} "
          f"(noiseless reference {ref['advantage']:.6f}). "
          "Any positive value validates that the quantum advantage survives on "
          "real hardware; the gap to 1.0 is device noise.")


if __name__ == "__main__":
    main()
