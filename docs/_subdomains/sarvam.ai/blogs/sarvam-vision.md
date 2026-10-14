---
url: https://sarvam.ai/blogs/sarvam-vision/
title: Sarvam Vision multimodal document AI | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:17:25.167385+00:00
---

# Sarvam Vision multimodal document AI | Sarvam AI

> Source: https://sarvam.ai/blogs/sarvam-vision/

  1. [ Home ](https://sarvam.ai/)
  2. /
  3. [ Blog ](https://sarvam.ai/blogs)



# Sarvam Vision

Leading performance on global benchmarks; best-in-class accuracy for Indian languages.

Research

[Try in Playground](https://dashboard.sarvam.ai/document-intelligence)

* * *

Feb 5, 2026·6 min readShare

![Sarvam Vision](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/a0e1262e6ef765360b2b2b1df18cc2f5818ebbb4-1800x1350.png)

## Introduction

Today, we are introducing Sarvam Vision. We have released models and applications across voice and text. With this release, we extend that work to vision. We live in a multimodal world, and vision is a crucial modality to ensure all perception problems can be solved for users and enterprises. Some of these problems surround document intelligence, general vision ("What am I seeing?") capabilities, among many others.

As part of the sovereign model series, we introduce a 3B-parameter state-space vision-language model. The model is capable of a range of visual understanding tasks, including image captioning, scene text recognition, chart interpretation, and complex table parsing.

A central challenge in vision today is high-accuracy document intelligence, particularly for Indian languages. Much of India's knowledge remains embedded in physical documents, scanned archives, and historical collections. This is knowledge locked in plain sight. Unlocking this material is essential for long-term preservation, access, and reuse across research, governance, and enterprise workflows.

Frontier Vision Language Models have established a high bar for processing modern English documents. However, a significant gap remains in the industry: most global models treat Indian languages as secondary, often resulting in lower accuracy for regional scripts. Along with pushing the frontiers of accuracy, our VLM is an inference-efficient 3B state-space model.

## Model Training, Performance, and Benchmarks

At a high-level, our document intelligence architecture comprises the sovereign VLM and two harness modules - (a) semantic layout parser and (b) reading order network. The primary advances we made were for data curation and training algorithms.

The data curation effort underwent a rigorous process of creating high-quality synthetic and real-world document image-text samples for all Indian languages, alongside English. The data consisted of various domains like scientific literature, financial documents, government bulletins, historical manuscripts, textbooks, magazines, newspapers, among others. Each domain underwent data generation tailored to the specific use case. For example, in the case of chart understanding, our data consisted of chart-text pairs for a variety of tasks - like structured extraction, description, analysis. In the case table parsing, we built datasets that focus on structure and relationship recognition of the table cells.

On the algorithmic side, we performed a round of continual pretraining on the base Sarvam sovereign 3B model; followed by supervised fine-tuning and reinforcement learning using verifiable rewards.

### Global Benchmarks

#### olmOCR-Bench

A benchmark for evaluating document-level OCR that performs pass-fail unit tests which are simple, unambiguous, and deterministically machine-verifiable. For the evaluation, we filtered out 1,258 samples out of 1,403 total samples in order to ensure the benchmarking is performed only on English documents.[![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)_olmOCR-Bench-English_](https://huggingface.co/datasets/sarvamai/olmOCR-Bench-English). The implementation details can be found in this [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)github repository](https://github.com/sarvamai/olmOCR-bench-sarvam-api).

Category| Sarvam Vision| Mistral OCR 3| Chandra| Gemini 3 Pro| PaddleOCR VL 1.5| PaddleOCR VL| DeepSeek OCR v2| Gemini 3 Flash| GPT 5.2  
---|---|---|---|---|---|---|---|---|---  
ArXiv Math| 86.5| 85.4| 81.4| 70.6| 85.4| 85.4| 81.9| 66.5| 61  
Base| 99.6| 99.9| 99.8| 99.8| 98.8| 98.6| 99.8| 99.8| 99.8  
Hdr/Ftr| 96.3| 93.8| 88.8| 84| 96.9| 96.9| 95.6| 83.8| 75.6  
TinyTxt| 91| 88.9| 91.9| 90.3| 80.8| 80.8| 88.7| 88.2| 62.2  
MultCol| 82.2| 82.1| 82.9| 79.2| 82.6| 82.5| 83.6| 73.7| 70.2  
OldScan| 49.8| 48.8| 49.2| 47.5| 39.2| 38.8| 33.7| 46| 34.6  
OldMath| 81| 68.3| 73.6| 84.9| 66.4| 66.4| 68.8| 85.8| 75.8  
Tables| 88.3| 86.1| 88.2| 84.9| 84.1| 83.9| 78.1| 75.9| 79  
  
Scroll

Scroll

olmOCR (Category-wise Performance Comparison)

#### OmniDocBench V1.5

A comprehensive benchmark for evaluating document parsing, featuring various document and layout types (academic papers, financial reports, and handwritten notes). We report the performance on the official English-only split from the evaluation set which contains 628 samples.

_OmniDocBench V1.5 (Category-wise Performance Comparison)_

## Sarvam Indic OCR Bench

Global benchmarks focus heavily on English document parsing, and at present there is no Indic benchmark of similar standard to the best of our knowledge. We bridge this gap by creating Sarvam Indic OCR Bench which contains 20,267 samples from various document pages. The sample set is distributed across 22 official Indian languages - ranging from 1800-present and with varying quality of scans and content. Furthermore, they are curated at a semantic block-level to robustly evaluate character and word accuracy. We report word accuracy in this section which is computed as 100 x (1 - WER).

#### Language-wise accuracy on Sarvam Indic OCR Bench across all 22 scheduled Indian languages

Language| Sarvam Vision| Gemini 3 Pro| GCV| Opus 4.5| Surya| Gemma3-27B| GPT 5.2  
---|---|---|---|---|---|---|---  
Hindi| 95.91| 95.12| 90.94| 93.08| 81.85| 85.57| 84.86  
Bengali| 92.61| 90.79| 88.23| 83.76| 70.82| 65.07| 70.52  
Tamil| 93.42| 92.73| 89.69| 89.62| 75.92| 77.14| 61.87  
Telugu| 87.70| 85.32| 82.58| 71.28| 58.77| 53.88| 35.70  
Marathi| 93.13| 90.39| 87.86| 81.66| 72.29| 70.61| 63.81  
Malayalam| 91.60| 87.10| 88.30| 82.88| 83.80| 20.03| 56.66  
Kannada| 89.89| 87.36| 85.54| 77.41| 68.05| 45.99| 26.49  
Odia| 81.95| 75.39| 82.20| 57.22| 61.16| -9.54| 10.53  
Punjabi| 92.28| 89.29| 88.10| 85.91| 71.75| 40.83| 59.98  
Gujarati| 90.74| 88.40| 81.63| 77.53| 68.02| 62.62| 53.45  
Urdu| 87.01| 85.76| 81.17| 77.89| 55.17| 64.97| 57.49  
Sindhi| 90.24| 86.31| 86.71| 71.89| 61.31| 56.69| 49.00  
Santhali| 80.32| 64.02| 54.79| 36.62| 31.24| 36.37| 27.44  
Sanskrit| 81.65| 76.62| 64.90| 4.25| 44.77| 34.85| -21.22  
Nepali| 93.90| 93.61| 91.43| 84.73| 80.94| 79.91| 67.63  
Manipuri| 90.11| 89.33| 82.50| 59.03| 67.09| 65.68| 3.26  
Maithili| 81.95| 50.96| 49.04| 26.07| 1.94| 3.16| 13.68  
Konkani| 91.10| 89.96| 83.02| 78.26| 71.96| 53.13| 35.73  
Kashmiri| 55.93| 44.46| 33.41| 29.89| 9.76| -18.03| -0.60  
Dogri| 82.61| 79.73| 72.46| 48.92| 59.41| 47.38| 6.08  
Bodo| 89.19| 87.21| 78.64| 62.60| 68.04| 55.76| 34.19  
Assamese| 88.74| 85.36| 84.50| 77.58| 75.76| 39.90| 52.71  
  
Scroll

Scroll

## Core Document Intelligence Capabilities

### Text Extraction ≠ Knowledge Extraction

Sarvam Vision fundamentally rethinks document intelligence as a knowledge extraction problem, while most alternatives stop at text extraction. Documents are more than words - they contain tables and visual elements like complex scientific charts, illustrations, and infographics. To truly extract all knowledge, any document intelligence model must attend to each and every pixel going beyond text. Sarvam Vision interprets visual logic that holds all information together. Whether it is extracting data points from a trend line or preserving a nested table, the model performs high-fidelity knowledge extraction end-to-end.

## Illustrations of Various Domains

### 1\. OCR on English + all 22 scheduled Indian languages

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-1-original.jpg)

Original Scan

have knowledge of some vacant "Consulate" or "Special Service", that my Record and Endorsements would warrant my filling to the advantage of the Government A Knowledge of your Selection and appointment of Such only as are most fitting for the place regarded of politics or local influence has prompted me you and myself to look to you Mr President for that just consideration we have failed to secure at other hands, With the assurance of two having their Countrys welfare more at heart than their own personal interest believe us Mr President ## Your Obt Servants Wm H. Young and native of Erie County New York Wife F Rowland Young native of St Markes Florida address P.O. box 565 Washington DC

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-1-enhanced.png)

Enhanced Version

Example 1

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-2-original.png)

Original Scan

32 ப்ரம்ஹஸ்வரூபம். எட்டு அக்ஷரங்கள், ஓங்காரம். இதை அறிந்தவன் ஆத்ம ப்ரக்ருதி, ப்ரம்ஹமறிந்தவன். அவனே மோக்ஷமடைகிறான். ஓம் ப்ரம்ஹம், ந. விஷ்ணு, ம. ருத்ரன், ந. ஈச்வரன், ர. அண்டவிராட், ய. புருஷன், ண. பகவான், ய. பரமாத்மா. (ப்ரம்ஹ, விஷ்ணு, ருத்ர, அண்ட விராட், புருஷன், பகவான், பரமாத்மா) என அர்த்தம். அ, உ, ம பிந்து, நாதம், கலை, கலாதீரம், பரம், தாரகப்ரம்ஹம், என இவைகளை உபாஸிக்கவேணும். அ. ப்ரம்ஹா-ஜாம்பவான், உ. உபேந்திரன்-ஹரிநாயகர், ம-சிவன்-ஹநுமான், பிந்து-ஈச்வரன் -சத்குனன், நாதம்-விராட்-பரதன், கலா-புருஷன்-லக்ஷ் மணன், கலாதீரம்-ஸீதா, பரன்-பரமாத்மா-ராமர், இவ்விதம், ஓம் என்ற இந்த அக்ஷரத்தையே ரிக்வேதம், யஜூர்வேதம் என்பது, யாஜ்ஞவல்க்யரை பரத்வாஜர் கேட்டதும் இதுவே. எந்த மந்த்ரத்தால் ஈச்வரன் ப்ரீதி அடைகிறான் என்றதும், யாஜ்ஞவல்க்யர் சொன்னார். பரமாத்மா, நாராயணர், ஜாம்பவான், ஹநுமான், சத்ருக்னன், பரதன், லக்ஷ்மணன், ஸீதை, ராமன் இவர்களை நமஸ்கரிக்கிறேன். எனச் சொல்லவேணும். இதுவே எட்டுவித மந்த்ரமாக உள்ளது. இதை எவன் அத்தியயனம் செய்கிறானோ? அவன் அடைகிறான். அக்னி பயத்தினின்று நீங்கி பரிசுத்தமடை கிறான். நாராயண என்ற எட்டு அக்ஷரமந்திரத்தினால் ஆயிரம் ருத்ர ஜபம் செய்த புண்யமடைகிறான். ஆயிரம் காயத்ரீ பலன், கோடி ப்ரணவ ஜபபலன், நாராயணபத மடைகிறான். இதுதான் பரமபத மான விஷ்ணு பதம், என எப்பொழுதும் வித்வான்கள் அறியவே நன்றாகப் பார்க்கிறார்கள். மிதிலையில் ஜனகர் ப்ராம்ஹணர்களை ஜயித்து யாஜ்ஞயவல்க்யரையும். ப்ருஹஸ்பதியையும் கேட்டு இதையே சொன்னார் ஜ்யோதிர்லிங்கத்தை புருவ மத்தியில் எவன் நித்யம்த்யானம் செய்கிறானோ? அவன் ஸதா ஸந்யாஸி ஆகிறான். எனச்சொல்லி உபநிஷத் விஸ்தாரமாக முடித்தது. 25. த்ரிபாத் விபூதி மஹாநாராயண உபநிஷத்விவரணம். பரமதத்வமறிய ப்ரம்ஹா தேவமானப்படி 1000-வருஷம் தபஸ் செய்தார். மஹாவிஷ்ணு ப்ரஸன்னமாகி, ப்ரம்ஹனை நீங்கள் தான்

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-2-enhanced.png)

