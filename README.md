# Human in the loop review queue

A reference pattern and a small runnable demo for the review step that sits between an LLM draft and anything a person acts on. The pattern comes from work Nirmeet Rao has shipped in healthcare AI: Paxei, a prior authorization assistant that keeps human review at the center of the process, and PharmFlows, where a review loop checks workflow output before it moves forward.

## The problem

An LLM can draft a summary, a letter, or a billing note in seconds. The draft is useful only if someone checks it before it is sent, filed, or billed. The failure mode is not a bad draft. It is a draft nobody looked at. A missing citation becomes a claim nobody can trace. A number nobody verified becomes a figure nobody can defend. A confident phrase becomes a promise nobody meant to make.

A review step fixes this only if it is a real gate. A queue where items can slip through unreviewed is a list, not a gate. A review that leaves no record is a conversation, not an audit trail.

## What the pattern does

1. Every draft enters a queue. Nothing goes straight from the model to the outside world.
2. Every item is checked the same way. The demo checks three things: is a citation present, are the numbers verified, and does the text carry guarded wording that should never go out as written.
3. Risk decides the path, not the mood of the day. Low risk items can be approved. Medium risk items go back for an edit and are approved only after the edit. High risk items are rejected or escalated, never quietly approved.
4. A named reviewer makes every decision. The decision, the reason, and the reviewer are recorded together, so any item can be traced back to the person who cleared it.
5. The queue closes only when every item has a decision. Zero items left undecided is the test, not a hope.

## The demo in this repository

The demo folder contains a small reference demo in plain Python with no external packages. It runs six invented items through the queue: two clean items approved directly, two items approved after an edit that adds the missing citation or the missing verified numbers, one item rejected for guarded wording, and one item escalated because both the citation and the verified numbers are missing. The audit trail records all eight steps, each with its reviewer and reason.

The docs folder describes the pattern in full: the checks, the risk levels, the four decisions, and the audit trail rule.

## What this is not

This demo is not the Paxei product and not the PharmFlows product. It models the review pattern those products use, at miniature scale, with invented sample data. No real patient records, claims, or model outputs appear here, and no accuracy, speed, or outcome number is claimed. A real review queue would call a language model to draft the text and would run its checks against real records. Neither the model nor the records are modeled here.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
