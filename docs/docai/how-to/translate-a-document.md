---
url: https://docs.sarvam.ai/docai/how-to/translate-a-document/
title: Translate a document | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:02.373254+00:00
---

# Translate a document | Sarvam API Docs

> Source: https://docs.sarvam.ai/docai/how-to/translate-a-document/

Skip to navigation

On this page

  * Step 1: Open the Translate page
  * Step 2: Start a new translation project
  * Step 3: Add or manage target languages
  * Step 4: Track progress per language
  * Step 5: Review in the side-by-side editor
  * Step 6: Use the side-panel tools
  * Step 7: Export



Scroll to top

[How-to](https://docs.sarvam.ai/docai/how-to/extract-fields-from-a-document/extract-structured-fields)

# Translate a document

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/docai/how-to/translate-a-document.md "View this page as plain text")|More actions

This page is for Doc Agents.

**Translate** renders a whole document into one or more languages while preserving its structure: headings, paragraphs, images, and layout all stay in place. You then review and refine each translation in a rich side-by-side editor with AI assistance, learned rules, and document-level guidelines.

This guide walks through the full flow: open Translate, start a new translation project, add target languages, refine in the editor, and export.

## Step 1: Open the Translate page

Click **Translate** under **Products** in the sidebar. The **Document Translation** page lists every translation in your workspace with columns for **Document name** , **Language** , **Genre** , **Created on** , **Status** , and **Actions**. Use the search bar to find one quickly.