Enhanced Version

Example 2

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-3-original.png)

Original Scan

अमरनाथ की कथा इस कथा का नाम अमर कथा इसलिए है कि इसके श्रवण करने से शिव- चाम की प्राप्ति होती है। यह वह परम पवित्र कथा है जिसके सुनने से सुनने वालों को अमरपद की प्राप्ति होती है। तथा वह अमर हो जाते हैं। यह कथा श्री शंकर भगवान ने इसी गुफा में (श्री अमरनाथ जी की गुफा में) भगवती पार्वती जी को सुनाई थी। इस कथा को सुनकर ही श्री शुकदेवजी अमर हो गये थे । जब भगवान श्री शंकर यह कथा भगवती पार्वती को सुना रहे थे तो वहां एक तोते का बच्चा भी इस परम पवित्र कथा को सुन रहा था और इसे सुनकर फिर उस तोते के बच्चे ने श्री शुकदेव स्वरूप को पाया था । 'शुक' संस्कृत में तोते को कहते हैं और इसी कारण बाद में फिर मुनि 'शुकदेव, के नाम से संसार में प्रसिद्ध हुए। यह कथा भगवती पार्वती तथा भगवान शंकर का संवाद है। यह परम-पवित्र कथा लोक व परलोक का सुख देने वाली हैं। शंकर भगवान और जगतमाता के इस सम्वाद का वर्णन मृगु सहिता, नीलमत पुराण, तीर्थ संग्रह आदि ग्रन्थों में पाया जाता है। हम यहाँ पर आपके सम्मुख यह परम पवित्र कथा विस्तार पूर्वक रखेंगे । देव ऋषि नारद का कैलाश पर्वत पर आना और श्री पार्वतीजी से पूछना कि भगवान शंकर के गले में रुण्डमाला क्यों है? एक बार देव ऋषि नारद कैलाश पर्वत पर भगवान श्री शंकर के स्थान पर दर्शनार्थ पधारे । भगवान श्री शंकर उस समय वन, विहार के लिए गये हुए थे और भगवती पार्वती यहाँ पर विराजमान थीं। श्री पार्वतीजी ने देव ऋषि नारद को प्रणाम किया और सादर आसन दिया। और बोलीं- 'देव ऋषि! आपने यहाँ पधार कर हम पर बड़ी कृपा की अपने आने का कारण कहिए ।' देव ऋषि नारद बोला-"देवी! मेरा एक प्रश्न है उसका उत्तर चाहता हूँ।" ने कहा-“कहिए?" श्री पार्वतीजी ने कहा-"कहिए?" नारद बोले-"देवी! मुझे इस बात का बड़ा आश्चर्य है भगवान श्री शंकर जोकि हम दोनों से बड़े हैं। उनके गले में रुण्ड माला क्यों है?

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-3-enhanced.png)

