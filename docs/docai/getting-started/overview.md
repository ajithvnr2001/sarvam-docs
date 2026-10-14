---
url: https://docs.sarvam.ai/docai/getting-started/overview/
title: Welcome to Doc Agents | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:02.843932+00:00
---

# Welcome to Doc Agents | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/getting-started/overview/

Skip to navigation

On this page

  * What you can do
  * Who it’s for
  * Prerequisites
  * Home Page
  * Products
  * Extract
  * Digitise
  * Translate
  * Extract or Digitise: how to choose
  * Workspace
  * Configs
  * Projects
  * How the flow works
  * Next steps



Scroll to top

[Getting Started](https://docs.sarvam.ai/docai/getting-started/overview)

# Welcome to Doc Agents

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/getting-started/overview.md "View this page as plain text")|More actions

This page is for Doc Agents.

## One workbench. Every document.

Extract, digitise, and translate any document in Hindi, Bengali, Tamil, Telugu, English, and 18 more Indian languages. No code required.

![Doc Agents Home dashboard with quick-start cards for Extract, Digitise, and Translate, a credit balance, and a template shelf.](https://docs.sarvam.ai/_fern-img/69ad5328ac658caa0060df1f12092180c9f8d7238656cd5df1f4d57f131e3666.webp)

The Doc Agents dashboard: Extract, Digitise, and Translate, all in one place.

**Doc Agents** is a document-intelligence workbench for turning real-world documents into data you can use. From BFSI paperwork (invoices, KYC, bank and credit-card statements, insurance claims) to government records (land deeds, licensing forms), legal filings, HR resumes, healthcare intake, printed books, and handwritten multilingual manuscripts, the workbench handles it all. Every workflow is one dashboard click at [dashboard.sarvam.ai](https://dashboard.sarvam.ai/akshar/dashboard). No code required.

Under the hood, **Sarvam Vision** powers extraction and digitisation, and **Sarvam Document Translation** powers whole-document translation — all with SOTA accuracy on **22 Indian languages plus English**.

### What you can do

Extract fields as structured data

Pull invoice numbers, PAN, dates, amounts, and line-items from any document type as JSON, CSV, or Excel.

Digitise whole documents

Convert scans, handwritten forms, land deeds, and historic multilingual manuscripts into structured text, Markdown, HTML, or DOCX.

Translate whole documents

Translate PDFs, Word files, and more into Indian languages while preserving layout, then refine in a side-by-side editor.

Export as CSV or Excel

Turn table-heavy PDFs such as bank statements and invoices into spreadsheet-ready CSV or Excel output.

Build reusable Configs

Save every workflow as a Config. Share with your team. Re-run against thousands of documents with one click.

## Who it’s for

Built for anyone whose day-to-day involves documents:

  * **BFSI teams** processing invoices, KYC, bank and credit-card statements, GST filings, and insurance claims at scale.
  * **Analysts** turning scanned reports and statements into Excel-ready data for pandas, SQL, or dashboards.
  * **Developers** wiring document extraction into product flows, back-office pipelines, and RAG systems.
  * **Legal, compliance, and government teams** working with land deeds, court records, licensing forms, and notarised documents.
  * **HR and healthcare teams** parsing resumes, offer letters, patient intake forms, and prescriptions.
  * **Researchers and publishers** digitising historic manuscripts, out-of-print books, and multilingual archives.



## Prerequisites

  * A document to test on: **PDF, JPEG, or PNG** , up to **50 MB per file** and **10 pages per project**
  * Sufficient credits in the workspace



## Home Page

Open [dashboard.sarvam.ai/akshar/dashboard](https://dashboard.sarvam.ai/akshar/dashboard) and sign in. You land on **Home** , which shows your credit balance, quick-start cards for Extract, Digitise, and Translate, and a shelf of ready-made template configs organised by category. The sidebar has three working groups: **Products** (Extract, Digitise, Translate) and **Workspace** (Projects, Configs).

![Doc Agents Home page with quick-start cards for Extract and Digitise, a credit balance, and a template shelf organised by category.](https://docs.sarvam.ai/_fern-img/d4c6a12b0f4108238f81046e661ca11952f5d810de8b2583adcb6875ed077c56.webp)

The Home dashboard: quick-start cards, credit balance, and a shelf of ready-made templates.

## Products

**Products** in the sidebar contains the three things the workbench does:

  * **Extract** pulls specific fields out of a document (invoice numbers, dates, amounts, names) and returns them as structured JSON, CSV, or Excel. You describe what you want in plain English and the workbench drafts a schema for you.
  * **Digitise** converts the whole content of a document into structured text (headlines, paragraphs, tables, images) and exports as HTML, Markdown, DOCX, or Plain Text. Great for scans, handwritten forms, land deeds, and historic multilingual manuscripts.
  * **Translate** renders a whole document into one or more languages while preserving layout, then lets you refine each translation in a side-by-side editor with AI assistance and learned rules.



### Extract

**Extract** pulls specific fields out of a document and returns them as structured data: invoice numbers, dates, amounts, PAN, GST IDs, account holders, transaction rows, or whatever fields the document contains.

You describe what you want in plain English (_“rider name, trip date, total amount”_), and the workbench auto-drafts a schema from your prompt. Review and edit the schema (change field types, add nested groups, remove fields you don’t need), then approve and run.

The results view puts the source document on the left and a hierarchical **Output** panel on the right. Every field carries a value, a per-field **confidence score** , and a dash placeholder if the field wasn’t found. Click any value to correct it inline before export.

![Extract results view with an Uber receipt on the left and a hierarchical Output panel with per-field confidence scores on the right.](https://docs.sarvam.ai/_fern-img/ef5c1e0afc78b498ced40e500614e6cda8ff0af8925efc36247ec6f39aadb3f8.webp)

Extract results: source document on the left, hierarchical Output with per-field confidence on the right.

**Great for:** invoices, receipts, KYC forms, bank and credit-card statements, GST filings, insurance claims, purchase orders, resumes, background verifications, loan applications, prescriptions, ID cards, and any document where you already know the fields you need.

**Download as:** JSON, CSV, or Excel (XLSX).

For the full walkthrough see **[How to Extract structured fields](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)**.

### Digitise

**Digitise** converts the whole content of a document into structured text. Headlines, section titles, paragraphs, tables, and images are all identified and preserved.

The editor puts the source page on the left with **color-coded bounding boxes** on every detected region, and a numbered **Sections** list on the right. Each section has a type dropdown, and table sections open in a dedicated **Table Editor** for cell-by-cell fixes. If a region was missed, click **\+ Add boxes** to draw a rectangle and label it from the same list of section types.

The output is clean, machine-readable text with layout preserved, ready to feed into LLMs, RAG pipelines, publishing tools, or archives.

![Digitise editor with a Tamil land deed on the left and the digitised Tamil text on the right, preserving the document's structure.](https://docs.sarvam.ai/_fern-img/e668f46d144c3f10dbce936de074d46b1aabdf983f707b294c67b2bc87e4c224.webp)

Digitise output: a Tamil land deed converted into clean, structured Tamil text.

Every page is broken into typed **Sections** (headers, paragraphs, tables, images, and more), each with color-coded bounding boxes you can review, reclassify, or edit.

![Digitise editor showing a document with color-coded bounding boxes on the left and a numbered Sections list on the right with types like Header and Image, including AI-generated image descriptions.](https://docs.sarvam.ai/_fern-img/7df1a9d3cd2cba1b6809e5a7f00bfe3aaf47142310a3ab86368211e204d4157a.webp)

Detected Sections with color-coded bounding boxes, each with a type you can reclassify or edit.

**Great for:** handwritten forms and notes, land deeds, court records, historic manuscripts, regional-language archives, printed books and journals, contracts, research papers, gazettes, and any document you want as clean text for LLMs, RAG, or publishing.

**Download as:** HTML, Markdown, DOCX, or Plain Text.

For the full walkthrough see **[How to Digitise a document](https://docs.sarvam.ai/docai/how-to/digitise-a-document)**.

### Translate

**Translate** renders a whole document into one or more languages while preserving its structure — headings, paragraphs, images, and layout all stay in place. You then review and refine each translation in a rich side-by-side editor with AI assistance, learned rules, and document-level guidelines.

**Great for:** reports, case studies, books, contracts, marketing collateral, and any document you need in multiple Indian languages without rebuilding the layout.

**Download as:** DOCX, PDF, HTML, EPUB, or TXT.

For the full walkthrough see **[How to Translate a document](https://docs.sarvam.ai/docai/how-to/translate-a-document)**.

### Extract or Digitise: how to choose

Use Extract when…

You know which fields you need. You want structured JSON, CSV, or Excel out. You’re feeding a database, spreadsheet, or business workflow.

Use Digitise when…

You want the whole document. You don’t know in advance what you’ll query. You’re feeding an LLM, publishing, or archiving.

## Workspace

### Configs

A **Config** is a saved recipe: a name, a description of what you want, a language, and an output format. Build once, run against every document of that type. The `Usage` column tells you how many projects have used each Config.

On **Home** , scroll past the Extract and Digitise cards to **Or start with a predefined config**. The template shelf lists **12 ready-made recipes** (9 Extract + 3 Digitise) with filter pills for **All / Extract / Digitise**. Click any card to preview the sample document and the fields it extracts, then start a project in one click.

![Home page showing Or start with a predefined config with All 12, Extract 9, and Digitise 3 filter pills, and template cards for Insurance Claim Form Extraction, Credit Card Statement Extraction, and KYC Document Extraction.](https://docs.sarvam.ai/_fern-img/e0aa72ecb857adbbd6006cd85ec4c1b7ba26e5da4135dbe269e7a1e769e5c943.webp)

Home: "Or start with a predefined config" — the template shelf with Banking and Insurance, Legal, and other categories.

Saved Configs you’ve built also surface on **Home** under **Start with your custom configs** , so your team can kick off a project in one click.

![Home dashboard with Configs highlighted in the sidebar and a Start with your custom configs row showing saved Configs \(Receipt Extraction, Invoice extraction, Story extraction\).](https://docs.sarvam.ai/_fern-img/a9e8f4451cb2a4b41db49294598b85d50cc94e24ab1f62cc01b4455bf0c4842e.webp)

Saved Configs appear on Home under "Start with your custom configs" for one-click reuse.

You can also browse the same templates under **Workspace → Configs → Templates** , duplicate any into your own Config, tweak the prompt or language, and share with your team. Or start from scratch with **\+ New config**. See **[How to Create a Config](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)** for the full walkthrough.

![Configs page with Your configs and Templates tabs, All / Extract / Digitise filter pills, and a Usage column.](https://docs.sarvam.ai/_fern-img/3309ddeaf1ba15e24c196353bbb5200c6b49bed01871aeac05b44c0c592501ee.webp)

Workspace → Configs: Your configs and Templates tabs, with All / Extract / Digitise filter pills and a Usage column.

### Projects

A **Project** is a single run of a Config against one document. It has its own status, results view, and downloads. **Workspace → Projects** lists every project across your organisation, sortable by any column and filterable by **Status** or **Type**.

![Projects page with search bar, All statuses and All types filter pills, and a New project button.](https://docs.sarvam.ai/_fern-img/2a3333dc4909d2a41f51be3072970822ac9193b8d646b7dc850ed6349039e4ed.webp)

Workspace → Projects: search, Status / Type filters, and a New project button.

![Projects pane listing individual project runs with their Config, type, status, and last-updated time.](https://docs.sarvam.ai/_fern-img/8a7bb1b11164eaa15b7cf2b25c2d172fd8f3d225159b5389d1526aa4cfa56bad.webp)

Each row is one project run, with its status and results a click away.

## How the flow works

Every project (Extract or Digitise) follows the same three-step flow.

[1](https://docs.sarvam.ai/docai/getting-started/overview#upload-documents)

### Upload documents

Drag and drop scans, photos, or PDFs. Supported: **PDF, JPEG, PNG** , up to **50 MB per file** and **10 pages per project**.

[2](https://docs.sarvam.ai/docai/getting-started/overview#sarvam-vision-processes-every-page)

### Sarvam Vision processes every page

The model reads each page. For **Extract** , it locates the fields you asked for. For **Digitise** , it converts every page into accurate structured text.

[3](https://docs.sarvam.ai/docai/getting-started/overview#edit-and-export)

### Edit and export

Review the output side-by-side with the source. Fix any values by hand. Download in the format that fits your workflow.

## Next steps

[Extract structured fieldsEnd-to-end walkthrough of an Extract project, including the AI-drafted schema step.](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)[Digitise a documentEnd-to-end walkthrough of a Digitise project, including bounding boxes, section types, and Add boxes.](https://docs.sarvam.ai/docai/how-to/digitise-a-document)[Translate a documentEnd-to-end walkthrough of a Translate project, from upload through side-by-side editing to export.](https://docs.sarvam.ai/docai/how-to/translate-a-document)[Create a ConfigStart from one of the 12 templates or build a custom Config with Name, Pipeline type, Prompt, and Output schema.](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)[Extract as CSV/ExcelTurn table-heavy PDFs (bank statements, invoices) into spreadsheet-ready output.](https://docs.sarvam.ai/docai/extract-as-csv-excel)

Was this page helpful?

YesNo

[Extract structured fieldsNext](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


