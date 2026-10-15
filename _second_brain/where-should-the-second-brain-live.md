---
title: Where should the second brain live?
dek: It is a connector decision, not a storage decision.
date: 2026-10-15
---

In our first article, we defined what a second brain actually is: the persistent layer of context, rules, and memory that turns an ephemeral AI chat into a reliable operating partner.

Once you decide you need one, the immediate question seems simple: Where do we put it?

Most teams treat this as a standard IT storage decision. Someone suggests Notion. Someone else suggests SharePoint for enterprise compliance. A technical founder wants a vector database or Neo4j graph. Someone else uploads twenty PDFs into a Claude Project and calls it a day.

Within a month, almost all of them hit a wall.

Across production setups we work with, we've watched teams move their memory four times in five weeks. None of those moves was about disk space. All were about workflow, permissions, and connectors.

Here is what we have learnt (the hard way) about where a second brain should live.

## It is a connector decision, not a storage decision

The first mistake is choosing a home where your AI can only read.

In one program we worked with, the initial choice was an enterprise SharePoint instance. It checked every compliance box. But within days, the team discovered that corporate IT rules prevented AI agents from writing back to it. Every time an agent extracted a decision or updated a note, a human had to copy-paste the output.

That defeats the purpose. A second brain is not a digital archive; it is an active workshop.

Before committing to any platform, run one test: Can your AI agent both read and write to this location today, autonomously? If it can only read, you haven't built a second brain; you've built a reading list. A caveat to this, while writing as a feature is important for the agent, it also means the agent can write incorrect things in your second brain, this is where human monitoring, agent guardrails and roll-back options play a role.

## Don't build inside the model's walled garden

It is tempting to keep your memory inside Claude Projects, ChatGPT workspaces, or proprietary tool silos.

It feels frictionless on day one. But two problems hit immediately:

- **Copies drift.** The moment you edit a note inside a vendor's workspace, it decouples from your team drive. Within two weeks, you have competing versions of reality, and neither is trustworthy.
- **Harness churn.** The AI tool you love today is not the one you will use eighteen months from now. Trapping institutional knowledge inside a vendor's proprietary memory guarantees corporate amnesia when you switch providers.

Your data layer must outlive the model reading it. Plain Markdown files, CSVs, and standard folder hierarchies have survived forty years of computing cycles. Build your memory in plain files on standard file systems, ideally adding versioning through git; treat the LLM as a modular engine you point at those files.

## Beware the knowledge graph trap

Whenever technical leaders (including ourselves) design an AI memory system, someone inevitably advocates for a knowledge graph, Neo4j, or complex GraphRAG pipeline.

We tried that. In an earlier production architecture, we deployed an automated knowledge graph backend. That meant 90-minute whole-graph rebuilds whenever files changed, brittle entity resolution, and constant schema debugging. The operational drag was enormous; the retrieval advantage was negligible.

We killed the graph backend completely, replacing it with flat Markdown files, YAML frontmatter, and deterministic local search (separate article on retrieval coming soon).

Unless you are indexing millions of cross-referenced legal filings, you do not need a graph database. At sub-5,000 document scale, structured Markdown and standard text search are faster, lower-latency, human-auditable, and free.

## The sweet spot: Local-first, cloud-synced

The dilemma is usually framed as Local vs. Cloud:

- **Pure local** gives you blazingly fast execution, privacy, and full access to local terminal tools. But shut the laptop lid, and your agent sleeps. Leave the company, and the memory leaves with you.
- **Pure cloud** lets the team collaborate, but introduces the connector tax: rate limits, brittle OAuth tokens, and sync delays.

The architecture that works in production is local-first, cloud-synced: a dedicated local directory mirrored to a shared corporate drive. Your AI agents run locally against the filesystem at machine speed with zero latency, while background sync keeps the team's master record updated.

## Ownership is invisible until it breaks

Almost every second brain begins inside a personal cloud folder or laptop because someone wants to move fast.

Then the system reaches 1,000 files across 200 folders. When you onboard an intern, contractor, or autonomous daemon on a server, permissions collapse. You spend days executing messy bulk ownership transfers because personal accounts block automation.

From minute one:

- Create the root folder under a dedicated company account, never a personal inbox.
- Set up at least two team members with full admin recovery access.
- Declare the location an invariant: no moving or re-architecting the folder tree without explicit sign-off.

## Draw access boundaries before you save File #1

You cannot solve privacy by trying to remember what not to tell the AI. The moment you invite a teammate or connect an autonomous agent, everything in that folder is fair game. Give the agent permissions and access only to what it needs to do its work, open up more only when needed, and draw a hard line on what the agent is never allowed to touch.

Before adding your first document, partition your directory into three clear zones:

- **Core Operating IP:** Playbooks, PRDs, customer discovery notes, and process guidelines open to the entire team and all agents.
- **Client / Deal Confidentiality:** Customer deliverables and NDA-bound notes restricted to specific project teams.
- **Corporate Governance:** Equity, cap tables, compensation notes, expenses and private board debriefs kept in a strictly segregated folder that general team agents never touch.

## The three rules to start with

If you are setting up your second brain this week, don't overcomplicate it:

1. Keep it in plain text (Markdown + frontmatter) so it remains portable across whatever AI tools arrive next year.
2. Host it in a company-owned shared drive that your AI can both read from and write to autonomously.
3. Partition your folders on day one so you can safely share context with teammates without leaking your cap table.

In the next piece, we will dig into Ingestion: how to get real data into your second brain continuously without drowning in documentation fatigue.
