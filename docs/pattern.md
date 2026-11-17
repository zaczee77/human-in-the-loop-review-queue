# The human in the loop review queue pattern

## Where the pattern comes from

Paxei is a healthcare AI prior authorization assistant built by Nirmeet Rao and presented on his portfolio at nirmeetrao.com. Its own description puts human review at the center of the process: the assistant prepares the work, and a person reviews it before anything moves forward. PharmFlows, his workflow product at Concordia Pharma, uses the same shape: a review loop checks workflow output before it moves on. This pattern writes down the review step those products share, so it can be reused wherever an LLM draft meets a decision that matters.

## The queue

Every draft enters one queue. The queue is the only way out. A draft that never enters the queue cannot be approved, and a draft that never leaves the queue cannot be sent, filed, or billed. That single rule is what turns review from a habit into a gate.

Each item in the queue carries the draft, the checks run on it, and, once decided, the decision, the reason, and the reviewer. An item with no decision is unfinished work, and the queue is not done until the count of unfinished items is zero.

## The three checks

Every item is checked the same way, in the same order.

1. Citation present. Can the claim in the draft be traced to a source. A summary with no citation is a claim with no address. It may be right, but nobody can check it.
2. Numbers verified. Is every number in the draft one someone has confirmed. A figure that came from the model is a guess until a person or a trusted source confirms it.
3. Guarded wording absent. Does the text carry wording that should never go out as written, such as a promise of approval or a definitive clinical claim. Guarded wording is a stop sign, not a style note.

The checks are deliberately small. A checklist with three items gets run every time. A checklist with thirty items gets skipped when the day is busy.

## Risk decides the path

The checks combine into a risk level, and the risk level decides what happens next.

1. Low risk. Citation present, numbers verified, no guarded wording. The reviewer can approve.
2. Medium risk. One of the citation or the verified numbers is missing, and no guarded wording is present. The item goes back for an edit. The edit adds exactly what is missing, and the item is approved only after the edit.
3. High risk. Guarded wording is present, or both the citation and the verified numbers are missing. Guarded wording means reject, because the draft must be rewritten rather than patched. Both checks missing means escalate, because the draft needs a closer look than a quick edit can give.

No risk level approves itself. The model never approves its own draft, and the queue never approves an item because it has waited long enough.

## The four decisions

A reviewer makes one of four decisions on each item, and only one.

1. Approve. The item is ready as written.
2. Approve after edit. The item was missing something, the edit supplied it, and the item is ready now.
3. Reject. The item carries guarded wording and must be rewritten. A rejection names the wording, so the rewrite knows what to remove.
4. Escalate. The item is missing too much for a quick edit, so it goes to someone who can look closer.

Each decision records the reviewer by name and the reason in plain words. The audit trail is the list of those records, in order. If a question comes up later about an item, the trail answers it: who decided, what they decided, and why.

## Design principles

1. The queue is the only way out. A draft that skips the queue is a draft nobody reviewed, whatever its quality.
2. The same checks every time. Review quality comes from consistency, not from a brilliant reviewer on a good day.
3. The reason travels with the decision. A decision without a reason cannot be audited, and an audit trail without reasons is a log of names.
4. An edit is a second decision, not a quiet fix. The edit is recorded, and the approval after it is a separate record from the edit request.
5. Rejection is a normal outcome. A queue that never rejects is not reviewing. It is stamping.
6. Undecided is unfinished. The queue closes only when every item has a decision, and the count of undecided items is printed, not assumed.

## What the demo shows, and what it does not show

The demo in this repository shows the pattern at miniature scale: six invented items, three checks, four decisions, and an audit trail of eight steps. It shows the shape of the work: a gate, a consistent check, a named decision, and a record. It does not show real drafts, real records, real reviewers, or measured results, and it does not show the Paxei product or the PharmFlows product. Real check logic, real citation sources, and real escalation routes are all real parts of a review queue, and none of them are modeled in the demo. The demo is a reference implementation of the pattern, written in plain Python with no external packages.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
