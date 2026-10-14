---
url: https://docs.sarvam.ai/api/cookbook/
title: Call Analytics Pipeline | Sarvam API Docs
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:40.163888+00:00
---

# Call Analytics Pipeline | Sarvam API Docs

> Source: https://docs.sarvam.ai/api/cookbook/

Skip to navigation

On this page

  * Overview
  * Business Value
  * How It Works
  * 1\. Prerequisites
  * 2\. Install the SDK and Dependencies
  * 3\. Authentication
  * 4\. The Full Pipeline Script
  * How it works
  * 5\. Sample Output
  * 6\. Tips & Best Practices
  * 7\. Error Handling
  * 8\. Additional Resources
  * 9\. Final Notes



Scroll to top

[Cookbook](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)[Guides](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)

# Call Analytics Pipeline

Ask a question|Copy page|[View as Markdown](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline.md "View this page as plain text")|More actions

This page is for Model APIs.

## **Overview**

This cookbook builds a call analytics pipeline that turns raw call recordings into structured, actionable insights. It uses Sarvam’s **Batch Speech-to-Text Translate API** with speaker diarization to transcribe calls, then uses a **Sarvam chat model** to analyze the conversation, answer follow-up questions, and generate summaries.

**What you’ll build:**

  * A reusable `CallAnalytics` class that goes from raw audio to structured insight with one method call
  * Speaker-wise, diarized transcripts (`*_conversation.txt`) with per-speaker talk-time (`*_timing.json`)
  * An LLM-generated structured analysis of each call, covering customer type, issue, sentiment, and resolution (`*_analysis.txt`)
  * Answers to any custom question you ask across all processed calls
  * A consolidated summary report across all calls (`summary_*.txt`)



### Business Value

  * Improve agent effectiveness
  * Understand customer sentiment
  * Detect operational issues early
  * Spot upsell/cross-sell opportunities
  * Generate real-time dashboards



###### E-commerce / D2C

###### Contact Centers / BPOs

###### Healthcare & Insurance

Understand refund requests, delivery concerns, or dissatisfaction with product quality directly from customer calls.

Sample audio files are available in the [sarvam-ai-cookbook GitHub repo](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/sample_data/call_analytics_audios).

## **How It Works**

Diarization assigns a speaker label to every line of the transcript, which is what makes agent/customer-specific analysis (sentiment, talk-time, resolution tracking) possible in the first place. The pipeline below preserves that speaker structure end-to-end, from raw audio to the final report.

