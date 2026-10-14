---
url: https://docs.sarvam.ai/docai/how-to/digitise-a-document/
title: Digitise a document | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:01.573887+00:00
---

# Digitise a document | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/how-to/digitise-a-document/

Skip to navigation

On this page

  * How it works
  * Step 1: Open Digitise and upload your document
  * Step 2: Configure the project
  * Step 3: Track processing
  * Step 4: Review and edit the output
  * Editor layout
  * The Sections and Digitised text tabs
  * Section types
  * Editing tables with the Table Editor
  * Add missing regions with Add boxes
  * Navigate multi-page documents
  * View the underlying Config
  * Step 5: Download
  * Feeding clean output into an LLM or RAG pipeline



Scroll to top

[How-to](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)

# Digitise a document

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/how-to/digitise-a-document.md "View this page as plain text")|More actions

This page is for Doc Agents.

**Digitise** converts a whole document (a printed page, a handwritten form, a scanned book, a historic manuscript) into clean, structured text. Headlines, section titles, paragraphs, tables, and images are all identified and preserved, so the output is ready for LLMs, RAG pipelines, publishing, or archives.

Digitise is not only for scans. Its typical use cases include:

Modern printed documents

Reports, product briefs, statements, and multi-page PDFs.

Handwritten forms and notes

Patient notes, insurance forms, application submissions, personal letters.

Land deeds and legal records

Property titles, government registration papers, and legal filings, often in regional scripts.

Historic and multilingual archives

19th-century manuscripts, Gujarati / Bengali / Tamil colonial-era records, court files, and out-of-print books.

## How it works

Every Digitise project follows the same three-step flow.

