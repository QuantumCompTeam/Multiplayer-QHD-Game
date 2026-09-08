# Macroscope review resolution — PR #22

Reviewed all eight inline findings on commit `19fbd84` before the user-authorized
merge. Six were correctness findings (one high, five medium); two were low
severity documentation findings. All eight are addressed. No QPU jobs were
submitted to test these changes, and no historical registrations were modified.

| Review thread | Resolution |
|---|---|
| [3958750675](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750675) — ring verification did not fail on divergence | Reject any nonzero advantage difference before appending/writing the report. Environment/version/convention checks also use explicit exceptions. An injected mismatch leaves the existing evidence untouched. |
| [3958750684](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750684) — submission/ID persistence gap | Flush a unique tagged submission intent before contacting the provider; send that tag with the job. Recovery can look up a job by tag if the response or pending-file write was interrupted. Pending records use flushed atomic writes. Zero or multiple matches fail closed and never cause resubmission. The old CLI already rejected reuse of an existing output directory, but could not recover this interrupted-submit case. |
| [3958750685](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750685) — CLI bypassed unique run allocation | The actual experiment CLI now uses automatic allocation and the allocated directory name as its timestamp. Two CLI invocations in the same minute produce distinct outputs and preserve the first result. |
| [3958750692](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750692) — source ZIP not authenticated against manifest | Before extraction, require the exact member inventory, reject duplicates, and check every source file, class, bibliography style and generated bibliography hash. Validation remains active under Python optimization. |
| [3958750693](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750693) — bibliography dependency omitted | Include resolved IEEEtran.bst and generated qhd.bbl, with their hashes. A recipient still needs a LaTeX installation, but these bibliography files now accompany the submission. |
| [3958750695](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750695) — audit described finished work as pending | Replace the stale future-tense validation section with completed results and a link to this follow-up. |
| [3958750704](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750704) — stale page count | Distinguish the September 7 17-page PDF from the current validated 18-page submission. |
| [3958750718](https://github.com/QuantumCompTeam/Multiplayer-QHD-Game/pull/22#discussion_r3958750718) — audit assertions disappear under python -O | Replace evidence assertions with explicit raising checks; verify rejection of an altered manifest in a separate optimized Python process. |

## Validation and limits

The initial 13 failure-path tests pass. The original three saved hardware results
still pass the independent audit, including under `python -O`, and the ring
recomputation still exactly matches the five source gaps. The complete Linux
suite runs on the updated PR before merge; its check result is authoritative.

The provider may index tagged jobs asynchronously. If recovery cannot yet find
exactly one job, retry recovery later; do not create a replacement submission.
Historical code hashes stay frozen: old registrations still require their
appropriate committed source checkout. The new workflow applies to newly
prepared registrations. Simulated interruptions verify application recovery;
they do not establish provider availability or protection against disk loss.

Macroscope's separate automatic-approval check is disabled for this workspace.
Its settings are not changed or bypassed. The user explicitly authorized merge
after review and successful checks; merging is a manual repository action.

## Follow-up on 5c46eff

The fresh Macroscope review identified five additional edge cases, all addressed:

- The journal now persists directory entries with POSIX fsync after rename
  (including newly created ancestor entries); Windows uses the native
  MoveFileExW write-through option, since os.open cannot open directories for
  fsync there. This follows the [Microsoft API documentation](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw).
- The independent audit rejects negative, fractional and boolean frequencies,
  invalid shot totals, and empty deviation evidence instead of accepting a
  vacuous equilibrium certificate.
- Ring verification prints by default. Optional `--output` creates a new file
  exclusively and refuses to overwrite existing evidence, including on a
  successful rerun. Its strict zero-difference requirement remains intentional
  for this explicitly pinned reproduction; the unrounded differences are shown.
- The change inventory labels older validation counts as historical and locates
  the incentive boundary in the current Section IV.

Additional tests cover these cases; the directory-fsync test runs on Linux CI,
while Windows exercises the native write-through path in recovery tests.
