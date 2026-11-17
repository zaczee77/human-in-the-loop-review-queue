"""Reference demo: a human in the loop review queue for LLM outputs.

Plain Python, standard library only. No network calls. Every sample item
is invented data written only to exercise the pattern.

The pattern: an LLM draft never leaves the queue on its own. Each item is
checked for a citation, for verified numbers, and for guarded wording.
A reviewer then makes the decision, and the audit trail records it.
Nothing is approved by the model, and nothing leaves without a human
decision attached.
"""

REVIEWER = "Reviewer A"


class ReviewItem:
    """One LLM draft waiting for a human decision."""

    def __init__(self, item_id, title, has_citation, numbers_verified,
                 guarded_phrase):
        self.item_id = item_id
        self.title = title
        self.has_citation = has_citation
        self.numbers_verified = numbers_verified
        self.guarded_phrase = guarded_phrase
        self.decision = None
        self.reason = None
        self.risk_level = None

    def risk(self):
        if self.guarded_phrase:
            return "high"
        if not self.has_citation and not self.numbers_verified:
            return "high"
        if not self.has_citation or not self.numbers_verified:
            return "medium"
        return "low"


class ReviewQueue:
    """The queue. It holds items, decisions, and the audit trail."""

    def __init__(self):
        self.items = []
        self.audit = []

    def add(self, item):
        self.items.append(item)

    def record(self, item, action, reason):
        self.audit.append({
            "item": item.item_id,
            "action": action,
            "reviewer": REVIEWER,
            "reason": reason,
        })

    def review(self, item):
        """One reviewer decision per item, driven by the risk level."""
        risk = item.risk()
        item.risk_level = risk
        if risk == "low":
            item.decision = "approved"
            item.reason = "citation present, numbers verified, no guarded wording"
            self.record(item, "approved", item.reason)
        elif risk == "medium":
            missing = []
            if not item.has_citation:
                missing.append("citation")
            if not item.numbers_verified:
                missing.append("verified numbers")
            self.record(item, "edit requested",
                        "missing " + " and ".join(missing))
            item.has_citation = True
            item.numbers_verified = True
            item.decision = "approved after edit"
            item.reason = "edit added the missing " + " and ".join(missing)
            self.record(item, "approved after edit", item.reason)
        elif item.guarded_phrase:
            item.decision = "rejected"
            item.reason = "guarded wording present, draft must be rewritten"
            self.record(item, "rejected", item.reason)
        else:
            item.decision = "escalated"
            item.reason = "citation and verified numbers both missing"
            self.record(item, "escalated", item.reason)

    def run(self):
        for item in self.items:
            self.review(item)

    def summary(self):
        approved = sum(1 for i in self.items
                       if i.decision in ("approved", "approved after edit"))
        rejected = sum(1 for i in self.items if i.decision == "rejected")
        escalated = sum(1 for i in self.items if i.decision == "escalated")
        undecided = sum(1 for i in self.items if i.decision is None)
        return {
            "total": len(self.items),
            "approved": approved,
            "rejected": rejected,
            "escalated": escalated,
            "undecided": undecided,
            "audit_entries": len(self.audit),
        }


def build_queue():
    queue = ReviewQueue()
    queue.add(ReviewItem(1, "Prior authorization summary, routine imaging",
                         True, True, False))
    queue.add(ReviewItem(2, "Pharmacy billing note, routine claim",
                         False, True, False))
    queue.add(ReviewItem(3, "Coverage summary, specialty drug request",
                         True, False, False))
    queue.add(ReviewItem(4, "Draft letter about a denied claim",
                         True, True, True))
    queue.add(ReviewItem(5, "Eligibility summary, new patient",
                         True, True, False))
    queue.add(ReviewItem(6, "Summary of a complex prior authorization case",
                         False, False, False))
    return queue


def main():
    queue = build_queue()
    queue.run()
    for item in queue.items:
        print("Item " + str(item.item_id) + ": " + item.title)
        print("  risk: " + item.risk_level + ", decision: " + item.decision)
        print("  reason: " + item.reason)
    print("")
    print("Audit trail:")
    for entry in queue.audit:
        print("  item " + str(entry["item"]) + ": " + entry["action"]
              + " by " + entry["reviewer"] + ", " + entry["reason"])
    result = queue.summary()
    print("")
    print("Summary: " + str(result["total"]) + " items reviewed, "
          + str(result["approved"]) + " approved, "
          + str(result["rejected"]) + " rejected, "
          + str(result["escalated"]) + " escalated, "
          + str(result["audit_entries"]) + " audit entries, "
          + str(result["undecided"]) + " left undecided.")
    assert result["undecided"] == 0, "every item needs a decision"
    assert result["total"] == result["approved"] + result["rejected"] \
        + result["escalated"], "every item ends in exactly one outcome"
    assert all(entry["reviewer"] for entry in queue.audit), \
        "every audit entry names its reviewer"
    print("Checks passed: every item has one human decision, "
          "and the audit trail covers every step.")


if __name__ == "__main__":
    main()