![Document Translation list showing documents with Document name, Language, Genre, Created on, Status, and Actions columns, plus a New translation button.](https://docs.sarvam.ai/_fern-img/665e4f047d02e041642c63263c504867d28d9fdd0b87cf0e0db79c8797313ca1.webp)

The Document Translation list: each document with its language, genre, and status.

## Step 2: Start a new translation project

Click **\+ New translation** to open the **New translation project** dialog. Upload your document and set up the project.

[1](https://docs.sarvam.ai/docai/how-to/translate-a-document#upload-the-source-document)

### Upload the source document

**PDF** , **Word** (`.doc`, `.docx`, `.odt`), **spreadsheets** (`.xls`, `.xlsx`, `.ods`), **presentations** (`.ppt`, `.pptx`, `.odp`), and **web pages** (`.html`, `.xhtml`, `.mhtml`), up to **300 MB** and **500 pages**.

[2](https://docs.sarvam.ai/docai/how-to/translate-a-document#name-the-project)

### Name the project

**Project name.** A short identifier, e.g. _HBS case study Q2_.

[3](https://docs.sarvam.ai/docai/how-to/translate-a-document#set-the-source-language)

### Set the source language

**From.** The source language of the document.

[4](https://docs.sarvam.ai/docai/how-to/translate-a-document#pick-a-genre)

### Pick a genre

**Genre.** Sets the tone and vocabulary the model uses (General, Children Fiction, and more).

[5](https://docs.sarvam.ai/docai/how-to/translate-a-document#choose-target-languages)

### Choose target languages

**Target.** Search and select one or more languages to translate into.

[6](https://docs.sarvam.ai/docai/how-to/translate-a-document#add-guidelines-optional)

### Add guidelines (optional)

**Translation guidelines.** Optionally add document-level rules up front (tone, terminology, do-not-translate terms).

![New translation project dialog with an upload zone \(PDF, Word, spreadsheet, and presentation formats up to 300 MB, up to 500 pages\), Project name, From, Genre, Target language search, and Translation guidelines fields.](https://docs.sarvam.ai/_fern-img/6da539b36b57c8a13172d45d71dcc5f45dabe4c9af3df779611eff0db7202dcd.webp)

New translation project: upload, name, source language, genre, target languages, and guidelines.

Click **Start translation →** to kick off the project.

## Step 3: Add or manage target languages

A single document can be translated into many languages. From the document’s detail view, click **Add Language** to pick from the full set of supported languages: Assamese, Bodo, Dogri, Gujarati, Kannada, Kashmiri, Konkani, Maithili, Malayalam, Manipuri, Marathi, Nepali, and more. Languages already on the document show under **Existing**.

![Add languages modal showing a grid of Indian languages \(Assamese, Bodo, Dogri, Gujarati, Kannada, Kashmiri, and more\) with Existing languages Bengali and English listed at the bottom.](https://docs.sarvam.ai/_fern-img/910210831bb1a5dbf7ffbe26676e53e29bf1d9704d675b98dad1ae47d5c8deb0.webp)

Add languages: pick one or more target languages for the document.

## Step 4: Track progress per language

The document detail view shows the source (with its genre and page count), plus a **Translations** section with one card per target language. Each card shows a status and a progress bar (for example _Bengali, Not started, 0%_ and _English, Complete, 100%_). Use **View Original** or **Download Original** to work with the source, and **Edit Guidelines** to update rules that apply across every language.

![Document Translation detail view for a Hindi source tagged Children Fiction and 5 Pages, with a Translations section showing Bengali at 0% Not started and English at 100% Complete, plus an Add Language card.](https://docs.sarvam.ai/_fern-img/77903f7dc524d2dda4f3be5b25f3f12eacdb69a03c7e7e5c8a14c569c1ae100d.webp)

Document detail: source on top, per-language translation cards with progress below.

## Step 5: Review in the side-by-side editor

Open a translation to enter the editor. The **source** sits on the left and the **translation** on the right, with a language selector at the top so you can switch between target languages. A page selector (`< 1 of N >`) moves through the document. Three actions live in the toolbar:

  * **Changes** shows your edit history for the document.
  * **Edit Guidelines** opens the document-level translation rules.
  * **Bulk Translate** re-runs the translation across the whole document, applying your latest guidelines and learned rules.



![Translate editor with the Hindi source on the left and the English translation on the right, a language selector at the top, Changes, Edit Guidelines, Bulk Translate, and Export buttons, and page navigation showing 1 of 5.](https://docs.sarvam.ai/_fern-img/d79d7389b8494058793810cbe80efdf420882a93a765bf007503fa7b13003821.webp)

The Translate editor: source on the left, translation on the right, with images and layout preserved.

## Step 6: Use the side-panel tools

The right rail has three tools:

  * **AI Assistance.** Ask questions about the content (_“what is the moral of the story”_) and get answers grounded in the document.
  * **Learned Rules.** Corrections you make are remembered and reapplied across the document, so you fix a term or phrasing once.
  * **Editor Settings.** Toggle **Transliteration** (type English, get Indic suggestions), **Spell Check** (target-language dictionary), and **Editor Stats** (word / character / reading-time counts); set **Font Size** (S / M / L); and choose a **Panel Layout** (50-50, 40-60, or 30-70 split, or drag the divider).



## Step 7: Export

When a translation reads the way you want, click **Export** in the editor toolbar. Pick a format from the dialog and click **Download** :

  * **DOCX** (Microsoft Word)
  * **PDF** (Portable Document)
  * **HTML** (Web page)
  * **EPUB** (E-book format)
  * **TXT** (Plain text)



![Export translation dialog with Format options DOCX, PDF, HTML, EPUB, and TXT, and a Download button.](https://docs.sarvam.ai/_fern-img/2b96a6c77b5371b7d08d993ee801ea930de7ef9300ccf010dcddf8af67bdec42.webp)

Export translation: choose DOCX, PDF, HTML, EPUB, or TXT.

For a multi-language deliverable (say, the same story in Bengali and English), add both target languages to one document. Each gets its own editor and progress bar, all tracked under the same source.

Next: [FAQs](https://docs.sarvam.ai/docai/resources/faq) · [Document Translation API](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/docai/how-to/digitise-a-document)[FAQsNext](https://docs.sarvam.ai/docai/resources/faq)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

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