Enhanced Version

Example 3

### 2\. Complex table parsing

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-4-original.jpg)

Original Scan

6 Public Health Nursing TABLE 2. Study Findings 

Characteristics| Experimental 1  
(n = 50)| Control 1  
(n = 50)| Experimental 2  
(n = 50)| Control 2  
(n = 38)  
---|---|---|---|---  
Antenatal and childbirth care| | | | | | | |   
Any antenatal care| 33| 49| <.001| 47| 18| <.001| |   
Received tetanus immunization ≥2  
times during last pregnancyᵃ| 33| 50| .001| 47| 29| .379| |   
Skilled attendant at last birth| 20| 45| <.001| 8| 12| .084| |   
Knowledge of danger signs during  
the perinatal period| | | | | | | |   
Number of danger signs recalled,  
27 items (SD)| 7.90 (3.07)| 4.70 (1.88)| <.001| 13.92 (3.88)| 4.37 (2.62)| <.001| |   
Contraception| | | | | | | |   
Number of modern methodsᵇ  
recalled (SD)| 4.06 (1.37)| 2.82 (1.08)| <.001| 5.16 (1.00)| 2.00 (0.77)| <.001| |   
First aidᶜ  
Acceptable treatment answeredᵈ| 45| 7| <.001| 33| 5| <.001| |   
Health behaviors| | | | | | | |   
Care for sick <5-year-old child| | | | | | | |   
Has your child had a fever during  
the last 2 weeks?| 5| 17| .004| 4| 9| .066| |   
Did you seek advice or treatment  
for the illness outside of your home?| 1| 13| .039| 0| 9| .001| |   
Has your child had a cough or  
difficulty breathing during the last  
2 weeks?| 11| 20| .052| 4| 9| .066| |   
Did you seek advice or treatment  
for the illness outside of your home?| 3| 2| 1.000| 1| 3| .400| |   
Sanitation| | | | | | | |   
What was done to dispose of the stool?  
Appropriate methodᵉ| 26| 22| .106| 21| 4| .002| |   
Inappropriate methodᶠ| 3| 9| | 13| 17| | |   
Number of correct precautions against  
malaria recalled (eight items)  
Mean (SD)| 2.64 (0.985)| 1.28 (0.784)| <.001| 2.72 (1.011)| 0.58 (0.522)| <.001| |   
  