[1](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#transcribe-with-diarization)

### Transcribe with diarization

Upload one or more call recordings to Sarvam’s Batch STT Translate API with `with_diarization=True`. The API transcribes and translates the call to English, tagging each line with a speaker ID.

[2](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#parse-speaker-wise-transcripts)

### Parse speaker-wise transcripts

Convert the raw diarized JSON into a clean `SPEAKER: text` transcript and compute total speaking time per speaker, useful for agent talk-time vs. listening-time monitoring.

[3](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#run-llm-analysis)

### Run LLM analysis

Send the transcript to a Sarvam chat model with a structured analysis prompt to extract customer type, issue, sentiment, resolution, and upsell opportunities.

[4](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#ask-follow-up-questions--summarize)

### Ask follow-up questions & summarize

Query any specific detail across all processed calls, and generate a concise, dashboard-ready summary report.

## **1\. Prerequisites**

  * Python 3.8+
  * A Sarvam API key, sign up on the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/) to get one
  * [FFmpeg](https://ffmpeg.org/download.html) installed and on your `PATH`, required by `pydub` to read and split audio files
  * One or more call recordings (`.mp3`, `.wav`, etc.). You can use the [sample call recording](https://github.com/sarvamai/sarvam-ai-cookbook/blob/main/sample_data/call_analytics_audios/Sample_product_refund.mp3) to follow along



## **2\. Install the SDK and Dependencies**
    
    
    pip install -U sarvamai pydub

`pydub` is used to inspect and split long recordings before transcription. See [The Full Pipeline Script](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#4-the-full-pipeline-script) below. It requires FFmpeg to be installed separately (it is not a Python package).

## **3\. Authentication**

  1. **Obtain your API key** : If you don’t have one, sign up on the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/).
  2. **Set your API key** : Export it as an environment variable, `export SARVAM_API_KEY="your-key-here"` (macOS/Linux) or `setx SARVAM_API_KEY "your-key-here"` (Windows). The [script](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#4-the-full-pipeline-script) below reads it via `os.environ["SARVAM_API_KEY"]`.



Loading the key from an environment variable, instead of hardcoding it, keeps it out of source control. If you’re just experimenting locally, you can instead replace `os.environ["SARVAM_API_KEY"]` with the key as a plain string, but avoid committing that change.

## **4\. The Full Pipeline Script**

Everything below, imports, the 2-hour-file-limit helpers, the `CallAnalytics` class, and the code that runs it end-to-end, lives in one script. Copy it into a single `.py` file as-is:
    
    
    import os
    
    import json
    
    import hashlib
    
    import textwrap
    
    from pathlib import Path
    
    from datetime import datetime
    
    from typing import List, Dict, Optional
    
    from pydub import AudioSegment
    
    from sarvamai import SarvamAI
    
    OUTPUT_DIR = "outputs"
    
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    def split_audio(audio_path: str, chunk_duration_ms: int = 2 * 60 * 60 * 1000) -> List[AudioSegment]:
    
        """Splits a recording into chunks so each fits the Batch API's 2-hour-per-file limit."""
    
        audio = AudioSegment.from_file(audio_path)
    
        return [audio[i:i + chunk_duration_ms] for i in range(0, len(audio), chunk_duration_ms)] if len(audio) > chunk_duration_ms else [audio]
    
    def prepare_audio_paths(audio_path: str) -> List[str]:
    
        """Splits and exports a recording longer than 2 hours; returns the original path unchanged otherwise."""
    
        chunks = split_audio(audio_path)
    
        if len(chunks) == 1:
    
            return [audio_path]
    
        paths = []
    
        for i, chunk in enumerate(chunks):
    
            chunk_path = f"{OUTPUT_DIR}/{Path(audio_path).stem}_part{i + 1}.mp3"
    
            chunk.export(chunk_path, format="mp3")
    
            paths.append(chunk_path)
    
        return paths
    
    ANALYSIS_PROMPT_TEMPLATE = """
    
    Analyze this call transcription thoroughly from start to finish.
    
    TRANSCRIPTION:
    
    {transcription}
    
    Please answer the following:
    
    1. Identify which speaker is the **customer** and which one is the **agent**.
    
    2. Determine if the customer is a **new/potential customer** or an **existing customer**.
    
    3. What **problem, query, or doubt** did the customer raise at the beginning?
    
    4. What **services/products** was the customer inquiring about or facing issues with?
    
    5. How did the agent respond to and resolve the issue throughout the call?
    
    6. Was the **customer satisfied** at the end of the call?
    
    7. Did the customer express any **emotions or sentiments** (positive, negative, or neutral)?
    
    8. Were there any mentions of **competitors**, or any opportunities for **upselling or cross-selling**?
    
    9. Summarize the **resolution** and whether it was successful.
    
    Provide your answer in a clear, structured format with section headings and bullet points.
    
    """
    
    SUMMARY_PROMPT_TEMPLATE = """
    
    Based on this call analysis, summarize each of the following in 2-3 words:
    
    {analysis_text}
    
    1. Customer & Agent
    
    2. Customer Type
    
    3. Main Issue
    
    4. Service Discussed
    
    5. Agent's Response
    
    6. Customer Satisfaction
    
    7. Sentiment
    
    8. Competitor or Upsell
    
    9. Resolution
    
    """
    
    class CallAnalytics:
    
        def __init__(self, client):
    
            self.client = client
    
            self.transcriptions = {}
    
        def process_audio_files(self, audio_paths: List[str]) -> Dict[str, dict]:
    
            if not audio_paths:
    
                print("No audio files provided")
    
                return {}
    
            print(f"Processing {len(audio_paths)} audio file(s)...")
    
            try:
    
                job = self.client.speech_to_text_job.create_job(
    
                    model="saaras:v4",
    
                    mode="translate",
    
                    with_diarization=True,
    
                )
    
                # For longer audio files, raise `timeout` so the upload has time to complete.
    
                job.upload_files(file_paths=audio_paths, timeout=300)
    
                job.start()
    
                print("Waiting for transcription to complete...")
    
                job.wait_until_complete()
    
                file_results = job.get_file_results()
    
                print(f"Successful: {len(file_results['successful'])} | Failed: {len(file_results['failed'])}")
    
                for f in file_results["failed"]:
    
                    print(f"  Failed: {f['file_name']}, {f['error_message']}")
    
                if not file_results["successful"]:
    
                    print("All files failed, nothing to analyze.")
    
                    return {}
    
                output_dir = Path(f"{OUTPUT_DIR}/transcriptions_{job._job_id}")
    
                output_dir.mkdir(parents=True, exist_ok=True)
    
                job.download_outputs(output_dir=str(output_dir))
    
                transcriptions = self._parse_transcriptions(output_dir)
    
                self.transcriptions.update(transcriptions)
    
                print(f"Successfully transcribed {len(transcriptions)} file(s)!")
    
                for file_name, data in transcriptions.items():
    
                    self.analyze_transcription(data["conversation_path"], output_dir, file_name)
    
                return transcriptions
    
            except Exception as e:
    
                print(f"Error processing audio files: {e}")
    
                return {}
    
        def _parse_transcriptions(self, output_dir: Path) -> Dict[str, dict]:
    
            transcriptions = {}
    
            for json_file in output_dir.glob("*.json"):
    
                try:
    
                    with open(json_file, "r", encoding="utf-8") as f:
    
                        data = json.load(f)
    
                    diarized = data.get("diarized_transcript", {}).get("entries")
    
                    speaker_times = {}
    
                    lines = []
    
                    if diarized:
    
                        for entry in diarized:
    
                            speaker = entry["speaker_id"]
    
                            text = entry["transcript"]
    
                            lines.append(f"{speaker}: {text}")
    
                            start = entry.get("start_time_seconds")
    
                            end = entry.get("end_time_seconds")
    
                            if start is not None and end is not None:
    
                                speaker_times[speaker] = speaker_times.get(speaker, 0.0) + (end - start)
    
                    else:
    
                        lines = [f"UNKNOWN: {data.get('transcript', '')}"]
    
                    conversation_text = "\n".join(lines)
    
                    txt_path = output_dir / f"{json_file.stem}_conversation.txt"
    
                    with open(txt_path, "w", encoding="utf-8") as f:
    
                        f.write(conversation_text)
    
                    timing_path = None
    
                    if speaker_times:
    
                        timing_path = output_dir / f"{json_file.stem}_timing.json"
    
                        with open(timing_path, "w", encoding="utf-8") as f:
    
                            json.dump(speaker_times, f, indent=2)
    
                    transcriptions[json_file.stem] = {
    
                        "entries": diarized or [],
    
                        "conversation_path": str(txt_path),
    
                        "timing_path": str(timing_path) if timing_path else None,
    
                    }
    
                except Exception as e:
    
                    print(f"Error parsing {json_file}: {e}")
    
            return transcriptions
    
        def analyze_transcription(self, conversation_path: str, output_dir: Path, file_name: str) -> Dict:
    
            try:
    
                with open(conversation_path, "r", encoding="utf-8") as f:
    
                    transcription = f.read()
    
                analysis_prompt = textwrap.dedent(ANALYSIS_PROMPT_TEMPLATE).format(transcription=transcription)
    
                response = self.client.chat.completions(
    
                    model="sarvam-105b",
    
                    max_tokens=4096,
    
                    reasoning_effort=None,
    
                    messages=[
    
                        {"role": "system", "content": "You are a call analytics expert working for a company's support operations team. Your job is to understand customer calls end-to-end and provide structured insights to improve customer experience and agent effectiveness."},
    
                        {"role": "user", "content": analysis_prompt},
    
                    ],
    
                )
    
                analysis = response.choices[0].message.content
    
                analysis_path = output_dir / f"{file_name}_analysis.txt"
    
                with open(analysis_path, "w", encoding="utf-8") as f:
    
                    f.write(analysis.strip())
    
                print(f"Analysis saved to {analysis_path}")
    
                return {"file_name": file_name, "analysis_path": str(analysis_path)}
    
            except Exception as e:
    
                error_msg = f"Error analyzing transcription: {str(e)}"
    
                print(error_msg)
    
                return {"file_name": file_name, "error": error_msg, "timestamp": datetime.now().isoformat()}
    
        def answer_question(self, question: str) -> None:
    
            for file_name, data in self.transcriptions.items():
    
                try:
    
                    with open(data["conversation_path"], "r", encoding="utf-8") as f:
    
                        transcription = f.read()
    
                    prompt = f"Based on this call transcription, answer the question below:\n\nTRANSCRIPTION:\n{transcription}\n\nQUESTION: {question}"
    
                    response = self.client.chat.completions(
    
                        model="sarvam-105b",
    
                        max_tokens=4096,
    
                        reasoning_effort=None,
    
                        messages=[
    
                            {"role": "system", "content": "You are a call analytics expert. Answer questions about the call using only information present in the transcription."},
    
                            {"role": "user", "content": prompt},
    
                        ],
    
                    )
    
                    answer = response.choices[0].message.content
    
                    q_hash = hashlib.sha1(question.encode()).hexdigest()[:6]
    
                    path = Path(data["conversation_path"]).parent / f"{file_name}_question_{q_hash}.txt"
    
                    with open(path, "w", encoding="utf-8") as f:
    
                        f.write(f"Question: {question}\n\nAnswer:\n{answer}")
    
                    print(f"Answer saved to {path}")
    
                except Exception as e:
    
                    print(f"Error answering question for {file_name}: {e}")
    
        def get_summary(self, output_dir: Optional[Path] = None) -> None:
    
            output_dir = output_dir or Path(OUTPUT_DIR)
    
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
            summary_path = output_dir / f"summary_{timestamp}.txt"
    
            try:
    
                with open(summary_path, "w", encoding="utf-8") as f:
    
                    f.write("CALL ANALYTICS SUMMARY REPORT\n")
    
                    f.write("=" * 60 + "\n")
    
                    f.write(f"Generated: {datetime.now()}\n")
    
                    f.write(f"Total Calls: {len(self.transcriptions)}\n")
    
                    f.write("=" * 60 + "\n\n")
    
                    for file_name, data in self.transcriptions.items():
    
                        analysis_file = Path(data["conversation_path"]).parent / f"{file_name}_analysis.txt"
    
                        if not analysis_file.exists():
    
                            print(f"Analysis file not found for {file_name}, skipping.")
    
                            continue
    
                        with open(analysis_file, "r", encoding="utf-8") as af:
    
                            analysis_text = af.read()
    
                        summary_prompt = textwrap.dedent(SUMMARY_PROMPT_TEMPLATE).format(analysis_text=analysis_text)
    
                        response = self.client.chat.completions(
    
                            model="sarvam-105b",
    
                            max_tokens=4096,
    
                            reasoning_effort=None,
    
                            messages=[
    
                                {"role": "system", "content": "You are a call analytics summarizing expert. Provide concise and clear answers to each point."},
    
                                {"role": "user", "content": summary_prompt},
    
                            ],
    
                        )
    
                        concise_summary = response.choices[0].message.content.strip()
    
                        f.write(f"Call File: {file_name}\n")
    
                        f.write("-" * 30 + "\n")
    
                        f.write(f"{concise_summary}\n\n")
    
                print(f"Summary saved to {summary_path}")
    
            except Exception as e:
    
                print(f"Error writing summary: {e}")
    
    client = SarvamAI(api_subscription_key=os.environ["SARVAM_API_KEY"])
    
    analytics = CallAnalytics(client=client)
    
    audio_path = "/path/to/your/audio/file.mp3"
    
    analytics.process_audio_files(prepare_audio_paths(audio_path))
    
    analytics.answer_question("Was a refund timeline promised to the customer?")
    
    analytics.get_summary()

### How it works

  * **`split_audio` / `prepare_audio_paths`** handle the Batch API’s 2-hour-per-file limit. Most calls are well under 2 hours, so `prepare_audio_paths` just returns the original path unchanged; only recordings longer than 2 hours actually get split and exported into parts.
  * **`process_audio_files`** creates a diarized transcription job on Sarvam’s Batch STT Translate API, uploads your audio, waits for completion, checks per-file success/failure, downloads the raw outputs, and kicks off analysis for every successfully transcribed file.
  * **`_parse_transcriptions`** reads the downloaded JSON, converts diarized entries into a `SPEAKER: text` transcript (`*_conversation.txt`), and tallies each speaker’s total talk-time (`*_timing.json`), handy for spotting whether the agent is doing too much (or too little) of the talking.
  * **`analyze_transcription`** sends the parsed transcript to a Sarvam chat model with a structured prompt covering speaker roles, customer type, issue, resolution, sentiment, and upsell opportunities, saving the result to `*_analysis.txt`.
  * **`answer_question`** lets you ask any custom question (e.g. _“Did the agent mention a refund timeline?”_) against every transcript you’ve processed so far.
  * **`get_summary`** condenses each call’s analysis into a 2-3-word-per-field summary and writes one consolidated report, the fastest way to scan many calls at a glance.



`sarvam-105b` has reasoning enabled by default, and reasoning tokens count toward `max_tokens`. With no `max_tokens` set, the 9-point structured analysis prompt above can get cut off mid-answer (which then breaks `get_summary`, since it summarizes a truncated analysis). Setting `max_tokens=4096` and `reasoning_effort=None` avoids this and is also cheaper and faster for this kind of structured-extraction task, which doesn’t benefit much from chain-of-thought reasoning. See [Reasoning](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level) for details.

For very long calls, the transcript plus prompt may exceed the chat model’s context window. See **Tips and Best Practices** below for how to handle this.

The last block in the script creates the client, runs the pipeline on your audio, asks a follow-up question, and generates a summary. Once it completes, check the `outputs/` directory. You’ll have the raw transcription JSON, the parsed conversation and timing files, the structured analysis, your question’s answer, and a summary report, all named by the original audio file.

## **5\. Sample Output**

Below is the analysis you’d get by running the pipeline on the sample [Sample_product_refund.mp3](https://github.com/sarvamai/sarvam-ai-cookbook/blob/main/sample_data/call_analytics_audios/Sample_product_refund.mp3) recording.
    
    
    Here's a structured analysis of the call transcription:
    
    ### 1. Speaker Identification
    
    * **Customer:** SPEAKER_00 (Adam Wilson)
    
    * **Agent:** SPEAKER_01 (Sam from Coaching Downs)
    
    ### 2. Customer Type
    
    * **Existing customer:** The customer has previously made a purchase (order number provided) and is now initiating a return and refund request.
    
    ### 3. Initial Problem/Query
    
    * The customer called to:
    
        * Return an item due to incorrect size.
    
        * Inquire about the status of their refund, as it hasn't reflected in their account yet.
    
    ### 4. Services/Products Involved
    
    * **Product:** Clothing item (implied by the return and size issue).
    
    * **Services:** Return processing and refund issuance.
    
    ### 5. Agent's Response and Resolution Process
    
    * **Initial Steps:**
    
        * Requested the order number, customer name, and contact details (phone number and email).
    
        * Verified the order details in the system.
    
    * **Issue Identification:**
    
        * The order wasn't immediately found in the system, leading to further verification.
    
        * The customer lacked the return tracking number from the courier company.
    
    * **Resolution Steps:**
    
        * Agent confirmed the return request date (15th of November) and noted it was outside the standard refund processing timeframe.
    
        * Agent escalated the case to the corporate office for review and promised to send an email update within 2-4 business days.
    
        * Agent reassured the customer about the refund timeline and confirmed the email address for communication.
    
    ### 6. Customer Satisfaction
    
    * **Neutral to slightly positive:** The customer seemed somewhat reassured by the agent's explanation and the promise of a prompt update. However, there was initial frustration about the refund delay.
    
    ### 7. Customer Sentiments
    
    * **Initial Frustration:** Expressing concern about the missing refund and the potential delay in processing.
    
    * **Reassurance:** After the agent's explanation, the customer seemed more at ease, though still awaiting confirmation.
    
    ### 8. Competitors/Upselling Opportunities
    
    * **No mention of competitors.**
    
    * **No clear upselling/cross-selling opportunities identified during the call.** The focus was solely on resolving the return and refund issue.
    
    ### 9. Resolution Summary and Success
    
    * **Resolution:** The agent escalated the case to the corporate office for review and promised an email update within 2-4 business days.

## **6\. Tips & Best Practices**

  * **Audio quality:** Clear audio with minimal background noise and cross-talk significantly improves diarization and transcription accuracy.
  * **Speaker count:** If you know the number of speakers in advance, pass `num_speakers` to `create_job` for more consistent diarization instead of relying on auto-detection.
  * **Batch limits:** A single job accepts up to 20 files and each file can be up to 2 hours long. `split_audio` and `prepare_audio_paths` in [The Full Pipeline Script](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline#4-the-full-pipeline-script) handle anything longer.
  * **Long transcripts:** If a call transcript is long enough to risk exceeding the chat model’s context window, chunk it (e.g. by time segment) and analyze each chunk before combining results, rather than sending the entire transcript in one prompt.
  * **Cost & latency:** Each call triggers one LLM request per method (`analyze_transcription`, `answer_question`, `get_summary`). For large call volumes, batch or parallelize these calls and monitor your token usage.
  * **API key security:** Load your key from an environment variable rather than hardcoding it, especially outside local experimentation.



## **7\. Error Handling**

You may encounter these errors while using the API:

  * **403 Forbidden** (`invalid_api_key_error`), invalid API key. Use a valid key from the [Sarvam AI Dashboard](https://dashboard.sarvam.ai/).
  * **429 Too Many Requests** (`insufficient_quota_error` / `rate_limit_exceeded_error`), credits exhausted or rate limit hit. Retry with exponential backoff.
  * **500 Internal Server Error** (`internal_server_error`), issue on our servers. Try again later; contact support if persistent.



For the full error-code table, request validation errors (400/422), retry guidance, and SDK exceptions, see [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting).

## **8\. Additional Resources**

  * **Documentation** : [docs.sarvam.ai](https://docs.sarvam.ai/)
  * **Related cookbooks** : [Batch Speech-to-Text Translate](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api) · [Chat Completion API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * **Example projects** : [sarvam-ai-cookbook on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook)
  * **Community** : [Join the Discord Community](https://discord.com/invite/5rAsykttcs)



## **9\. Final Notes**

  * Keep your API key secure, prefer environment variables over hardcoding.
  * Use clear audio for best diarization and transcription results.
  * All outputs (transcripts, timing, analysis, answers, summaries) are saved under `outputs/` for easy review.



**Keep Building!** 🚀

Was this page helpful?

YesNo

[Previous](https://docs.sarvam.ai/api/developer-tools/agent-skills)[Live Video TranscriptionNext](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)[Built with](https://buildwithfern.com/?utm_campaign=buildWith&utm_medium=docs&utm_source=docs.sarvam.ai)

  * Getting Started

    * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
    * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
    * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
    * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
    * [Models](https://docs.sarvam.ai/api/getting-started/models)

    * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
    * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
    * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
    * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
    * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
    * Account & Billing

  * API Guides & Tutorials

    * Large Language Models

    * Speech to Text

    * Text to Speech

    * Text Processing

    * Document Intelligence

    * Document Translation

    * Dubbing

    * Instant Voice CloningBeta

  *     * Integration

    * Developer Tools

  * Cookbook

    * Guides
      * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
      * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
      * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
      * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
      * [Example Projects on GitHub](https://github.com/sarvamai/sarvam-ai-cookbook/tree/main/examples "Example Projects on GitHub")

    * Example Voice Agents

  * Self-Hosted Deployments

    * Overview

    * AWS SageMaker

  *     * Migrations




  * [Welcome](https://docs.sarvam.ai/api/getting-started/welcome)
  * [Quickstart](https://docs.sarvam.ai/api/getting-started/quickstart)
  * [SDKs & Libraries](https://docs.sarvam.ai/api/getting-started/sdks)
  * [Building for Indian Languages](https://docs.sarvam.ai/api/getting-started/building-for-india)
  * [Models](https://docs.sarvam.ai/api/getting-started/models)
  * [Saaras](https://docs.sarvam.ai/api/getting-started/models/saaras)
  * [Bulbul](https://docs.sarvam.ai/api/getting-started/models/bulbul)
  * [Sarvam 105B](https://docs.sarvam.ai/api/getting-started/models/sarvam-105b)
  * [Open-Weight Models](https://docs.sarvam.ai/api/getting-started/models/openweight)
  * [GLM-5.3](https://docs.sarvam.ai/api/getting-started/models/openweight/glm-5-3)
  * [Gemma 4 31B](https://docs.sarvam.ai/api/getting-started/models/openweight/gemma-4-31b)
  * [DeepSeek V4.1 Flash](https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash)
  * [Mayura](https://docs.sarvam.ai/api/getting-started/models/mayura)
  * [Sarvam Translate](https://docs.sarvam.ai/api/getting-started/models/sarvam-translate)
  * [Sarvam Vision](https://docs.sarvam.ai/api/getting-started/models/sarvam-vision)
  * [Sarvam 30B (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-30b)
  * [Sarvam M (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/sarvam-m)
  * [Saarika (Deprecated)](https://docs.sarvam.ai/api/getting-started/models/saarika)
  * [Credits & Rate Limits](https://docs.sarvam.ai/api/getting-started/ratelimits)
  * [Commercial Licensing](https://docs.sarvam.ai/api/getting-started/commercial-licensing)
  * [Errors & Troubleshooting](https://docs.sarvam.ai/api/getting-started/errors-troubleshooting)
  * [Talk to us](https://docs.sarvam.ai/api/getting-started/help)
  * [Pricing](https://docs.sarvam.ai/api/getting-started/pricing)
  * [Organisations & workspaces](https://docs.sarvam.ai/api/platform/organisations-and-workspaces)
  * [Create an organisation](https://docs.sarvam.ai/api/platform/create-an-organisation)
  * [Create a workspace](https://docs.sarvam.ai/api/platform/create-a-workspace)
  * [Invite your team](https://docs.sarvam.ai/api/platform/invite-your-team)
  * [Billing & payments](https://docs.sarvam.ai/api/platform/billing)
  * [Platform FAQ](https://docs.sarvam.ai/api/platform/faq)
  * [Chat Completion](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/overview)
  * [Responses API](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/responses-api)
  * [List your chat messages](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/list-your-chat-messages)
  * [Control response randomness](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-randomness)
  * [Control response diversity](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-response-diversity)
  * [Adjust the model's thinking level](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/adjust-the-models-thinking-level)
  * [Encourage new topics in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/encourage-new-topics-in-response)
  * [Reduce repetition words or phrases in response](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/reduce-repetition-words-or-phrases-in-response)
  * [Get repeatable results](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/get-repeatable-results)
  * [Control the response length](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-the-response-length)
  * [Control where the model stops](https://docs.sarvam.ai/api/api-guides-tutorials/chat-completion/how-to/control-where-the-model-stops)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/overview)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/rest-api)
  * [Batch API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/batch-api)
  * [Realtime Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/realtime-streaming)
  * [Best Practices](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/best-practices)
  * [FAQs](https://docs.sarvam.ai/api/speech-to-text/faq)
  * [Select Output Mode](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/select-output-mode)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/specify-language-codes)
  * [Enable Speaker Diarization](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/enable-speaker-diarization)
  * [Keyterm Prompting](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/how-to/keyterms)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/agri-rural)
  * [Streaming API](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/streaming-api)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/overview)
  * [Voices](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/voices)
  * [Which API to Use](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/which-api-to-use)
  * [Rest API](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/rest-api)
  * [HTTP Stream](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/http-stream)
  * [WebSocket](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/streaming-api/web-socket)
  * [Pronunciation Dictionary](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/pronunciation-dictionary)
  * [Best Practice Guide for Bulbul v4 Flash](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/best-practices)
  * [Best Practices (Bulbul v3)](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/bulbul-v3-best-practices)
  * [Set the Language](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-language)
  * [Change the Speaker Voice](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/change-the-speaker-voice)
  * [Adjust the Tone](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-tone)
  * [Adjust the Speed](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-speed)
  * [Adjust the Loudness](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/adjust-the-loudness)
  * [Set the Sample rate](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-the-sample-rate)
  * [Enable Text Preprocessing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/enable-text-preprocessing)
  * [Set audio format for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-audio-format-for-output)
  * [Set bitrate for output](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-bitrate-for-output)
  * [Set maximum length for sentence splitting](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-maximum-length-for-sentence-splitting)
  * [Set buffer size to start processing](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/how-to/set-buffer-size-to-start-processing)
  * [IVR & Contact Center](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/ivr-contact-center)
  * [BFSI Voice Bots](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/bfsi-voice-bots)
  * [EdTech](https://docs.sarvam.ai/api/api-guides-tutorials/speech-to-text/use-cases/edtech)
  * [Government Services](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/government-services)
  * [Agri & Rural](https://docs.sarvam.ai/api/api-guides-tutorials/text-to-speech/use-cases/agri-rural)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/overview)
  * [Text Translation](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/translation)
  * [Transliteration](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/transliteration)
  * [Language Detection](https://docs.sarvam.ai/api/api-guides-tutorials/text-processing/language-detection)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/overview)
  * [Get your config_id](https://docs.sarvam.ai/api/api-guides-tutorials/document-intelligence/how-to/get-your-config-id)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/overview)
  * [Set Style Guidelines](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/style-guidelines)
  * [Pick a Genre](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/genre-and-model-tier)
  * [Use Native Numerals](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/native-numerals)
  * [Poll Status and Export Results](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/how-to/poll-and-export)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/faq)
  * [Use Cases](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/use-cases)
  * [Translate a PDF](https://docs.sarvam.ai/api/api-guides-tutorials/doc-translation/guides/translate-a-pdf)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/overview)
  * [Job Lifecycle](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/job-lifecycle)
  * [Specify Language Codes](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/specify-language-codes)
  * [Control Translation Tone](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/control-translation-tone)
  * [Choose a Voice](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-a-voice)
  * [Choose Export Formats](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/how-to/choose-export-formats)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/dubbing/faq)
  * [Overview](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/overview)
  * [Prepare Reference Audio](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/prepare-reference-audio)
  * [Clone Across Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/clone-across-languages)
  * [Choose Audio Formats](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/choose-audio-formats)
  * [Use Quality Control](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/use-quality-control)
  * [HTTP Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/http-streaming)
  * [WebSocket Streaming](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/how-to/websocket-streaming)
  * [Supported Languages](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/supported-languages)
  * [FAQs](https://docs.sarvam.ai/api/api-guides-tutorials/voice-cloning/faq)
  * [LiveKit](https://docs.sarvam.ai/api/integration/build-voice-agent-with-live-kit)
  * [Pipecat](https://docs.sarvam.ai/api/integration/build-voice-agent-with-pipecat)
  * [Twilio](https://docs.sarvam.ai/api/integration/build-voice-agent-with-twilio)
  * [Exotel](https://docs.sarvam.ai/api/integration/build-voice-agent-with-exotel)
  * [Vobiz](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vobiz)
  * [Vapi](https://docs.sarvam.ai/api/integration/build-voice-agent-with-vapi)
  * [n8n](https://docs.sarvam.ai/api/integration/n8n)
  * [Vercel AI SDK](https://docs.sarvam.ai/api/integration/vercel-ai-sdk)
  * [LangChain](https://docs.sarvam.ai/api/integration/langchain)
  * [LiveKit in Production](https://docs.sarvam.ai/api/integration/livekit-production-best-practices)
  * [Pipecat in Production](https://docs.sarvam.ai/api/integration/pipecat-production-guide)
  * [MCP Server](https://docs.sarvam.ai/api/developer-tools/mcp)
  * [Markdown & llms.txt](https://docs.sarvam.ai/api/developer-tools/llms-txt)
  * [Context7](https://docs.sarvam.ai/api/developer-tools/context7)
  * [Agent Skills](https://docs.sarvam.ai/api/developer-tools/agent-skills)
  * [Call Analytics Pipeline](https://docs.sarvam.ai/api/cookbook/guides/call-analytics-pipeline)
  * [Live Video Transcription](https://docs.sarvam.ai/api/cookbook/guides/live-video-transcription)
  * [Podcast Generator](https://docs.sarvam.ai/api/cookbook/guides/podcast-generator)
  * [WhatsApp Bot](https://docs.sarvam.ai/api/cookbook/guides/whats-app-bot)
  * [Collection Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/collection-agent)
  * [Government Scheme Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/government-scheme-agent)
  * [Tutor Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/tutor-agent)
  * [Loan Advisory Agent](https://docs.sarvam.ai/api/cookbook/example-voice-agents/loan-advisory-agent)
  * [Introduction](https://docs.sarvam.ai/api/self-hosted/introduction)
  * [Managed vs Self-Hosted](https://docs.sarvam.ai/api/self-hosted/hosted-vs-self-hosted)
  * [How it works](https://docs.sarvam.ai/api/self-hosted/architecture)
  * [Get started](https://docs.sarvam.ai/api/self-hosted/sagemaker/get-started)
  * [Speech-to-Text (Saaras v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-vision)
  * [Text-to-Speech (Bulbul v3)](https://docs.sarvam.ai/api/self-hosted/sagemaker/deploy-bulbul)
  * [Deploy with Terraform](https://docs.sarvam.ai/api/self-hosted/sagemaker/terraform)
  * [Speech-to-Text](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-saaras)
  * [Sarvam Vision](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-vision)
  * [Text-to-Speech](https://docs.sarvam.ai/api/self-hosted/sagemaker/api-bulbul)
  * [Error handling](https://docs.sarvam.ai/api/self-hosted/sagemaker/errors)
  * [Configure & tune](https://docs.sarvam.ai/api/self-hosted/sagemaker/configure)
  * [Operations](https://docs.sarvam.ai/api/self-hosted/sagemaker/operations)
  * [Limitations](https://docs.sarvam.ai/api/self-hosted/sagemaker/limitations)
  * [Troubleshooting](https://docs.sarvam.ai/api/self-hosted/sagemaker/troubleshooting)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-elevenlabs/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-elevenlabs/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-elevenlabs/speech-to-text)
  * [Instant Voice Cloning](https://docs.sarvam.ai/api/migrations/from-elevenlabs/voice-cloning)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-cartesia/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-cartesia/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-cartesia/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-deepgram/overview)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-deepgram/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-deepgram/speech-to-text)
  * [Overview](https://docs.sarvam.ai/api/migrations/from-gemini/overview)
  * [Chat Completion](https://docs.sarvam.ai/api/migrations/from-gemini/chat-completion)
  * [Text to Speech](https://docs.sarvam.ai/api/migrations/from-gemini/text-to-speech)
  * [Speech to Text](https://docs.sarvam.ai/api/migrations/from-gemini/speech-to-text)



  * [Model APIs](https://docs.sarvam.ai/api)
  * [Voice Agents](https://docs.sarvam.ai/voice-agents)
  * [Doc Agents](https://docs.sarvam.ai/docai)
  * [Content Studio](https://docs.sarvam.ai/creative)
  * [Cowork](https://docs.sarvam.ai/cowork)
  * [API Reference](https://docs.sarvam.ai/api-reference)
  * [Changelog](https://docs.sarvam.ai/changelog)


