---
url: https://docs.sarvam.ai/docai/resources/faq/
title: FAQs | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:02.738453+00:00
---

# FAQs | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/resources/faq/

Skip to navigation

On this page

  * Still stuck?



Scroll to top

[Resources](https://docs.sarvam.ai/docai/resources/faq)

# FAQs

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/resources/faq.md "View this page as plain text")|More actions

This page is for Doc Agents.

Short answers to the questions we get asked most often. Questions that aren’t already covered in the how-to pages.

###### What's the difference between Extract and Digitise?

  * **Extract** pulls specific structured fields from a document, based on a prompt you write (e.g. _“rider name, trip date, total amount”_) and an AI-drafted schema you review before running. Output is a hierarchical Field / Value view with per-field confidence scores, downloadable as **JSON, CSV, or Excel**.
  * **Digitise** converts the full content of a document into structured text, organised into headlines, section titles, paragraphs, tables, and images. Output is a side-by-side editor with the original page on the left and detected sections on the right, downloadable as **HTML, Markdown, DOCX, or Plain Text**.



**Rule of thumb:** Use Extract when you know which fields you need. Use Digitise when you want the whole document.

###### What's the difference between a Config and a Project?

  * A **Config** is a saved recipe: a name, a description of what to extract (or a document format + language for Digitise), an output format, and sharing settings. Build once, reuse across every document of that type.
  * A **Project** is a single run of a Config against one document, with its own status, results view, and download.



Configs live under **Workspace → Configs**. Projects live under **Workspace → Projects**. A Config’s `Usage` column tells you how many projects have used it.

###### What file formats can I upload, and what are the limits?

  * **Accepted formats:** PDF, JPEG, PNG.
  * **Per-file size:** up to **50 MB**.
  * **Per-project pages:** up to **10 pages** (whether that’s a 10-page PDF or a batch of 10 image files).



If you have an unusual format, check the upload dialog in your workspace for the current list. New formats are added over time.

###### My document has more than 10 pages. How do I process it?

Split the source into 10-page batches on your computer, then upload each batch as its own project against the same Config. After each project completes:

  * **Extract:** download every project’s JSON (or CSV) and concatenate them. Column layouts are identical across runs of the same Config.
  * **Digitise:** download every project’s Markdown (or HTML) and paste them in order.



The 10-page cap applies uniformly across plans; upgrading does not raise it. If you have a genuine single-document requirement beyond 10 pages, reach out to [support](mailto:support@sarvam.ai).

###### Extract returned the wrong value for a field. How do I fix it?

A few things to try, in order:

  1. **Sharpen the extraction prompt.** Copy one of these into **Describe what to extract** :


    
    
    Vague: Total amount
    
    Better: Numeric total at the bottom of the invoice, after taxes, in INR

Treat the prompt like a prompt to the model, because it is. 2\. **Tune the schema before running.** The AI-drafted schema in the _Define your output format_ dialog is a starting point. Change field types (`string` to `date` or `number`), remove noise fields, or add nested structure where the document has it. 3\. **Correct inline before export.** Click into the field on the results view and fix the value. The correction is baked into the download. 4\. **Improve the source.** Blurry or skewed scans hurt accuracy more than any prompt change. Re-scan at 300 DPI and straighten before uploading if you can.

###### How much does a project cost?

To learn more about project costs, visit [Sarvam pricing](https://indus.sarvam.ai/pricing).

###### What do the different project statuses mean?

A project moves through up to four states, visible on **Workspace → Projects** and the **Home** dashboard:

Status| Meaning  
---|---  
**Draft**|  Project created but not submitted. Usually because the New Project dialog was closed before confirming (e.g. the schema in _Define your output format_ was never approved). Reopen the project to resume.  
**Processing**|  The Vision model is actively reading the document. Most single-page runs finish in a few seconds; long PDFs take proportionally longer.  
**Completed**|  Ready to review. A _“[project name] is ready”_ notification also appears on Home.  
**Failed**|  Something went wrong (unsupported file, corrupted upload, timeout). Open the project’s `⋯` menu to retry or delete.  
  
Filter by status using the **All statuses** pill on the Projects page.

## Still stuck?

[Email supportReach out directly at support@sarvam.ai.](mailto:support@sarvam.ai)[Join our DiscordEarly access to new releases, biweekly challenges, office hours with the team, and India’s AI builder community.](https://discord.com/invite/5rAsykttcs)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/docai/how-to/translate-a-document)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/docai/getting-started/overview)
  * How-to

    * Extract fields from a document

    * [Digitise a document](https://docs.sarvam.ai/docai/how-to/digitise-a-document)
    * [Translate a document](https://docs.sarvam.ai/docai/how-to/translate-a-document)
  * Resources

    * [Frequently Asked Questions](https://docs.sarvam.ai/docai/resources/faq)
    * [Data retention](https://docs.sarvam.ai/api/platform/data-retention "Data retention")



  * [Overview](https://docs.sarvam.ai/docai/getting-started/overview)
  * [Extract structured fields](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)
  * [Extract as CSV/Excel](https://docs.sarvam.ai/docai/extract-as-csv-excel)
  * [Create a reusable config](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)
  * [Digitise a document](https://docs.sarvam.ai/docai/how-to/digitise-a-document)
  * [Translate a document](https://docs.sarvam.ai/docai/how-to/translate-a-document)
  * [Frequently Asked Questions](https://docs.sarvam.ai/docai/resources/faq)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