treatment (applying dirt and saliva, tomato, salt, or AJINOMOTO [monosodium glutamate]) for injuries that were sustained during agricultural work. The experimental villages had a significantly higher proportion of participants who answered that they received acceptable first aid treatment (E1-C1: χ2=57.85\chi^2 = 57.85χ2=57.85, p<.001p <.001p<.001; E2-C2: χ2=24.57\chi^2 = 24.57χ2=24.57, p<.001p <.001p<.001). **Health behaviors.** **Care for sick ≤5-** **year-old children** -Compared to E1, significantly more children in C1 had experienced a fever during the 2-week period before questioning (χ2=4.22\chi^2 = 4.22χ2=4.22, p =.004), and significantly more children in C1 were treated during their illness (χ2=5.29\chi^2 = 5.29χ2=5.29, p =.04). Although the frequency of children with fever in C2 was higher than that in E2, there were

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-4-enhanced.png)

Enhanced Version

Example 4

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-5-original.jpg)

Original Scan

118 Egypt. J. Phytopathol., Vo. 50, No. 2, pp 104-123 Table (10): The effect of different control treatments on some growth parameters of two Tagetes varieties grown in infested soil 90 days after transplanting, under greenhouse conditions. 

Tagetes spp.| Treatments| F. oxysporum| F. solani| R. solani  
---|---|---|---|---  
Plant  
height  
(cm)| Fresh  
weight  
(g)| Dry  
weight  
(g)| Plant  
height  
(cm)| Fresh  
weight  
(g)| Dry  
weight  
(g)| Plant  
height  
(cm)| Fresh  
weight  
(g)| Dry  
weight  
(g)  
Tagetes minuta| Bio-Cure B| 60| 400| 130.3| 55| 380| 125.6| 50| 360| 115.8  
Bio-Cure F| 70| 460| 151.2| 66| 450| 149.4| 60| 455| 153.6  
Rhizo-N| 76| 500| 163.4| 73| 470| 155.5| 70| 460| 156.6  
Topsin-M 70| 82| 550| 182.7| 80| 540| 179.9| 77| 530| 175.7  
Vitavax 200| 90| 600| 199.5| 86| 590| 190.5| 80| 580| 190.8  
Wood vinegar| 80| 520| 172.9| 75| 511| 171.5| 70| 500| 167.8  
Control| 30| 200| 65.8| 33| 210| 70.6| 35| 220| 70.6  
Mean| 69.7| 461.4| 152.2| 66.5| 450.1| 149| 63.1| 443.6| 147.3  
Tagetes erecta| Bio-Cure B| 65| 430| 135.7| 59| 395| 130.7| 54| 366| 122  
Bio-Cure F| 73| 470| 155.8| 71| 460| 155.5| 63| 462| 164.7  
Rhizo-N| 80| 520| 166.7| 75| 485| 166.4| 75| 473| 173  
Topsin-M 70| 85| 565| 185.5| 83| 455| 185.4| 81| 540| 183  
Vitavax 200| 94| 610| 210| 91| 610| 196.2| 86| 595| 196.6  
Wood vinegar| 83| 532| 178.6| 82| 520| 175.6| 75| 509| 177  
Control| 31| 205| 65.0| 32| 200| 71| 34| 210| 71.4  
Mean| 73| 476| 156.7| 70.4| 446.4| 154.4| 66.8| 450.7| 155.4  
L.S.D. at 5% Treatments (T) = 2.30, Varieties (V) = 0.50, Fungi (F) = 3.30, T×V = 4.40, T×F = 5.60, V×F = 5.20, T×V×F = 6.40  
  
OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-5-enhanced.png)

Enhanced Version

Example 5

### 3\. Multilingual visual reasoning

Visual components in a document play an important role. Oftentimes charts and illustrations communicate details that are not present in the extracted text. Sarvam Vision delivers natively multilingual reasoning capabilities for such visual elements in a document.

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-6-original.jpg)

Original Scan

| Metric | Decoding Temperature (Std Dev) | Suffix Injection (Std Dev) | Prompt Paraphrase (Std Dev) | | :--- | :--- | :--- | :--- | | Refusal Rate | ~0.195 | ~0.312 | ~0.134 | | Toxicity | ~0.110 | ~0.210 | ~0.092 | | AQI | ~0.020 | ~0.060 | ~0.020 | Figure 6: **Standard Deviation of Metrics under Perturbations.** AQI exhibits consistently lower variance than Refusal Rate (RR) and Detoxify-based Toxicity across decoding temperature, suffix injection, and prompt drift. This reflects its geometric robustness to generation stochasticity and surface perturbations, making it more stable for adversarial alignment evaluation. 

Model| AQI (Clean)| AQI (Jailbreak)| Drop (%)  
---|---|---|---  
TinyLLaMA| 0.91| 0.34| 62.6%  
Phi-2| 0.91| 0.35| 61.5%  
GPT-NeoX| 0.91| 0.61| 32.9%  
LLaMA-13B| 0.91| 0.67| 26.4%  
LLaMA-65B| 0.91| 0.73| 19.8%  
  
Table 10: AQI degradation under adversarial suffix in- jection. Smaller models show sharper collapses in latent safety separation. using LITMUS-P, a paraphrased variant of LIT- MUS generated via backtranslation and synonym augmentation. For each prompt, five semantically equivalent rewrites were used to elicit completions across four models. These results affirm that smaller models fail to encode paraphrase-invariant safety boundaries, while AQI captures these shifts via latent over- lap-quantified using XBI. 

Model| AQI (Orig)| AQI (Paraphrase)| Drop (%)  
---|---|---|---  
TinyLLaMA| 0.58| 0.32| 44.8  
Phi-2| 0.65| 0.45| 30.8  
LLaMA-13B| 0.78| 0.70| 10.3  
LLaMA-65B| 0.81| 0.76| 6.1  
  