![New Project dialog on Doc Agents showing the three-step Digitise flow](https://docs.sarvam.ai/_fern-img/368dbe3396b9d45c5e7189eb869746c8d7ea9b1807e50637d59fe7f4b35bdcdd.webp)

The Digitise "New Project" dialog: Upload, Digitise, Edit & Export.

[1](https://docs.sarvam.ai/docai/how-to/digitise-a-document#upload-documents)

### Upload documents

Drag and drop or click to upload **PDF, JPEG, or PNG** files, up to **50 MB per file** and **10 pages per project**.

[2](https://docs.sarvam.ai/docai/how-to/digitise-a-document#sarvam-digitises-every-page)

### Sarvam digitises every page

Each page becomes accurate structured text with headings, section titles, paragraphs, tables, and reading order preserved.

[3](https://docs.sarvam.ai/docai/how-to/digitise-a-document#edit-and-export)

### Edit and export

Review side-by-side with the source, tweak anything by hand, and download as HTML, Markdown, DOCX, or Plain Text.

## Step 1: Open Digitise and upload your document

Click **Digitise** under **Products** in the sidebar. The Digitise page shows your Digitise configs and recent Digitise projects. Click **Upload files** , select your document in the file picker, and click **Open**.

Supported formats: **PDF, JPEG, PNG**. Limits: **50 MB per file** , **10 pages per project**. To process more than 10 pages, use our [API](https://docs.sarvam.ai/api-reference/doc-ai/job/extract), and batch your requests at 10 pages per batch.

Three ready-made Digitise templates ship out of the box under **Workspace → Configs → Templates → Digitise** :

  * **Land Deeds Digitisation** for property registration papers and legal records.
  * **Digitise Handwritten Document** for scanned handwritten forms, patient notes, and letters.
  * **Digitise Historic Gujarati Document** for regional-language historic manuscripts.



Duplicate any template into your own Config and tweak language or document format as needed.

## Step 2: Configure the project

Once the file uploads, the New Project dialog shows a preview of your document on the left and three fields on the right.

![Digitise New Project dialog with the Document language dropdown open, showing Hindi, English \(selected\), Bengali, Gujarati, and Kannada, plus a search field. Document format is set to Printed.](https://docs.sarvam.ai/_fern-img/fdddddd2f21c77448e308bb6095a5f3d6d2d369482481abb77a372e3fdc79515.webp)

Configuring a Digitise project: Project name, Document format, Document language (searchable dropdown).

[1](https://docs.sarvam.ai/docai/how-to/digitise-a-document#name-the-project)

### Name the project

**Project name.** A short identifier like _Test 1_ , _Court ruling 1987_ , or _Gujarati Land Deed 22-A_. Shows up in the Projects list.

[2](https://docs.sarvam.ai/docai/how-to/digitise-a-document#pick-the-document-format)

### Pick the document format

**Document format.** Choose the option that matches the source: **Printed** for typeset books, statements, and product reports; **Handwritten** for handwritten forms, manuscripts, and personal notes; or **Mixed (handwritten & printed)** for forms with typed labels and handwritten answers.

[3](https://docs.sarvam.ai/docai/how-to/digitise-a-document#choose-the-document-language)

### Choose the document language

**Document language.** Pick the primary language from the searchable dropdown: **English, Hindi, Bengali, Gujarati, Kannada** , and other supported languages. Sarvam Vision has SOTA accuracy on 22 Indian languages plus English.

[4](https://docs.sarvam.ai/docai/how-to/digitise-a-document#start-the-project)

### Start the project

Click **Digitise →** to run the project.

## Step 3: Track processing

The project appears in your list and progresses through **Draft → Processing → Completed** (or **Failed** if something went wrong). A _“Project submitted, we’ll notify you when it’s ready”_ toast confirms the run. Single-page documents typically finish in seconds; long PDFs take proportionally longer.

## Step 4: Review and edit the output

Click the project to open the editor.

![Digitise editor showing a redacted credit-card statement with 77 detected sections and color-coded bounding boxes](https://docs.sarvam.ai/_fern-img/ab7099f13208d7f6eb4164b750f592ce727984443c15b36dc6c3d30c2e3bef51.webp)

The Digitise editor: source on the left with bounding boxes, Sections list on the right.

### Editor layout

Source pane (left)

Your document rendered at full resolution with **color-coded bounding boxes** on every detected element (headers, paragraphs, images, tables, footnotes). Zoom is controlled from the pane’s zoom dropdown (defaults to `100%`).

Sections pane (right)

Every detected element as a numbered card, ordered top-to-bottom. Each card has a **type dropdown** and the extracted content underneath. Tables render inline with the data preserved.

### The Sections and Digitised text tabs

The right pane has two tabs:

###### Sections (default)

###### Digitised text

Numbered, editable list of every element Sarvam detected. Each section has:

  * A **type dropdown** to reclassify by picking from the list of section types (see below).
  * The **content**. Click to edit inline. Text sections edit as plain text; **Table** sections render as a proper grid and are editable cell-by-cell.



### Section types

Sarvam classifies every detected region into one of the following types. Change the type on any section with the type dropdown, or use it when drawing a new box (see below).

Type| Typical content  
---|---  
`headline`| Document title  
`sub-headline`| Secondary title  
`section-title`| Section heading  
`header`| Page or column header  
`paragraph`| Body text  
`footer`| Page footer  
`footnote`| Note referenced from body text  
`page-number`| Folio / page number  
`table`| Tabular data  
`image`| Figure or graphic  
`image-caption`| Caption under an image  
`photograph`| Photographic content  
`chart` / `diagram`| Charts and diagrams  
`advertisement`| Ad blocks  
`folio`| Book folio marker  
  
### Editing tables with the Table Editor

**Double-click any table on the right pane** (the rendered grid inside its Table section) to open the dedicated **Table Editor** modal. It’s the fastest way to review and fix a tabular region without losing the surrounding page context.

![Table Editor modal with a small source-table image on the left and an editable grid of bank transaction rows on the right. Toolbar shows Image Zoom 90%, Close, and Save Changes controls.](https://docs.sarvam.ai/_fern-img/204483bcb931fecc1ab9f5d51df926ba681dd851776394c058d2360231165a0f.webp)

Table Editor: source-table preview on the left, editable grid on the right.

[1](https://docs.sarvam.ai/docai/how-to/digitise-a-document#zoom-the-source-preview-if-needed)

### Zoom the source preview if needed

Use the **Image Zoom** dropdown (90%, 75%, and other steps) on the toolbar to verify values against dense statements.

[2](https://docs.sarvam.ai/docai/how-to/digitise-a-document#edit-cells-inline)

### Edit cells inline

Click any cell to edit its value directly. Number, date, and text cells all accept free-form input.

[3](https://docs.sarvam.ai/docai/how-to/digitise-a-document#add-or-delete-rows)

### Add or delete rows

Hover any cell to reveal the `+` and trash icons for adding or removing rows.

[4](https://docs.sarvam.ai/docai/how-to/digitise-a-document#click-save-changes)

### Click Save Changes

**Save Changes** commits your edits back to the Sections list and the eventual download. **Close** discards them.

The Table Editor is especially useful for bank statements and invoices where a handful of cells (currency symbols, OCR-misread digits) benefit from a quick human touch-up before export.

### Add missing regions with Add boxes

If Sarvam missed a region (a caption, a footnote, an extra column), you can draw it in.

![Add boxes mode showing the confirm / cancel / label / delete controls on the source pane](https://docs.sarvam.ai/_fern-img/8e6d973aefd0e583b615d8abafb27d0f0428e846e4d566c0e8ed8c34b255f6a0.webp)

Draw mode after clicking Add boxes: pick a Label and confirm.

[1](https://docs.sarvam.ai/docai/how-to/digitise-a-document#enter-draw-mode)

### Enter draw mode

Click **\+ Add boxes** on the source pane.

[2](https://docs.sarvam.ai/docai/how-to/digitise-a-document#draw-a-rectangle)

### Draw a rectangle

Click and drag on the source page to draw a box around the region you want to capture.

[3](https://docs.sarvam.ai/docai/how-to/digitise-a-document#assign-a-label)

### Assign a Label

The bottom bar shows: `✓ × Label:[paragraph ▾] 🗑`. Open the **Label** dropdown to pick the section type. It’s the same list Sarvam uses for auto-detected sections.

[4](https://docs.sarvam.ai/docai/how-to/digitise-a-document#confirm-or-discard)

### Confirm or discard

Click **✓** to add the box (it appears in the Sections list). Click **×** or the trash icon to discard.

Add boxes is available on Digitise projects only. Extract does not use bounding boxes.

### Navigate multi-page documents

For multi-page uploads, use the page selector on the source pane (`< 1/N >`). Each page’s bounding boxes are shown when that page is active; the Sections pane scrolls to the sections belonging to the current page.

The Sections tab shows a running count in its label (e.g. `Sections 77`). That’s the total across every page in the document.

### View the underlying Config

Click **View config** in the editor toolbar to see the Config that drove this project: its Document format, Document language, and any advanced settings. Handy when you’re troubleshooting output that doesn’t match expectations.

## Step 5: Download

When you’re happy with the output, click **Download** in the editor toolbar. Choose your format from the dropdown:

HTML

Preserves rich layout (headings, images, tables, colored spans). Best for publishing to the web or feeding into any HTML-aware tool.

Markdown

Clean, LLM-friendly text with heading levels and tables. Best for RAG pipelines, embedding, and archival.

DOCX

Native Word format. Best when the downstream user will hand-edit the document further.

Plain Text

Flat text without formatting. Best for lightweight indexing and search.

## Feeding clean output into an LLM or RAG pipeline

Digitised structured text is a much better LLM input than raw OCR:

  * **Headings become natural chunk boundaries.** Split on section titles for coherent chunks.
  * **Tables stay parseable.** Sarvam preserves them as tables, not as jumbled words.
  * **Reading order matches expectations.** No column-mixing on multi-column layouts.



If your RAG pipeline currently ingests raw OCR, swap in a Digitise Markdown export and re-measure retrieval quality. Most teams see immediate improvement.

Next: [Extract as CSV/Excel](https://docs.sarvam.ai/docai/extract-as-csv-excel).

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/create-a-reusable-config)[Translate a documentNext](https://docs.sarvam.ai/docai/how-to/translate-a-document)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


