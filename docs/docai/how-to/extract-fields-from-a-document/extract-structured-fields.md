---
url: https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields/
title: Extract structured fields | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:02.287935+00:00
---

# Extract structured fields | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields/

Skip to navigation

On this page

  * How it works
  * Step 1: Open Extract and upload your document
  * Step 2: Configure the project
  * Step 3: Review the auto-drafted schema
  * Step 4: Track processing
  * Step 5: Review the results
  * Step 6: Download
  * Handling multi-page documents
  * Improving accuracy



Scroll to top

[How-to](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)[Extract fields from a document](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)

# Extract structured fields

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields.md "View this page as plain text")|More actions

This page is for Doc Agents.

**Extract** pulls specific fields out of a document (invoice numbers, dates, amounts, PAN, GST IDs, rider names, addresses) and returns them as structured data ready to download as JSON, CSV, or Excel.

This guide walks through the full Extract flow: open the Extract page, upload a document, describe what to extract, review the auto-drafted schema, and download the results.

## How it works

Every Extract project follows the same three-step flow.

![Extract New Project dialog showing the three-step flow \(Upload documents, Describe what to extract, Get structured data\) and a dropzone that accepts PDF, JPEG, and PNG files up to 50 MB.](https://docs.sarvam.ai/_fern-img/442a2b68ee447c78733f17471c57043d6294515a5a87e01a46c887f61ee15aa0.webp)

Extract New Project dialog: three-step flow on the left, upload dropzone on the right.

[1](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#upload-documents)

### Upload documents

Drag and drop **PDF, JPEG, or PNG** files, up to **50 MB per file** and **10 pages per project**.

[2](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#describe-what-to-extract)

### Describe what to extract

Write a plain-English prompt for the fields you want. Sarvam auto-drafts a schema from it.

[3](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#get-structured-data)

### Get structured data

Review the results with per-field confidence, then download as JSON, CSV, or Excel.

## Step 1: Open Extract and upload your document

Click **Extract** under **Products** in the sidebar. The **Extract from Documents** page shows an upload area and a shelf of Extract templates you can start from. Click **Upload files** (or click a template to prefill its settings) and drop in your file.

![Extract from Documents page with an Upload files button and a row of Extract templates including Insurance Claim Form Extraction, Court Appeal Information Extraction, and Historic Land Deed Extraction.](https://docs.sarvam.ai/_fern-img/c190e87b9ef9ca642064bda751232a7846f75af5399251d7d440b03134aba3bd.webp)

The Extract from Documents landing page: Upload files button and a template shelf.

Supported formats: **PDF, JPEG, PNG**. Limits: **50 MB per file** , **10 pages per project**. To process more than 10 pages, use our [API](https://docs.sarvam.ai/api-reference/doc-ai/job/extract), and batch your requests at 10 pages per batch.

## Step 2: Configure the project

Once the file uploads, the dialog shows a preview of your document on the left and three fields on the right.

![Extract configuration panel with a Credit Card Statement preview on the left and Project name, Describe what to extract, and Output format fields on the right.](https://docs.sarvam.ai/_fern-img/817cb0f7332bd94aa6ad8c157893b40c28979657f4a7cfe6e182abd848a7dd59.webp)

Configuring an Extract project: document preview on the left, Project name / Describe what to extract / Output format on the right.

[1](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#name-the-project)

### Name the project

**Project name.** A short identifier like _Credit Receipt_ or _Invoice batch May-Q2_. Shows up in the Projects list.

[2](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#describe-what-to-extract-1)

### Describe what to extract

**Describe what to extract.** A plain-English prompt describing the fields you want. Copy and paste one of these into **Describe what to extract** , then edit for your document:
    
    
    Extract the transactions with the highest amounts.

[3](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#pick-an-output-format)

### Pick an output format

**Output format.** Leave on **Generate from prompt** to let Sarvam auto-draft the schema, or pick a specific format.

[4](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#continue)

### Continue

Click **Extract →** to move on to the schema.

The extraction prompt is exactly that: a prompt. The more specific it is, the better the result. Copy one of these into **Describe what to extract** and adjust for your document:
    
    
    Weak: Get the fields.
    
    Better: Extract rider name, trip date, trip time, total amount, and currency from the Uber receipt.
    
    Best: Extract rider name, trip date (Jun 4, 2026 format), trip time (24-hour), total amount as a number, and the currency symbol. Also include the fare breakdown and payment details if visible.

## Step 3: Review the auto-drafted schema

If **Output format = Generate from prompt** , Sarvam opens a **Define your output format** dialog before running the extraction. It contains an AI-drafted schema you can inspect and edit. The dialog has two tabs.

###### Schema tab

###### JSON tab

A visual, expandable view of every field the AI proposes. Each field has a **type** dropdown (`string`, `number`, `object`, `array of objects`, `date`, and more). Objects and arrays reveal nested fields underneath. Add fields with **\+ Add field** or **\+ Add nested field** ; delete with the `×`.

![Define your output format dialog on the Schema tab, showing an AI-drafted schema with nested objects \(report_metadata, key_features\) and typed fields \(string, array of objects\).](https://docs.sarvam.ai/_fern-img/afc02ac6f97d7be7380baad85fb3065da6ec093090df080d8315a853bbb01dab.webp)

Define your output format, Schema tab: nested fields with type dropdowns, Regenerate and Clear all controls.

[1](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#refine-or-regenerate)

### Refine or regenerate

Edit the prompt on the left, click **Regenerate** to have Sarvam re-draft. Or **Clear all** to wipe the schema and start from an empty structure.

[2](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#tweak-types-and-nesting)

### Tweak types and nesting

On the Schema tab, change field types (`string` to `date` or `number`), add or remove fields, and nest objects and arrays as your downstream system expects.

[3](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields#run-the-extraction)

### Run the extraction

Once the schema looks right, click **Looks good, run extraction →**. The project starts running.

The auto-drafted schema is a starting point, not a lock-in. A Config saved with a good schema is worth building once and reusing everywhere.

## Step 4: Track processing

Your project appears in the list with a status that flows through:

  * **Draft.** Project created but not yet submitted, for example if you closed the Extract dialog without confirming the schema.
  * **Processing.** The Vision model is reading the pages and locating your fields.
  * **Completed.** Ready to review. A notification also appears on the Home dashboard.
  * **Failed.** Something went wrong. Open the project’s `⋯` menu to retry or delete.



Most single-page receipts and invoices finish in a few seconds. Multi-page PDFs take proportionally longer.

## Step 5: Review the results

Click the project to open the results view. The source document sits on the left, and a hierarchical **Output** panel sits on the right. For documents like bank statements, the Output panel expands to show every transaction row with its own set of fields (date, description, amount, type), each carrying its own confidence score and source-page reference.

![Extract results view for a credit card statement showing the source PDF on the left and a Transactions Output panel on the right with expanded transaction items \(date, description, amount, type\) and per-field confidence scores.](https://docs.sarvam.ai/_fern-img/78375108a2c85718992b8fa3af0173db5e2347089044efdd56cbeabaaf7e38f2.webp)

Complex output: a credit-card statement with multiple transactions, each row expanded to show date, description, amount, and type with per-field confidence.

The **Output** panel groups extracted values by the top-level objects in your schema (e.g. **Statement Summary** , **Credit Summary** , **Transactions**). For every field you get:

The value

The extracted string, number, date, list, or nested object. Fields that weren’t found in the document appear as a dash.

Confidence

A per-field score (e.g. `97%`) showing how sure Sarvam is about the value.

Groups & arrays

Object groups collapse and expand. Arrays show an item count (e.g. _Transactions, 1 item_) and expand to individual entries.

Click any value to correct it inline before downloading. Corrections apply to the exported file; the source document stays untouched.

## Step 6: Download

Click **Download** to open the export dialog. Choose your format:

JSON

Structured output keyed by your schema. Preserves nested objects and arrays exactly. Best for feeding into another system.

CSV

Flattened one-row-per-project layout. Great for consolidating many extractions into a single spreadsheet.

Excel (XLSX)

Native Excel workbook with formatting preserved.

Confirm to save the file to your computer.

## Handling multi-page documents

Multi-page PDFs are processed page-by-page and fields are consolidated into one Output panel. A page selector on the source pane (`< 1/N >`) lets you spot-check individual pages against the extracted values. Larger documents take longer to process but the flow is identical.

Each upload is capped at **50 MB per file** and **10 pages per project**. For longer PDFs, split into 10-page batches on your computer before uploading, then consolidate the results after export.

## Improving accuracy

###### Write a specific extraction prompt

 _“Total amount”_ is vague. _“Numeric total at the bottom of the invoice, after taxes, in INR”_ is not. The prompt drives both the auto-drafted schema and the extraction. Treat it like a prompt to the model, because it is.

###### Tune the schema before running

The auto-drafted schema often over- or under-specifies. Add missing fields, remove ones you don’t need, tighten types (change `string` to `date` or `number` where appropriate). Better schema in equals better output out.

###### Save common wording as a Config

Once you’ve dialed in a great prompt and schema, save it as a Config. Everyone in the workspace picks up the same wording, so accuracy stays consistent across teammates.

###### Improve the source image

Blurry or skewed scans hurt accuracy more than any prompt change. Re-scan at 300 DPI and straighten before uploading if you can.

Next: [Extract as CSV/Excel](https://docs.sarvam.ai/docai/extract-as-csv-excel).

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/docai/getting-started/overview)[Extract as CSV/ExcelNext](https://docs.sarvam.ai/docai/extract-as-csv-excel)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Overview](https://docs.sarvam.ai/docai/getting-started/overview)
  * How-to

    * Extract fields from a document
      * [Extract structured fields](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)
      * [Extract as CSV/Excel](https://docs.sarvam.ai/docai/extract-as-csv-excel)
      * [Create a reusable config](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)

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