Table 11: AQI sensitivity to paraphrastic rewording. Higher-capacity models show improved latent invari- ance. D.4 Stability vs. Behavioral Metrics Across all three settings, AQI demonstrates lower variance and higher sensitivity to latent collapse (cf. Figure 6). Moreover, AQI deflection often precedesprecedesprecedes be- havioral collapse. In jailbreak scenarios, AQI drops by 40-60% even when detox scores remain low-indicating representational entanglement be- fore output misalignment. As illustrated by Figure 7, AQI deflection of- 45

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-6-enhanced.png)

Enhanced Version

Example 6

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-7-original.png)

Original Scan

चित्र शीर्षक: प्राचीन भारत विवरण: यह चित्र भारत का एक विस्तृत ऐतिहासिक मानचित्र है। इसमें विभिन्न नदियों, पर्वत श्रृंखलाओं और भौगोलिक क्षेत्रों को दर्शाया गया है। मानचित्र पर कई स्थानों के नाम लिखे हैं जो संभवतः प्राचीन भारतीय राज्यों या शहरों को इंगित करते हैं। नीचे दाईं ओर 'अंग्रेजी मिल' (English Mill) लिखा हुआ स्केल बार है।

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-7-enhanced.png)

Enhanced Version

Example 7

### 4\. Visual data, structured outputs

![Original Scan](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-8-original.png)

Original Scan

अपेक्षित पाठ्यक्रम सुधार करने अथवा नीतिगत कार्यक्रमों का एक मंच उपलब्ध कराकर शिक्षा नीति हेतु 'परिणामों' पर ध्यान केंद्रित करना है। प्रतिस्पर्धी और सहयोगी संघवाद की भावना को बढ़ावा देने के लिए नीति आयोग के अधिदेश के अनुरूप, एसईक्यूआई देश भर में ज्ञान और सर्वोत्तम प्रथाओं को साझा करने की सुविधा प्रदान करने का प्रयास करता है। मानव संसाधन विकास मंत्रालय (एमएचआरडी), विश्व बैंक और क्षेत्र विशेषज्ञों जैसे प्रमुख हितधारकों सहित एक सहयोगी प्रक्रिया के माध्यम से विकसित सूचकांक में 30 महत्वपूर्ण संकेतक शामिल हैं। ये संकेतक हैं: श्रेणी 1: परिणाम डोमेन 1: शिक्षण परिणाम डोमेन 2: पहुंच परिणाम डोमेन 3: परिणामों के लिए अवसंरचना और सुविधाएं डोमेन 4: इक्विटी परिणाम श्रेणी 2: शासी-प्रक्रिया-सहायता परिणाम ▪ शिक्षण संबंधी परिणाम ▪ अभिगम परिणाम ▪ परिणामों के लिए अवसंरचना और सुविधाएं ▪ इक्विटी परिणाम ▪ शासन प्रक्रिया सहायता परिणाम यह छवि एक पाई चार्ट है जो पाँच अलग-अलग श्रेणियों में प्रतिशत वितरण को प्रदर्शित करती है, जो संभवतः किसी रिपोर्ट या अध्ययन के निष्कर्षों से संबंधित है। दाईं ओर की लेजेंड (legend) रंगों और उनके संबंधित लेबल द्वारा डेटा बिंदुओं की पहचान कराती है: 'लर्निंग आउटकम्स' (Learning Outcomes) के लिए गुलाबी, 'एक्सेस आउटकम्स' (Access Outcomes) के लिए नारंगी, 'इन्फ्रास्ट्रक्चर एंड फैसिलिटीज फॉर आउटकम्स' (Infrastructure & Facilities for Outcomes) के लिए पीला, 'इक्विटी आउटकम्स' (Equity Outcomes) के लिए हरा, और 'गवर्नेंस प्रोसेसेस एडिंग आउटकम्स' (Governance Processes Aiding Outcomes) के लिए नीला। डेटा का विस्तृत विवरण इस प्रकार है: 1. लर्निंग आउटकम्स (Learning Outcomes): यह श्रेणी सबसे बड़ा हिस्सा रखती है, जो कुल हिस्सेदारी का 34% है। 2. इक्विटी आउटकम्स (Equity Outcomes): दूसरा सबसे बड़ा खंड हरे रंग में दर्शाया गया है, जो 28% है। 3. गवर्नेंस प्रोसेसेस एडिंग आउटकम्स (Governance Processes Aiding Outcomes): नीले रंग में दिखाया गया, यह खंड 26% है। 4. एक्सेस आउटकम्स (Access Outcomes): नारंगी रंग में चित्रित, यह भाग 9% है। 5. इन्फ्रास्ट्रक्चर एंड फैसिलिटीज फॉर आउटकम्स (Infrastructure & Facilities for Outcomes): पीले रंग में दिखाई देने वाला, यह सबसे छोटा स्लाइस केवल 3% है। कुल मिलाकर, शीर्ष तीन श्रेणियां ('लर्निंग', 'इक्विटी', और 'गवर्नेंस') सामूहिक रूप से पूरे वृत्त के लगभग 88% हैं, जबकि शेष दो श्रेणियां मिलकर शेष 12% बनाती हैं। स्कूली शिक्षा के परिणाम वास्तविक शिक्षण परिणामों में होने चाहिए। यह प्रणाली शिक्षण सीखने की ओर अग्रसर है यह सुनिश्चित करने के लिए एसईक्यूआई शिक्षण परिणामों के लिए लगभग अपना आधा योगदान देता है। शिक्षण पर ध्यान केंद्रित रहे यह सुनिश्चित करने के लिए यह समूचे राष्ट्र में एक मजबूत संकेत भेजता है। तुलनात्मक सुविधा प्रदान करने के लिए, राज्यों और संघ राज्य क्षेत्रों को बड़े राज्यों, छोटे राज्यों और संघ राज्य क्षेत्रों के रूप में वर्गीकृत किया गया है। इन समूहों में समग्र निष्पादन स्कोर 45

