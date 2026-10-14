---
url: https://www.sarvam.ai/products/coding-agents/
title: Coding Agents | Coding agent for long-running work
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:16:06.805990+00:00
---

# Coding Agents | Coding agent for long-running work

> Source: https://www.sarvam.ai/products/coding-agents/

![Sarvam Motif](https://assets.sarvam.ai/assets/motifs/ui/motif.svg)

Coding Agents

# Better code in the long run

Coding Agents work across the codebase and saves checkpoints as it goes. The plan stays visible, so you can change direction while the run is live.

[Try Coding Agents](https://indus.sarvam.ai)[Talk to us](https://www.sarvam.ai/contact-us)

![](https://assets.sarvam.ai/tr:w-1920,q-70,f-auto,dpr-auto/assets/products/coding-agents/hero/coding-agents-hero.webp)

user@sarvam:~/acme/payments-service$ sarvam-code

>_ Coding Agents (v0.38.0)

directory: ~/acme/payments-service

Migrate the payments data layer

› Move the payments service off the legacy ORM without downtime. Keep the public API stable. Stop the run if a contract test fails.

  1. Thought  for 6 seconds 

  2. Read  billing/repository.py, billing/models.py, tests/contract/ 

  3. Found  214 uses of 'session.execute' 

  4. I'll add a compatibility shim, migrate one module at a time, and run the contract suite after each change. Billing first.  I'll add a compatibility shim, migrate one module at a time, and run the contract suite after each change. Billing first.

  5. billing/repository.py +shim +41  -0 

  6. billing/models.py +data layer +96  -12 

  7. Contract tests pass. 3 of 5 steps done. Moving to the ledger module now.  Contract tests pass. 3 of 5 steps done. Moving to the ledger module now.




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Move on to the ledger module

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 38% used · Distinguished

[ Try Coding Agents ↗ ](https://indus.sarvam.ai)

##  A visible plan for work across the codebase. 

Coding Agents break the job into steps, writes and tests each change, and saves checkpoints as it goes. The plan stays visible throughout the run. 

###  Work across the codebase 

Give Coding Agents a refactor, migration, or performance problem that crosses services. It works through one part at a time while the original goal stays on the plan. 

![](https://assets.sarvam.ai/tr:w-800,q-70,f-auto,dpr-auto/assets/products/coding-agents/pillars/sarvam-code-01.webp)

Migrate 214 database calls

› Replace the legacy ORM across the payments service, one module at a time.

  1. Thought  for 4 seconds 

  2. Read  214 call sites across 18 modules 

  3. billing/repository.py +41  -0 

  4. ledger/queries.py +63  -8 




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Continue with the next module

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 4% used · Distinguished

###  Steer the run 

The whole plan stays on screen. Change the goal, move a step, or stop the current approach. Coding Agents pick up from the work already done. 

![](https://assets.sarvam.ai/tr:w-800,q-70,f-auto,dpr-auto/assets/products/coding-agents/pillars/sarvam-code-02.webp)

Reorder the migration plan

› Skip the webhook rewrite for now and finish the ledger module first. Keep the rest of the plan.

  1. Thought  for 2 seconds 

  2. Dropped  branch 'reconnect-webhooks' 

  3. Plan updated. The ledger module is step 3. The webhook rewrite is last.  Plan updated. The ledger module is step 3. The webhook rewrite is last.




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Start the ledger module now

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 4% used · Distinguished

###  Pick up from a checkpoint 

When a test fails or a path reaches a dead end, Coding Agents returns to a checkpoint and tries again. Completed steps stay in place. 

![](https://assets.sarvam.ai/tr:w-800,q-70,f-auto,dpr-auto/assets/products/coding-agents/pillars/sarvam-code-03.webp)

Recover from a failed test

› The ledger contract tests failed. Resume from the last checkpoint and keep the completed steps.

  1. Thought  for 7 seconds 

  2. Read  tests/contract/test_ledger.py 

  3. ledger/queries.py fix decimal rounding +6  -4 

  4. Contract suite passes. I resumed from the last checkpoint and kept the completed work.  Contract suite passes. I resumed from the last checkpoint and kept the completed work.




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Re-run the contract suite

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 4% used · Distinguished

##  Use expensive models only for the tasks that need them. 

### Pick a model for each task

A refactor and a rollback review call for different models. Coding Agents routes them separately during the same run.

### Pay for completed work

We charge for completed work. Retries and dead ends are not billed to you.

  1. ### Pick a model for each task

A refactor and a rollback review call for different models. Coding Agents routes them separately during the same run.

  2. ### Pay for completed work

We charge for completed work. Retries and dead ends are not billed to you.




![](https://assets.sarvam.ai/tr:w-1920,q-70,f-auto,dpr-auto/assets/products/coding-agents/pillars/coding-agents-bg-cost.webp)

user@sarvam:~/acme/payments-service$ sarvam-code

>_ Coding Agents (v0.38.0)

directory: ~/acme/payments-service

Route each task

› Write the data-layer boilerplate, then review the rollback path. Route each one to whichever model suits it.

  1. Classified  2 task types in this run 

  2. Scaffolding  routed to a fast, lower-cost model 

  3. Rollback review  routed to a reasoning model 

  4. Scaffolding and rollback review went to different models. Coding Agents routed each task separately.  Scaffolding and rollback review went to different models. Coding Agents routed each task separately.




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Show the cost split by task

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 11% used · Distinguished

user@sarvam:~/acme/payments-service$ sarvam-code

>_ Coding Agents (v0.38.0)

directory: ~/acme/payments-service

Finish the migration

› Complete the remaining changes in the migration and report what finished.

  1. Thought  for 2 seconds 

  2. migration complete 214 call sites +612  -188 

  3. Migration complete across 214 call sites. We bill this as completed work.  Migration complete across 214 call sites. We bill this as completed work.




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Summarise the completed work

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/payments-service · Context 54% used · Distinguished

![](https://assets.sarvam.ai/tr:w-1920,q-70,f-auto,dpr-auto/assets/products/coding-agents/pillars/coding-agents-bg-aside.webp)

##  Train a model for a specialised task. 

Coding Agents can train a task-specific model during the run using your data and requirements, then apply it to the job. For underwriting, that can mean training on your risk parameters. 

user@sarvam:~/acme/underwriting$ sarvam-code

>_ Coding Agents (v0.38.0)

directory: ~/acme/underwriting

Train an underwriting model

› Train a task-specific model on our portfolio and risk parameters, then use it for this pricing task.

  1. Thought  for 9 seconds 

  2. Read  risk/params.yaml, historical policies 

  3. Prepared  evaluation holdout 

  4. Training finished this run. The model is ready for your review on this risk band.  Training finished this run. The model is ready for your review on this risk band.

  5. risk/underwriting.model ready for review




─ Flow ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

› Show the evaluation on the held-out band

──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

~/acme/underwriting · Context 4% used · Distinguished

## Frequently Asked Questions

### What is Coding Agents?

Coding Agents are an AI coding agent for engineering teams. Give it a software goal. It makes a plan, writes and tests the change, and prepares the result for review.

### How does Coding Agents handle a long run?

Coding Agents saves checkpoints as it works, then returns to the latest one after a failed test or dead end.

### Can I change the plan while it is running?

Yes. The plan stays visible during the run. You can change the goal, reorder a step, or stop the current approach. Coding Agents continues from the work already completed.

### How is it priced?

Pricing follows completed work. Retries and dead ends are not billed.

### Where does our code and data live?

Your repositories, prompts, and run history stay within Indian jurisdiction.

### How do we get started?

Tell us about your codebase and work that crosses files or services. We will set up a pilot on your repository.

Put Coding Agents to work on a real codebase. 

Put Coding Agents to work on a real codebase.

[Talk to us](https://www.sarvam.ai/contact-us)
