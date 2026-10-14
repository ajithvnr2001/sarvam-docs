---
url: https://docs.sarvam.ai/docai/extract-as-csv-excel/
title: Extract as CSV/Excel | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:01.404213+00:00
---

# Extract as CSV/Excel | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/extract-as-csv-excel/

Skip to navigation

On this page

  * Step 1: Run the project
  * Step 2: Review in the editor pane
  * Edit tables in the Table Editor
  * Step 3: Download as CSV, Excel, or JSON
  * Handling tricky tables
  * Batch processing many documents



Scroll to top

[How-to](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)[Extract fields from a document](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)

# Extract as CSV/Excel

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/extract-as-csv-excel.md "View this page as plain text")|More actions

This page is for Doc Agents.

Turn table-heavy PDFs (receipts, invoices, bank statements, expense sheets, GST filings) into spreadsheet-ready **CSV** , **Excel (XLSX)** , or structured **JSON**.

You’ll need an **Extract** Config that describes the tabular fields you want. If you don’t have one yet, see [How to Create a Config](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config), then come back here.

## Step 1: Run the project

[1](https://docs.sarvam.ai/docai/extract-as-csv-excel#open-extract)

### Open Extract

Click **Extract** under **Products** in the sidebar.

[2](https://docs.sarvam.ai/docai/extract-as-csv-excel#kick-off-a-new-project)

### Kick off a new project

Click **Extract** next to your Config, or click **Upload documents** and pick your file.

[3](https://docs.sarvam.ai/docai/extract-as-csv-excel#give-the-project-a-name)

### Give the project a name

Something like _Bank Statement May-Q2_ to make it easy to spot in the Projects list.

[4](https://docs.sarvam.ai/docai/extract-as-csv-excel#start-extract)

### Start Extract

Click **Extract**. Status progresses **Draft → Processing → Completed** (or **Failed** if something goes wrong).

## Step 2: Review in the editor pane

Once the project shows **Completed** , click it to jump straight into the editor pane. The source document sits on the left and the extracted tables appear as a hierarchical **Output** panel on the right. Every row expands to show its fields, and every field carries a per-field confidence score and a source-page reference.

![Extract results view for a credit card statement showing the source PDF on the left and a Transactions Output panel on the right with expanded transaction items \(date, description, amount, type\) and per-field confidence scores.](https://docs.sarvam.ai/_fern-img/78375108a2c85718992b8fa3af0173db5e2347089044efdd56cbeabaaf7e38f2.webp)

Credit-card statement extraction: source PDF on the left, expandable Transactions with per-field confidence on the right.

For a bank statement, you might see something like:

Date| Description| Amount| Type  
---|---|---|---  
02/04/2020| UPI Payment Received| 100000| credit  
26/03/2020| LOGIN AND PAY WITH AMA BANGALORE IN| 4923.98| debit  
18/03/2020| AMAZON PURCHASE IN| 2347.98| debit  
  
Low-confidence values (e.g. `48%`) are highlighted so you can spot-review them quickly.

### Edit tables in the Table Editor

Double-click any table in the results to open the dedicated **Table Editor**. It puts the source-table image on the left and an editable grid on the right, so you can fix cells without losing the surrounding page context.

![Table editor showing a source-table image on the left and an editable grid of extracted bank transaction rows on the right, with Image Zoom, Close, and Save Changes controls.](https://docs.sarvam.ai/_fern-img/204483bcb931fecc1ab9f5d51df926ba681dd851776394c058d2360231165a0f.webp)

The Table Editor: source-table preview on the left, editable grid on the right.

Inside the Table Editor you can zoom the source preview with the **Image Zoom** dropdown, click any cell to edit its value, add or delete rows with the `+` and trash icons, then click **Save Changes** to commit (or **Close** to discard).

## Step 3: Download as CSV, Excel, or JSON

Click **Download** to open the export dialog and pick your **Format** from the dropdown.

![Extract Download dialog with the Format dropdown open showing JSON, CSV, and Excel \(XLSX\) options; Excel \(XLSX\) is currently selected.](https://docs.sarvam.ai/_fern-img/bc013b50619a5d6e1c7b44ec577beebf5af8bc269a7a9c32d18ff85cd9a3df66.webp)

Extract Download dialog: pick JSON, CSV, or Excel (XLSX) from the Format dropdown.

CSV

Single-file, one-row-per-transaction. Best for pandas, SQL loading, or a spreadsheet tool.

Excel (XLSX)

Native Excel format with headers and cell formatting preserved.

JSON

Structured JSON, preserving nested groups and arrays. Best for feeding another system natively.

Confirm to save the file.

## Handling tricky tables

###### Merged or spanning cells

Ask the Extract description to un-merge them:
    
    
    When a cell spans multiple rows, repeat the value across the child rows.

Sarvam normalises the output for you.

###### Multi-line descriptions

Bank-statement descriptions often wrap. Sarvam consolidates wrapped lines into a single row by default. To keep them split, add:
    
    
    Preserve each line of the description as a separate row.

###### Multiple tables on one page

Sarvam detects each distinct table. In **Excel** output, each becomes its own sheet. In **CSV** , tables are separated by a blank row. Split on blank rows in your loader.

###### Numeric formatting (₹ 1,24,500)

Currency symbols and thousands separators are kept as-is unless you ask otherwise. Add:
    
    
    Return amounts as plain numbers without currency symbols or commas.

## Batch processing many documents

Two approaches, depending on how many similar documents you have:

Run one project per document

Best when you want each document’s rows in its own file. Every project shows up in **Workspace → Projects** for easy tracking.

Consolidate manually after download

Download CSVs or JSON from multiple projects and concatenate them. One paste per project works because column layouts are identical across runs of the same Config.

Next: [FAQs](https://docs.sarvam.ai/docai/resources/faq).

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)[Create a ConfigNext](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