OCR result

![Enhanced Version](https://assets.sarvam.ai/Blogs/sarvam-vision/comparison-8-enhanced.png)

Enhanced Version

Example 8

## In-the-Wild OCR and Perception

Sarvam Vision is built on a foundation of general image understanding and multilingual capabilities. While our current efforts are focused on pushing the frontiers of document intelligence, these broader capabilities remain a core part of the model.

Some illustrations of how Sarvam Vision interprets the natural image contexts:

![English Caption](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-caption-road.jpg)

### English Caption

output

The image captures a wide, paved asphalt road stretching into the distance under a bright, clear sky. On the left side of the road, there is a sidewalk lined with a series of blue and white metal bike racks. Behind these racks, a low fence with a green base and yellow horizontal bars separates the sidewalk from a dense, lush green tree line. The trees are thick with foliage, creating a natural canopy over the road. In the middle distance, a blue public trash bin is visible near the fence. Further down the road, several motorcyclists are riding away from the viewpoint, and a white car is also visible in the distance. The road surface is marked with white dashed lines. The overall scene is bright and sunny, suggesting a clear day.

![Kannada Caption](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-caption-road.jpg)

### Kannada Caption

output

ಈ ಚಿತ್ರವು ಒಂದು ವಿಶಾಲವಾದ ಡಾಂಬರು ರಸ್ತೆಯನ್ನು ತೋರಿಸುತ್ತದೆ, ಇದು ಬಹುಶಃ ಒಂದು ಹೆದ್ದಾರಿಯಾಗಿರಬಹುದು. ರಸ್ತೆಯ ಎಡಭಾಗದಲ್ಲಿ ದಟ್ಟವಾದ ಹಸಿರು ಮರಗಳ ಸಾಲು ಇದೆ, ಇದು ರಸ್ತೆಯ ಮೇಲೆ ನೈಸರ್ಗಿಕ ಮೇಲ್ಛಾವಣಿಯನ್ನು ಸೃಷ್ಟಿಸುತ್ತದೆ. ಮರಗಳ ಪಕ್ಕದಲ್ಲಿ ತಿಳಿ ನೀಲಿ ಬಣ್ಣದ ಲೋಹದ ಬೇಲಿ ಮತ್ತು ಒಂದು ಸಣ್ಣ ನೀಲಿ ಬಣ್ಣದ ಕಸದ ಬುಟ್ಟಿ ಇದೆ. ರಸ್ತೆಯ ಬಲಬದಿಯಲ್ಲಿ, ದೂರದಲ್ಲಿ ಕೆಲವು ಜನರು ಮೋಟಾರ್ ಸೈಕಲ್ಗಳಲ್ಲಿ ಪ್ರಯಾಣಿಸುತ್ತಿರುವುದನ್ನು ಕಾಣಬಹುದು. ರಸ್ತೆಯ ಮೇಲೆ ಬಿಳಿ ಬಣ್ಣದ ಗೆರೆಗಳನ್ನು ಗುರುತಿಸಲಾಗಿದೆ. ಆಕಾಶವು ಪ್ರಕಾಶಮಾನವಾಗಿದ್ದು, ಇದು ಬಿಸಿಲಿನ ದಿನವನ್ನು ಸೂಚಿಸುತ್ತದೆ.

![OCR in the wild](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-ocr-in-the-wild.jpg)

### OCR in the wild

output

જાહેર નોટીસ આથી આ જાહેર નોટીસ થી જાણ કરવા માં આવે છે કે સદરહુ ઓડા ધ્વારા ફાળવવામાં આવેલ પ્લોટ ઉપર કોઈએ ઘન કચરો (સોલીડ વેસ્ટ) નાખવો નહી સદરહુ જગ્યા ઉપર કચરો નાખનાર સામે ગામ પંચાયત અસલાલી ધ્વારા કાયદેસર ની કાર્યવાહી હાથ ધરવામાં આવશે જેની નોંધ લેશો. સરપંચ શ્રી અસલાલી ગ્રામ પંચાયત

![Structured information extraction in the wild](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-structured-extraction.jpg)

### Structured information extraction in the wild

output

| STA | ETA | Airline | Flt No | Origin | Status | | :---: | :---: | :--- | :--- | :--- | :--- | | 02:00 | 01:29 | IndiGo | 6E 6256 | ಕೋಲ್ಕತಾ | ಆಗಮಿಸಿದೆ | | 02:00 | 01:56 | IndiGo | 6E 5284 | ಮುಂಬಯಿ | ಆಗಮಿಸಿದೆ | | 02:05 | 02:01 | IndiGo | 6E 996 | ಅಹಮದಾಬಾದ್ | ಆಗಮಿಸಿದೆ | | 02:10 | 02:10 | IndiGo | 6E 1723 | ದೋಹಾ | ಸರಿಯಾದ ಸಮಯ | | 02:20 | 02:00 | QATAR | QR 572 | ದೋಹಾ | ಬೇಗ ಆಗಮಿಸುತ್ತಿದೆ | | 02:20 | 02:10 | IndiGo | 6E 361 | ಪುಣೆ | ಸರಿಯಾದ ಸಮಯ | | 02:30 | 02:35 | Emirates | EK 568 | ದುಬೈ | ಸರಿಯಾದ ಸಮಯ | | 02:50 | 02:50 | AirArabia | G9 496 | ಶಾರ್ಜಾ | ಸರಿಯಾದ ಸಮಯ | | 03:05 | 03:05 | ETIHAD | EY 216 | ಅಬುಧಾಬಿ | ಸರಿಯಾದ ಸಮಯ | | 03:05 | 02:41 | IndiGo | 6E 2403 | ದೆಹಲಿ | ಬೇಗ ಆಗಮಿಸುತ್ತಿದೆ |

![Student Handwriting Recognition](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-student-handwriting.jpg)

### Student Handwriting Recognition

output

APJ Abdul Kalam was a great scientist and leader from India. He loved science and worked hard to make rockets and missiles. He was also known as "Missile Man". He became India's President in 2002 and was affectionately called the "People's President". Kalam played a pivotal role at the Defence Research and Development Organization (DRDO) and ISRO. He was the brain behind India's indigenous missile development, leading projects like Agni and Prithvi.

### Edge Cases

While the performance of the models are significantly better than other models for Indian languages; it is not perfect. We did find edge cases - a few of them are shared here. Incorrect translation of the Bengali script while describing the image.

![Incorrect translation of the bengali script while describing the image.](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-bengali-storefront.jpg)

### Incorrect translation of the bengali script while describing the image.

output

The image shows the storefront of a shop named "Doyamondilibrerii," which translates to "Doyamond Library." The shop is located in Kolkata, as indicated by the address "368, Rabindra Sarani, Kolkata-6" on the signboard. The signboard is black with white Bengali script. Above the shop, there is a balcony with a red metal railing and green shutters. The building's facade is painted pink, and there are decorative carvings on the left side. A black electrical wire runs across the front of the building. The shop appears to be a local bookstore or library.

![A low resource Indic Language](https://assets.sarvam.ai/Blogs/sarvam-vision/vision-low-resource-indic.jpg)

### A low resource Indic Language

output

The image depicts a busy street scene in an urban area. There are two auto-rickshaws, one black and one green, driving on the road. Several people are walking on the street, and there are various shops and buildings on either side of the street. The sky is blue with some clouds.

For the above image, the model was prompted to describe the scene in Santhali (a low-resource Indian language). Instruction following for such long-tail requests can be low quality.

## **Experience Sarvam Vision & Get Started with Document Intelligence API Today**

Sarvam Vision’s Document Intelligence is built to handle real-world, production-grade workloads and we’re just getting started! To kick things off and accelerate adoption, we’re making the Document Intelligence APIs & Vision experience **completely free** for the **entire month of February, 2026**. This is your chance to push the model to its limits, experiment at scale, and start building with zero friction.

**_Want to try it right away?_** Jump into our no-code, interactive experience on the Sarvam API Platform. Simply log in and enjoy unlimited usage for the month of February![![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32)https://dashboard.sarvam.ai/](https://dashboard.sarvam.ai/)

**Ready to integrate into your product?** Head over to our API Developer Docs for ready-to-use SDKs, clear examples, and everything you need to get production-ready in minutes.

**Building something exciting?** Join our Discord Developer Community to stay up to date on new releases, share feedback, and collaborate directly with the Sarvam team.

We’re excited to work closely with developers and partners to build on this strong foundation and unlock powerful downstream applications across education, healthcare, video intelligence, and more. Now’s the time to explore, experiment, and build with Sarvam Vision.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
