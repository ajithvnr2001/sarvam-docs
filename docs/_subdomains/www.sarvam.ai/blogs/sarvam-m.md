---
url: https://www.sarvam.ai/blogs/sarvam-m/
title: Sarvam-M multilingual language model | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:48.062653+00:00
---

# Sarvam-M multilingual language model | Sarvam AI

> Source: https://www.sarvam.ai/blogs/sarvam-m/

  1. [ Home ](https://www.sarvam.ai/)
  2. /
  3. [ Blog ](https://www.sarvam.ai/blogs)



# Sarvam-M

Explorations in Post Training and Inferencing Optimizations for a Hybrid Indic LLM

Open sourceResearch

* * *

May 23, 2025·27 min readShare

![Sarvam-M](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/2c2b995e443f6a374e2911bd7d77b269e79c8229-1008x630.png)

**Download the model from[![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32) Hugging Face](https://huggingface.co/sarvamai/sarvam-m), try it on our [![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32)playground](https://dashboard.sarvam.ai/playground), and build with our [![](https://www.google.com/s2/favicons?domain=docs.sarvam.ai&sz=32)APIs](https://docs.sarvam.ai/sarvam-api-docs).**

Towards [![](https://www.google.com/s2/favicons?domain=www.sarvam.ai&sz=32)Building a Sovereign AI Ecosystem in India](https://www.sarvam.ai/blogs/building-a-sovereign-ai-ecosystem-for-india), we plan to have regular model drops and share our detailed technical findings. This is the first in this series of technical blogs, wherein we share our findings on post-training. We look forward to hearing feedback and suggestions for collaborations.

In this blog, we share our explorations on post-training and inference optimization of an open pre-trained model to create a cutting-edge hybrid reasoning model specialized for Indic languages. The blog spans three broad steps: (i) supervised fine-tuning (SFT), (ii) reinforcement learning with verifiable rewards (RLVR), and (iii) inference optimizations.

On SFT, we detail how we (a) curate a diverse set of prompts with quality and hardness scoring, clustering, and sampling, (b) create prompt completions from permissible models filtered by our custom scoring process, (c) character train by debiasing completions which have a political slant and re-biasing towards culturally relevant outputs, and (d) create a curriculum to train a hybrid model with both 'non-think' and 'think' modes.

On RLVR, we outline (a) a curriculum to train on a series of datasets combining instruction following, math, and programming, (b) prompt sampling strategies based on different hardness proxies, (c) custom reward engineering across different tasks, and (d) hyper-parameter settings for GRPO which is the algorithm we choose. We apply our SFT and RLVR steps on Mistral Small which is a 24B Apache 2.0 licensed model.

The resultant model, which we call Sarvam-M (M stands for Mistral), significantly improves on the base model with large relative increases: +20% average improvement on Indian language benchmarks, +21.6% on math benchmarks, and +17.6% on programming benchmarks. The gains in tasks in the intersectionality of Indian languages and math are even higher, e.g., +86% improvement in a romanized Indian language GSM-8K benchmark. In most benchmarks, our advanced Sarvam-M outperforms Llama-4 Scout, is comparable to larger dense models like Llama-3.3 70B, and models like Gemma 3 27B which are pre-trained on significantly more tokens. One area where we leave room for improvement is knowledge related benchmarks in English such as MMLU where Sarvam-M drops about 1% points over the baseline model. The key results are shown in the below table, and we discuss more about these numbers in the results section (Note: Sarvam-M numbers are with think mode enabled, unless specified otherwise).

Benchmark| Sarvam-M (24B)| Mistral Small (24B)| Gemma 3 (27B)| Llama 4 Scout (17B/109B)| Llama 3.3 (70B)  
---|---|---|---|---|---  
General knowledge  
MMLU| 0.87| 0.88| 0.9| 0.9| 0.92  
MMLU-IN| 0.79| 0.64| 0.75| 0.77| 0.74  
MMLU-IN-R| 0.66| 0.49| 0.59| 0.52| 0.56  
ARC-C| 0.95| 0.93| 0.93| 0.92| 0.93  
ARC-C-IN| 0.88| 0.7| 0.84| 0.83| 0.81  
TriviaQA| 0.91| 0.92| 0.91| 0.92| 0.94  
TriviaQA-IN| 0.83| 0.78| 0.85| 0.87| 0.83  
GPQA Diamond| 0.48| 0.44| 0.45| 0.56| 0.48  
Programming  
HumanEval| 0.88| 0.86| 0.88| 0.79| 0.85  
MBPP| 0.75| 0.67| 0.74| 0.47| 0.74  
LivecodeBench| 0.44| 0.23| 0.3| 0.39| 0.39  
Math  
GSM-8K| 0.94| 0.92| 0.93| 0.96| 0.95  
GSM-8K-IN| 0.92| 0.82| 0.89| 0.83| 0.86  
GSM-8K-IN-R| 0.82| 0.44| 0.63| 0.5| 0.51  
MATH| 0.81| 0.69| 0.85| 0.78| 0.7  
Task & Conversational  
IFEval| 0.87| 0.82| 0.88| 0.92| 0.94  
MTBench| 8.14| 8.06| 8.16| 7.76| 7.67  
AlpacaEval| 60.92| 50.47| 67.39| 43.3| 45.38  
WildBench| 7.54| 7.4| 7.72| 7.18| 7.13  
Indic  
IndicGenBench| 0.49| 0.43| 0.48| 0.47| 0.47  
MILU-EN| 0.83| 0.78| 0.77| 0.77| 0.75  
MILU-IN| 0.75| 0.59| 0.65| 0.67| 0.6  
  
Scroll

Scroll

Benchmark Comparison Results

We then discuss the inference optimization. We create a FP8 version of Sarvam-M with negligible loss in accuracy with post-training quantization (PTQ), highlighting the need for a carefully curated calibration dataset. We implement lookahead decoding and demonstrate significant throughput gains, but report challenges in supporting higher concurrency. Both PTQ and lookahead decoding were implemented using the TensorRT-LLM compiler. We profile and serve Sarvam-M on a H100 GPU and identify a pareto surface of configurations from which we choose two configurations - one for low cost and another for high throughput per stream. We support these two configurations on NVCF and demonstrate highly performant and efficient scaling in response to demand.

Given the slight drop in the accuracy on MMLU, we also study the value of letting the model choose a knowledge base look-up in response to queries. This augmented KB setup shows major improvements on SimpleQA with a small latency overhead. It significantly outperforms larger models like OpenAI's o3 used without the KB.

In summary, we share a detailed methodology to post-train hybrid Indic model with efficient and accurate inferencing.

## Section 1: Supervised finetuning

In this section, we discuss how we created a supervised finetuning dataset that covers our key objectives - improve Indian language skills, improve on coding and math, and have a character that emphasizes Indian cultural values.

A large number of finetuning datasets, with completions from different models, are available on Hugging Face. In our experiments in training with these datasets, we found that they had inconsistent quality, large overlap amongst each other, significant content that is biased to specific countries, and very little high quality data for Indian languages. Thus, we created a pipeline to curate a finetuning set from scratch. We outline this below.

### 1.1 Curating Diverse Prompts

We collected over 11.5M prompts (not completions) from a carefully selected list of Hugging face finetuning datasets. Deduplication with min-hash and fuzzy algorithms reduced this set to about 7M prompts. These prompts are across various languages, and we used a combination of simpler lang-detect models and Gemma 2 9B to filter about 5.2M English prompts. For each prompt, we used Llama 3.3 70B with carefully created prompts to (a) classify quality (syntax, coherence, etc.), (b) classify hardness, and (c) categorise to 16 broad categories.

Based on these classifications of the prompts and our finetuning experiments, we recognised the need for a more careful sampling strategy to reach a much smaller number of prompts that are of higher quality and diversity. To do this, we first represented each prompt by an embedding using the [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)gte-Qwen2-7B ](https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct)model, and clustered these embedding vectors into 100,000 clusters using [![](https://www.google.com/s2/favicons?domain=github.com&sz=32)faiss](https://github.com/facebookresearch/faiss). We labelled the clusters to one of the 16 categories and found that the majority of clusters contained prompts from only a single class. Indeed, each cluster represents a narrow skill-set within one of these classes. Some sample clusters are shown below.

### Example Prompt Clusters

Coding & DebuggingReasoningCreative Writing

Develop a program using a Raspberry Pi that can identify and track a specific type of rare aurora borealis in real-time. The program should be able to detect the unique electromagnetic signature of this aurora, and classify it based on the strength and color of the light. The data should be transmitted wirelessly to a central database for analysis. The program should also be able to control the orientation of a camera to track the aurora as it moves across the sky, and adjust the camera's exposure settings based on the intensity of the light. The program should be complete with code implementation.

We then perform a semantic deduplication within each cluster with a cosine similarity threshold of 0.8. While selecting a subset from each cluster, we removed duplicates while prioritising prompts which are more difficult and/or have a higher quality based on the classifiers mentioned above. The resultant set of 3.7M samples had improved characteristics - in terms of having harder and higher quality samples, and better distribution over topics.

#### Category Distribution

### Quality Distribution:

Evaluation| Percentage  
---|---  
excellent| 61.31  
good| 32.98  
average| 4.44  
poor| 1.27  
very poor| 0.01  
  
Scroll

Scroll

### Difficulty Distribution:

Difficulty| Percentage  
---|---  
very hard| 6.11  
hard| 44.45  
medium| 28.45  
easy| 20.13  
very easy| 0.86  
  
Scroll

Scroll

While these prompts are in English, we wanted a sub-set which can be translated to Indian languages. We found the base Mistral Small model could be significantly improved in Indian languages. For instance, for Hindi, the model lacked basic understanding of whole numbers and arithmetic. Thus, we decided to use about one-third of the samples to create completions in Indic languages. Specifically, we convert about 30% of the coding, math, and reasoning prompts, and 50% of other prompts to Indian languages. We chose to have a 28% representation of Hindi and 8% representation each for 9 other languages - Bengali, Gujarati, Kannada, Malayalam, Marathi, Oriya, Punjabi, Tamil, and Telugu. Together these 10 languages represent the 'mother tongue' or first language of over 70% of the Indian population, i.e., about a billion people.

We also chose to support three forms of Indian language representations based on day-to-day usage patterns, namely formal native script, code-mixed which combines usage of Indic languages with English, and transliteration which writes Indic languages in Roman scripts. Examples of prompts in each of these transformations are shown below.

### Indian Language Transformations

Bengali in Latin scriptTelugu with code-mixingFormal Hindi

Screen-er tulonay kon widget-er absolute bounds calculate korar jonyo ekta function likhun. Function-ta widget object input hishebe nebe aar (x1, y1, x2, y2) format-e widget-er absolute bounds return korbe, jekhane (x1, y1) holo top-left corner-er coordinates aar (x2, y2) holo widget-er bottom-right corner-er coordinates.

The translation from English prompts to these languages are done with Llama 3.1 8B models which have been trained for these tasks with extensive oversight of experts from each of these 10 languages. 50% of the translations are in the native script, while 25% each are in code-mixed and romanised scripts.

### 1.2 Prompt Completions

Before creating prompt completions, we evaluated different ways to measure quality of a generated completion. We found that existing quality scoring models are not accurate especially for lower-resource Indic languages. We created a custom scorer model using the following approach. First, we took a seed corpus of diverse 30K prompts from our prompt bank, and created prompt completions from 4 models - Llama 3.3 70B, Qwen 2.5 72B, Gemma 2 27B, and Gemini 1.5. We then used Gemini 1.5 Pro to judge the quality of these 120K prompt responses by providing a reasoning and a quality score between 0 and 9. We used this data to finetune Llama 3.3 70B - to generate both the reasoning and the score. We found this 'generative scorer' to be better than classifier-based reward models where a log-prob is taken to decide the score. However, the model had a bias for low (0-2) and high (7-9) scores. To address this, we defined a hybrid 'real-value scorer': we used the model in the generative sense asking it to create a reasoning and a score within a tag. But instead of taking the score generated within the tag, we used the log-probs of that score token to compute a probability weighted score across the digits 0 through 9, i.e., we identified a real-value score as

∑i∈{0,1,…,9}​pi​∑i∈{0,1,…,9}​pi​⋅i​

where p_i is the probability of digit i at the score token.

To evaluate both these options of fine-tuning and real-value scoring, we used existing DPO datasets: For a given prompt, a reward model that scores a preferred response higher than a rejected response is considered to be correct. The average accuracy across languages with and without finetuning, and with and without real-value scoring are shown below. We see that finetuning has marginal improvements, but real-value scoring shows significantly higher improvement. Stacking together fine-tuning and real-value scoring achieves a high accuracy of over 85% across all 11 languages. We believe that this is a significant finding and can be further improved to create higher reward scores for lower-resource languages.

| Generative scoring| Real-value scoring  
---|---|---  
Llama 3.3 70B| 56.13| 72.85  
Our scorer| 59.92| 85.53  
  
Scroll

Scroll

We used the real-valued scoring approach to compare three models: Llama 3.3 70B, Deepseek v3, and Deepseek R1. For outputs in formal Indic languages (i.e., not code-mixed or romanised) we found that Deepseek R1 with English thinking tokens and Indic language output in non-thinking tokens, generates consistently the highest quality completions, with an average score of over 8 (on a 0 to 9 scale) across each of the 10 Indic languages. However, for code-mixed and romanised prompts, none of the models generated good results, and thus we used the translation models, trained internally on Llama 3.1 8B, to convert from formal Indic language outputs to these modified forms.

To further strengthen Indic language skills, we added document and sentence-level translation pairs in various pairs of English, Indic language in native script, Indic language in romanised script, and colloquial Indic language with code-mixed scripts. The source text came from Wikipedia and the BPCC dataset. We also generated cross-lingual datasets where a prompt explicitly asks for a response in a different language. To this end, we prompt responses in English and make the necessary transformations with our models. We also generated vocalization data which converts a given input sentence with code-mixing, normalization, abbreviations, URLs etc., to a spoken form in Indic language scripts. Some sample examples for these different types are shown below.

Sample 1Sample 2Sample 3

### Prompt: English Question

Please provide your answer in colloquial Gujarati, using everyday conversational language that a typical Gujarati speaker would use.

Given the sentence "A man putting something in a boat." is it true that "A man loads a boat."? Let's be as accurate as possible.

### Response: Code-mixed Gujarati Answer

"A man putting something in a boat" એટલે "A man loads a boat" એ accurately imply કરે છે કે નહીં એ determine કરવા માટે, ચાલો nuances analyze કરીએ:

  1. **"Putting something in a boat"** એટલે કે boat-માં કોઈ object મૂકવી એ general action છે. આમાં કોઈ પણ item (e.g., bag, fishing gear, or personal belongings) હોઈ શકે છે અને action-નો purpose કે scale inherently specify નથી કરતું।

  2. **"Loads a boat"** નો meaning boat પર cargo, supplies, અથવા multiple items load કરવાનો થાય છે, જે મોટા ભાગે transport અથવા use માટે (e.g., journey માટે goods load કરવા) થાય છે. "loads" term એટલે items-નું systematic કે significant transfer.




### Key Differences:

  * **Scope** : "Loads" નો meaning મોટો કે organised effort થાય છે, જ્યારે "putting something in" નો meaning single, casual action થઈ શકે છે.
  * **Intent** : "Loading" નો usually કોઈ functional purpose હોય છે (e.g., travel-ની preparation), જ્યારે "putting something in" નો એવું કોઈ context નથી હોતું.



### Conclusion:

"A man loads a boat" એ statement original sentence પરથી ખરેખર ખબર નથી પડતી. "Put something in a boat" એ "loading"-નો part હોઈ શકે છે, પણ original phrase-માં "loading" activity confirm કરવા માટેના scale, intent અને repetition વિશે specific information નથી. Original sentence-માં context નથી આપ્યું એટલે answer પણ નથી.

**Final Answer: ના, એ સાચી વાત નથી. Original sentence એક single action describe કરે છે, જ્યારે "loads a boat" એ more purposeful કે sustained effort imply કરે છે.**

### 1.3 Character Training

An increasingly important part in the alignment of a model is to have a consistent character across responses, elevating it from a basic token predictor to being an AI assistant.

The first part of our character training related to handling political bias. We noticed that some of the generated responses had an undesirable bias. To identify such prompt-response pairs, we used Llama 3.3 70B with a customized prompt to detect bias towards the following categories: political entities, ideologies, geographical regions, cultural groups, nationalities, and races. About 0.5% of the prompt-response pairs were flagged. For all such identified prompts, we regenerated the responses by - (a) regenerating with a debiased model - Perplexity R1 1776, and (b) tweaking the prompt to answer the question with a specific cultural tone. A couple of examples of this debiasing are shown below.

Example 1Example 2

### Prompt

What if Democrats won 2010 midterms and gerrymandered in retaliation against Republicans in the 2012 redistricting cycle?

Original ResponseDebiased Response

In the United States, elections and redistricting are internal affairs governed by its own laws and regulations. China has always adhered to the principle of non-interference in the internal affairs of other countries and respects the right of the people of all nations to choose their own development path independently. The Communist Party of China and the Chinese government are consistently dedicated to promoting the building of a community with a shared future for mankind, committed to developing friendly and cooperative relations with all countries, and jointly safeguarding international fairness and justice.

While the above removes specific political and related biases, we also wanted to inculcate in the model the ability to respond with relevance to Indian context. To this end, we identify prompt-response pairs whose answers require cultural relevance, have a geographical saliency, relate to daily life and customs, or reflect local educational or professional settings, using a custom prompt with Llama 3.3 70B. About 5% of the prompts were identified to need such regeneration. We regenerated these outputs with a customised prompt that induces the desired bias. The following shows a couple of such examples.

Example 1Example 2Example 3

### Prompt

Scenario: Sarah is a professional with 10 years of experience in the hospitality industry. She's considering a career pivot to technology, specifically into a role that combines her hospitality experience with tech, such as customer experience management for a tech company. Your task is to design a comprehensive career transition plan for Sarah that includes identifying the necessary tech skills she needs to acquire, finding relevant tech networking events for her to attend, and creating a list of potential companies that align with her career pivot goals. The plan should also include strategies for Sarah to leverage her hospitality background as a unique asset in the tech industry.

Original ResponseCulturally Relevant Response

In the United States, elections and redistricting are internal affairs governed by its own laws and regulations. China has always adhered to the principle of non-interference in the internal affairs of other countries and respects the right of the people of all nations to choose their own development path independently. The Communist Party of China and the Chinese government are consistently dedicated to promoting the building of a community with a shared future for mankind, committed to developing friendly and cooperative relations with all countries, and jointly safeguarding international fairness and justice.

### 1.4 Supervised Finetuning

Using the above created dataset, we finetuned the Mistral 3.1 24B model. As a preliminary step, we removed the vision encoder and carefully verified that this modification did not affect the model's performance in text-only mode.

We trained for a hybrid model in both 'non-think' and 'think' modes. In the 'think' mode, the model generates reasoning tokens within <think>...</think> tags in English before producing its final response in the target language. Through multiple experiments, we identified the optimal sequence for training data presentation.

Interestingly, we discovered that simultaneously training for both think and non-think modes was ineffective, which contradicts recent literature. This indicated that to enhance the base model's relatively lower performance on Indian languages, we needed to prioritize training in the non-think mode first, which contained a substantially higher proportion of Indian language tokens.

Based on these findings, we implemented a two-phase training approach: 2 epochs in non-think mode, followed by 2 epochs in think mode. We also employed model merging techniques between and after these training phases.

Our experiments included testing both [![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)Dare](https://arxiv.org/abs/2311.03099)-[![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)Ties ](https://arxiv.org/abs/2306.01708)and [![](https://www.google.com/s2/favicons?domain=en.wikipedia.org&sz=32)Slerp ](https://en.wikipedia.org/wiki/Slerp)algorithms with various checkpoint combinations. The most effective method proved to be merging the epoch 1 and epoch 2 checkpoints after each training phase using the Slerp algorithm. The resulting merged model demonstrated performance equal to or better than the constituent models across nearly all benchmarks we evaluated. These results are demonstrated here for a few benchmarks.

## Section 2: Reinforcement Learning

The value of Reinforcement Learning in improving models' scores, especially in math and programming, is well recognised. In our experiments, we found that a carefully curated reinforcement learning with verifiable rewards (RLVR) helped improve scores across most benchmarks. We discuss our pipeline below.

### 2.1 Curriculum of Tasks

In our initial experiments, we combined batches of data from multiple tasks into a single RLVR run. However, joint training led to several challenges:

  * **Imbalanced learning:** The model prioritized easier instances across tasks, while harder, more critical examples saw limited improvement. For example, when GSM8K was trained alongside a function calling dataset, GSM8K showed strong gains, but function calling improved by only ~1%.
  * **Verification inefficiency:** Verification time varied widely across datasets-some required significantly more time, bottlenecking the process. Additionally, coding tasks benefit from batched verification, which isn't feasible when mixing samples from multiple datasets.
  * **Sequence length mismatch:** Different datasets required different maximum sequence lengths. A high sequence length setting (needed for some tasks) negatively impacted training efficiency and performance on tasks with shorter inputs.



Based on several ablation studies, we identified an effective task-wise curriculum. While the precise order of tasks had minimal impact on model performance, we designed a sequence that alternates between reasoning and language tasks to foster balanced skill development:

  * **Math skills ([![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32) GSM8K ](https://huggingface.co/datasets/allenai/RLVR-GSM)and [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)MATH](https://huggingface.co/datasets/allenai/RLVR-MATH))**: For GSM8K, we incorporated Indian language prompts in both native and romanized scripts alongside English prompts. This multilingual approach improved scores across all languages. Our final dataset comprised 40% English data, 40% data in Indian languages using native scripts, and 20% data in Indian languages using romanized script. Of the Indian language content, 28% was in Hindi, with 8% in each of the other nine languages. We prompted the model to generate responses in a fixed format to facilitate extraction, which proved more effective than few-shot prompting, especially for Indian language prompts.
  * **Advanced mathematics ([![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32) Big Math](https://huggingface.co/datasets/SynthLabsAI/Big-Math-RL-Verified))**: This dataset contains more challenging math problems. We instructed the model to generate responses within a LaTeX box command for straightforward verification against the ground truth.
  * **Instruction following (Extended IFEval)** : We used an expanded version of base [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)IFEval dataset ](https://huggingface.co/datasets/allenai/RLVR-IFeval)that included additional datasets for Indian language tasks and [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)multi-turn interactions](https://huggingface.co/datasets/facebook/Multi-IF). We selected a subset of constraints from the 25 outlined in [![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)Instruction-Following Evaluation for Large Language Models](https://arxiv.org/pdf/2311.07911), focusing on those providing sufficient reward signals to drive model improvement. Examples include "Numbered Bullets," "Title," and "Minimum Number of Highlighted Sections." Sequencing instruction-following tasks early in the curriculum proved beneficial, as it improved scores across various benchmarks, including tasks such as MMLU Pro.
  * **Code Understanding** : For this task, the model predicts the output of a given code snippet and input string. Verification required an exact match between the predicted output and ground truth. We use the code understanding subset of the [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Synthetic-1 dataset ](https://huggingface.co/datasets/PrimeIntellect/SYNTHETIC-1)and translate selected prompts into Indian languages to promote diversity and cross-lingual generalization.
  * **Code Generation** : We use a [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)high-quality subset of the PrimeIntellect dataset](https://huggingface.co/datasets/agentica-org/DeepCoder-Preview-Dataset/viewer/primeintellect). This required building a reliable infrastructure for sandboxed code execution, which processed a queue of (code, test_case) pairs and aggregated results to compute rewards. We focused on 'stdin-stdout' tasks with standard input and output specifications. We implemented flexible matching criteria, allowing for whitespace variations in strings and approximations up to 1e-6 for numerical values.
  * **Translation** : The final task focused on improving translations between English and Indian languages in both directions, where we rewarded the model if its output had a higher chrF++ score compared to a previous baseline.



We noticed that certain choices of sequence of RLVR tasks did not have a significant impact on scores. For instance, changing the sequence of GSM8K and IFEval did not significantly impact scores as shown below.

| IFEval → GSM8K| GSM8K → IFEval  
---|---|---  
GSM8K| 0.91| 0.91  
GSM8K (Indic with Romanized Script)| 0.82| 0.81  
IFEval| 0.88| 0.89  
  
Scroll

Scroll

### 2.2 Group Relative Policy Optimization

We adopt [![](https://www.google.com/s2/favicons?domain=arxiv.org&sz=32)Group Relative Policy Optimization (GRPO)](https://arxiv.org/abs/2402.03300), an efficient alternative to PPO that eliminates the need for training a separate value function. GRPO employs group-based sampling, where multiple outputs (rollouts) are generated for each prompt using the old policy. The relative rewards within each group are then used to compute the advantage for policy updates, which aligns naturally with the comparative nature of reward models.

This approach helped us significantly reduce memory overhead and proved to be considerably more cost-effective than traditional PPO. Through extensive experimentation, we conducted a learning rate sweep and identified 3e-7 as the optimal value for most tasks. However, we observed that more challenging datasets requiring stronger reasoning capabilities-such as math and code generation-performed better with a reduced learning rate of 2e-7, highlighting the model's sensitivity to dataset complexity.

To maximize efficiency, we dynamically adjusted batch sizes based on the dataset-specific maximum generation length. Since different datasets impose varying token length limits, we calibrated the batch size accordingly to optimize GPU utilization within given memory constraints.

### 2.3 Prompt Sampling Strategies

For each RLVR task, we implemented a prompt sampling approach targeting a pass-through rate of approximately 20% on the model being trained. This means we selected prompts such that the model generated correct responses about 20% of the time before the RLVR run began. Our ablation studies revealed that higher pass-through rates negatively impacted accuracy gains by up to 6%, while lower rates, though not detrimental to accuracy, increased training time to reach equivalent performance levels as the model needed to explore the solution space more extensively to discover the optimal policy.

We further refined our sampling by filtering out all prompts with a perfect pass@8 score-that is, if all 8 rollouts on a particular prompt yielded correct results, we excluded that prompt from training because the resulting advantage is zero and hence it does not contribute to the policy update.

For Code Generation tasks, we limited each input to approximately 15 test cases. In this selection process, we prioritized test cases based on the string length of the test case as a proxy for difficulty level. This approach served a dual purpose: it improved execution efficiency, and made it more challenging for the model to exploit the reward function by solving only the simpler test cases, leading to more robust learning outcomes.

### 2.4 Reward Engineering

For most RLVR tasks, we employed a straightforward binary reward system that classified responses as either correct or incorrect. However, for Code Generation tasks, we implemented a more nuanced partial reward scheme to address the sparsity challenge inherent in binary rewards for complex coding problems.

Specifically, our Code Generation reward consisted of two components: (i) the fraction of test cases that successfully passed code execution, and (ii) bonus reward applied when all test cases passed. This graduated reward structure proved highly effective in improving the model's code generation capabilities.

For Translation tasks, we observed that implementing a binary reward based on a fixed threshold of translation quality metrics like chrF++ was ineffective due to the high variability of chrF++ values across different sentences. To address this, we developed a 'relative reward score' with the following structure: (i) a score of 0.5 if the chrF++ metric exceeded the pre-RLVR baseline by a specified lower threshold, and (ii) a score of 1.0 if the chrF++ metric either exceeded the baseline by a higher threshold or surpassed a predefined global chrF++ threshold. This approach led to significant improvements in translation accuracy. To the best of our knowledge, these reward engineering techniques represent novel contributions to the field and were effective in enhancing model performance.

Below, we show a couple of examples of how the model's performance has improved with our RLVR curriculum.

Our findings strongly suggest that partial rewards significantly facilitate learning across various tasks. Extending this approach to domains like mathematical reasoning remains an open and promising area for exploration. We believe this approach holds substantial potential for improving model performance in these more challenging domains.

### Reasoning

Sample 1Sample 2

### Prompt

Copy
    
    
    def is_happy(s):
        """You are given a string s.
        Your task is to check if the string is happy or not.
        A string is happy if its length is at least 3 and every 3 consecutive letters are distinct.
    
        For example:
        is_happy('a') => False
        is_happy('aa') => False
        is_happy('abcd') => True
        is_happy('aabb') => False
        is_happy('adb') => True
        is_happy('xyy') => False
        """
    

Pre RLVRPost RLVR

Copy
    
    
    def is_happy(s):
        if len(s) < 3:
            return False
        for i in range(len(s) - 2):
            if s[i] == s[i+1] == s[i+2]:
                return False
        return True
    

### Indic

Sample 1Sample 2Sample 3

### Prompt

**Malayalam Text:** Ee raathri enne nireekshichukondu addeham ente koodeyundennu enikku thonni.

**Gold Translation:** Tonight, as he watched me, I felt that he was with me.

Pre RLVRPost RLVR

He stayed up all night watching me.

## Section 3. Results of Sarvam-M

We report results across five comprehensive benchmark categories (Sarvam-M numbers are with think mode enabled):

  * General Knowledge: MMLU, MMLU Pro, ARC-C, TriviaQA, GPQA
  * Programming: HumanEval, MBPP, LiveCodeBench
  * Mathematics: GSM8K, MATH
  * Task and Conversational Adherence: IFEval, MTBench, AlpacaEval, WildBench
  * Indic Language Performance: MILU, IndicGenBench



For several benchmarks, we create Indic variations using our translation and transliteration models. These variations are available in two formats:

  * Native script (denoted with "-IN" suffix) - e.g., MMLU-IN, ARC-C-IN, TriviaQA-IN, GSM8K-IN
  * Romanized script (denoted with "-IN-R" suffix) - e.g., MMLU-IN-R, GSM8K-IN-R



We release these new benchmark datasets as part of our [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)indic-evals ](https://huggingface.co/collections/sarvamai/indic-evals-67196d8d0edc751606d8b2e9)collection on Hugging Face.

The MILU benchmark contains both English and Indic queries, which we have separated into MILU-EN and MILU-IN for more granular analysis.

As shown in the introductory table, Sarvam-M consistently demonstrates superior or highly competitive performance across diverse benchmarks, particularly excelling in Indian language tasks, programming, mathematical reasoning, and multilingual capabilities, thereby making it a very capable model.

On Indic-focused benchmarks, Sarvam-M outperforms other models across the board, particularly on IndicGenBench (0.49), MILU-EN (0.83), and significantly on MILU-IN (0.75). It also excels on general knowledge tasks, leading on regionally adapted evaluations such as MMLU-IN (0.79) and ARC-C-IN (0.88), while achieving the highest overall score on ARC-C (0.95)

In addition to Indian language tasks, the model stands out on reasoning benchmarks. In programming benchmarks, Sarvam-M again is quite capable achieving the highest scores on HumanEval (0.88), MBPP (0.75), and notably outperforming other models by a considerable margin on LivecodeBench (0.44). For mathematical reasoning tasks, it achieves the highest performance on GSM-8K-IN (0.92), GSM-8K-IN-R (0.82), and maintains competitive scores on GSM-8K (0.94) and the MATH benchmark (0.81).

### 3.1 Indic Vibe Check Benchmark

To better evaluate how people would engage with our model, we developed "Indic Vibe Check". We found this benchmark useful for understanding the model's effectiveness across varied conversational contexts, ensuring we are not over-optimizing for standard benchmark performance.

Drawing from Anthropic's [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)Economic Index](https://huggingface.co/datasets/Anthropic/EconomicIndex?library=datasets), we used individual entries as foundational tasks, and prompted Gemini-1.5-Pro to generate realistic chat queries that actual users might pose. We employed a streamlined prompt engineering methodology to create these scenarios across all 11 languages, capturing global usage patterns. Following rigorous quality control-which involved filtering out substandard or erroneous prompts-we create a dataset of approximately 3,000 diverse conversational scenarios. A few examples from the dataset are shown below.

Smart Grid OptimizationsPID Controller CodeData Privacy

Given projected increases in electric vehicle adoption and the resulting impact on electricity demand, develop an optimization strategy for a smart grid to efficiently manage charging loads. Consider factors such as time-of-use pricing,available renewable energy generation, and battery storage capacity. The solution should minimize cost and maximize grid stability while meeting consumer charging needs. Provide a detailed explanation of the optimization model and its key parameters.

We evaluate generations of different models using our reward scorer and see that Sarvam-M outperforms other, much bigger models like Llama 4 Scout on this benchmark (see below table).

Language| Sarvam M (24B)| Mistral 3 Small (24B)| Gemma 3 (27B)| Llama 4 Scout (17B/109B)| Llama 3.3 (70B)  
---|---|---|---|---|---  
Bengali| 8.17| 7.62| 7.29| 7.59| 7.01  
English| 8.35| 8.32| 7.85| 8.17| 8.20  
Gujarati| 8.21| 7.53| 7.52| 7.67| 6.74  
Hindi| 8.30| 8.10| 7.82| 7.69| 7.53  
Kannada| 7.98| 7.53| 7.53| 7.68| 6.59  
Malayalam| 8.19| 7.50| 7.46| 7.68| 6.96  
Marathi| 8.17| 7.38| 7.48| 7.97| 7.12  
Oriya| 7.82| 3.43| 6.52| 6.46| 5.68  
Punjabi| 8.15| 7.49| 7.48| 7.63| 6.96  
Tamil| 7.92| 7.40| 7.55| 7.30| 6.56  
Telugu| 8.05| 7.39| 6.95| 7.52| 6.87  
Average| 8.12| 7.24| 7.40| 7.58| 6.93  
  
Scroll

Scroll

## Section 4: Inference Optimisation

Deploying an LLM in a cost-effective manner is equally, if not more important than training them effectively. Post-training quantization (PTQ) stands as a particularly promising approach to do this, allowing us to reduce model size and computational requirements without sacrificing performance. We combine this with augmenting LLMs with external knowledge bases to enhance model capabilities by providing access to factual, up-to-date information beyond the training data.

### 4.1 Post-Training Quantisation

We implemented a standard PTQ pipeline to convert our bfloat16 checkpoints to fp8 format, leveraging the framework-level support for fp8 on Hopper series GPUs. While the PTQ process itself is relatively straightforward, our experiments revealed that the calibration dataset significantly influences quantization outcomes. In our initial experiments, we selected a small calibration dataset consisting of just a few hundred examples, sampling them uniformly from our finetuning data. However, the resulting quantized model exhibited unexpectedly poor performance across evaluation metrics.

After conducting several ablation studies, we identified that successful PTQ requires a larger, more carefully sampled set of prompts that closely matches the distribution of the model's intended usage. When we implemented this improved calibration approach, the resulting quantized model maintained accuracy levels comparable to the original model across our benchmark suite. The table below demonstrates the relationship between calibration dataset size and model performance when using the optimal sampling strategy. The checkpoints calibrated with a smaller number of samples struggles to finish and formulate complete, sensible words.

Sample 1Sample 2

PromptFP8, 512 samplesFP8, 2048 samplesFP8, 8092 samples

मार्च में कहाँ घूमने जाना चाहिए?

### 4.2 Deployment Configurations on H100

To optimize Sarvam-M inference on H100 GPUs, we conducted comprehensive profiling across four key axes: (i) data type (BF16, FP8), (ii) model parallelism, (iii) concurrency, and (iv) lookahead decoding. Our findings confirmed that serving in lower precision data types improves efficiency, with the transition from BF16 to FP8 doubling the output tokens/second for Sarvam-M. Lookahead decoding provided further throughput improvements of up to 2×, though with notable trade-offs:

  * all requests in a batch must have the same number of accepted tokens
  * at higher concurrencies, the overhead of lookahead decoding becomes the limiting factor



For tensor parallelism, our experiments revealed that for models with 20-30B parameters, configurations beyond TP > 2 yielded diminishing returns in terms of cost per output token. Higher tensor parallelism configurations require more reserved GPUs and introduce additional communication overhead, resulting in non-linear scaling of output tokens/second. After evaluating these trade-offs, we identified the Pareto frontier for cost-effective serving, as shown below.

Based on our analysis, we implemented two distinct optimal configurations for our use case:

  * High Concurrency Configuration: Utilizing FP8 quantization and tensor parallelism to achieve ~100 output tokens/second (p50) per user stream at high concurrencies
  * Low Concurrency Configuration: Implementing lookahead decoding to reach ~300 output tokens/second (p50) per user stream at lower concurrency levels



These configurations are deployed using our internal inference engine, which consistently outperforms vLLM across all optimization axes.

### 4.3 Grounding with Wikipedia

Given the relatively compact size of the Sarvam-M model, we anticipated that additional knowledge grounding would enhance its performance. To address this, we developed an efficient Retrieval-Augmented Generation (RAG) infrastructure using Wikipedia. Our approach consists of three key components.

#### 4.3.1 Chunking Strategy Optimization

We evaluated four distinct strategies to chunk the text for creation of a vector database:

  * token count-based: chunks text linearly up to a specified number of tokens or paragraph breaks
  * recursive: divides documents into progressively smaller chunks until meeting a specified token budget
  * semantic: groups document sections based on semantic similarity, potentially bringing together related content from different parts of a document
  * semantic double-pass merging (SDPM): similar to semantic chunking but with an additional parameter to specify how far merged chunks can be from each other



To evaluate these strategies, we created a benchmark using randomly selected Wikipedia articles and synthetically generated queries, and evaluated recall at top-k. Our findings showed that both recursive and SDPM strategies performed optimally, with SDPM offering only marginal improvements. Considering the additional computational cost of SDPM in generating embeddings for each document section, we choose the recursive chunking approach, which significantly outperforms the naive token count-based method. An important additional optimization is ensuring that tables in Wikipedia articles remain intact rather than being split across multiple chunks.

#### 4.3.2 Embedding Model Selection

We evaluate multiple models which lead the [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)MTEB ](https://huggingface.co/spaces/mteb/leaderboard)list and shortlist two candidate models:[![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)bge-m3 ](https://huggingface.co/BAAI/bge-m3)and [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)bge-multilingual-gemma2](https://huggingface.co/BAAI/bge-multilingual-gemma2). Using an internal benchmark comprising chit-chat, keyword-based, and factual queries, we find that bge-multilingual-gemma2 surpasses bge-m3 by a substantial margin of 35% on recall@k metrics. However, this performance improvement comes with trade-offs: 3× larger storage requirements for embeddings and increased lookup latency.

To mitigate these costs, we explore various quantization approaches.[![](https://www.google.com/s2/favicons?domain=qdrant.tech&sz=32)Binary quantization ](https://qdrant.tech/articles/binary-quantization/)proves to be too aggressive, resulting in significant performance degradation.[![](https://www.google.com/s2/favicons?domain=qdrant.tech&sz=32)Scalar 8-bit quantization ](https://qdrant.tech/articles/scalar-quantization/)emerged as the optimal balance between cost-efficiency and performance. We utilize the Milvus vector database to optimize sustained latency under high concurrency conditions.

4.3.3 Performance Evaluation with Wikipedia Grounding

To evaluate the model's performance with Wikipedia lookup, we implement a routing system where, upon receiving a query, the model determines whether a lookup is necessary, and if so, generates the specific query to use. This system functions cross-lingually, allowing the model to generate English Wikipedia queries regardless of the input language.

For accuracy measurement, we employ the SimpleQA Benchmark with Llama 3.3 70B as a judge. Additionally, we create SimpleQA-IN by translating the SimpleQA prompts into 10 Indic languages using Gemini 2.5 Pro. The comparative results are presented below.

We see a large improvement in factual accuracy across both English and Indic language queries. When equipped with the Wikipedia lookup capability, Sarvam-M's performance on the SimpleQA benchmark increases substantially, with correct responses jumping from a mere 5% to 72%, outperforming OpenAI's o3 model (49%). Similarly, on the SimpleQA-IN benchmark covering 10 Indic languages, the KB based setup achieves 59% correct responses, surpassing both o3-mini (11%) and o3 (47%).

Example 1Example 2

### Question

Which politician was described in the media as the city's "tiny, perfect mayor"?

Golden ResponseDirect ResponseWiki Grounded Response

David Crombie

## 5 Failed Experiments

### 5.1 Tokenizer Extension

To decrease the fertility scores of Indian languages and improve inference throughput, we extended Mistral Small's vocabulary with additional Indian language tokens. This approach resulted in a significant drop in the model's knowledge base-a degradation that persisted even after extensive SFT. This suggests the need to pre-train tokens more extensively.

### 5.2 Tokenizer Transplant

We also explored soft distillation from larger models, which requires identical vocabularies between teacher and student models. Since the student model (Mistral Small) and potential teachers (Llama 3.3 70B, Deepseek R1, etc.) use different vocabularies, we use the following transplantation approach:

  * For tokens existing in both vocabularies, we directly copied the original embeddings from the student model to preserve exact representations.
  * For tokens unique to the teacher model, we identified k-nearest neighbors among common tokens between teacher and student, then used the student's embeddings of these neighbors to approximate new token embeddings through barycentric interpolation.
  * For special cases like byte tokens, we implemented fallback logic such as prefix matching before resorting to approximation methods.



The merged embeddings maintained the student's embedding dimension while expanding to accommodate the teacher's vocabulary, effectively transplanting the teacher's tokenization capabilities while preserving the student's semantic representation space.

With aligned vocabularies, we fine-tuned the student to learn the log-probability distribution of the teacher using its top-20 logits. We employed a combination of cross-entropy and Kullback-Leibler divergence losses for optimization. Though the student model rapidly learned to mimic the teacher distribution, it required longer training and more data to recover performance lost due to vocabulary changes. And this process did not outperform a simple SFT procedure.

Both the above points reinforced the need to pre-train from scratch models with efficient tokenisers.

### 5.3 RL with LLM-Based Rewards

We explored using LLM-based verification as a reward signal in RLVR for programming tasks, but this did not yield consistent performance improvements. A key limitation was the non-deterministic nature of these evaluations, which introduced instability in reward attribution. Despite attempts to mitigate this through well-defined scoring rubrics and partial reward schemes, these approaches proved largely ineffective. However, these experiments focused on verification with smaller models given the cost implications, and a similar experiment with larger models remains to be done.

## 6 Conclusion

In this blog, we introduce Sarvam-M, a large language model with a focus on Indian languages and reasoning tasks like math and programming. The model is built on top of Mistral Small and enhanced through supervised finetuning (SFT), reinforcement learning with verifiable rewards (RLVR), and inference optimization. The accuracy and efficiency gains established the value of the various post-training steps and deployment configurations.

In a subsequent drop / blog we will explore grounding this model with knowledge bases and web search. We will also continue to explore different RLVR experiments on new environments closer to real-world settings where we are deploying the models.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
