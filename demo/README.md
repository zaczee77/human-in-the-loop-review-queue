# Demo: human in the loop review queue

A small reference demo of the review pattern behind Paxei and PharmFlows: an LLM draft enters a queue, is checked the same way every time, and leaves only with a named human decision attached.

## How to run it

From the repository root, or from this folder:

```
python3 demo/review_queue_demo.py
```

Plain Python, no external packages, no network calls.

## What it does

1. Review item 1. A prior authorization summary for routine imaging. Citation present, numbers verified, no guarded wording. Low risk, approved.
2. Review item 2. A pharmacy billing note for a routine claim. No citation, numbers verified. Medium risk, edit requested to add the citation, then approved after edit.
3. Review item 3. A coverage summary for a specialty drug request. Citation present, numbers not verified. Medium risk, edit requested to verify the numbers, then approved after edit.
4. Review item 4. A draft letter about a denied claim. Guarded wording present. High risk, rejected, and the draft must be rewritten.
5. Review item 5. An eligibility summary for a new patient. Citation present, numbers verified, no guarded wording. Low risk, approved.
6. Review item 6. A summary of a complex prior authorization case. No citation and no verified numbers. High risk, escalated for a closer look.

## What it printed when it was tested

6 items reviewed, 4 approved, 1 rejected, 1 escalated, 8 audit entries, 0 left undecided. The 4 approvals split into 2 approved directly and 2 approved after edit. The audit trail lists all 8 steps, each with its reviewer and reason. The built in checks passed: every item has one human decision, every item ends in exactly one outcome, and every audit entry names its reviewer.

## What the sample data is

Every item title, check result, and decision reason in `review_queue_demo.py` is invented sample data written only to exercise the pattern. Nothing here is a real draft, a real claim, a real patient record, or a real reviewer decision. A real queue would hold real drafts and real records. None of those are modeled here.

## Files

1. `review_queue_demo.py`: the demo. The queue, the checks, the risk levels, the reviewer decisions, and the audit trail.
2. `README.md`: this file.
