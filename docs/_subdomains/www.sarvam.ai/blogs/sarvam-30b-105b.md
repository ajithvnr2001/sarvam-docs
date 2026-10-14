---
url: https://www.sarvam.ai/blogs/sarvam-30b-105b/
title: Open-sourcing Sarvam 30B & 105B models | Sarvam AI
method: scrapling+scrapegraph
fetched_at: 2026-10-14T08:15:47.573791+00:00
---

# Open-sourcing Sarvam 30B & 105B models | Sarvam AI

> Source: https://www.sarvam.ai/blogs/sarvam-30b-105b/

  1. [ Home ](https://www.sarvam.ai/)
  2. /
  3. [ Blog ](https://www.sarvam.ai/blogs)



# Open-Sourcing Sarvam 30B and 105B

ResearchOpen source

[Download Now](https://www.sarvam.ai/download-sarvam-105b-model)

* * *

Mar 6, 2026·18 min readShare

![Open-Sourcing Sarvam 30B and 105B](https://assets.sarvam.ai/tr:w-1600,q-90,f-auto,dpr-auto/images/03117ysv/production/ef7fefef0603837a95a8ad4547cb5def4818dbe9-2016x1260.png)

We're releasing Sarvam 30B and Sarvam 105B as open-source models. Both are reasoning models trained from scratch on large-scale, high-quality datasets curated in-house across every stage of training: pre-training, supervised fine-tuning, and reinforcement learning. Training was conducted entirely in India on compute provided under the IndiaAI mission. These models represent a true full-stack effort. Beyond datasets, we optimized tokenization, model architecture, execution kernels, scheduling, and inference systems to make deployment efficient across a wide range of hardware, from flagship GPUs to personal devices like laptops. Both models are already in production. Sarvam 30B powers [![](https://www.google.com/s2/favicons?domain=www.sarvam.ai&sz=32)Samvaad](https://www.sarvam.ai/products/conversational-agents), our conversational agent platform. Sarvam 105B powers [![](https://www.google.com/s2/favicons?domain=links.sarvam.io&sz=32)Indus](https://links.sarvam.io/indus-app), our AI assistant built for complex reasoning and agentic workflows.

The Sarvam models are globally competitive for their class. Sarvam 105B performs well on reasoning, programming, and agentic tasks across a wide range of benchmarks. Sarvam 30B is optimized for real-time deployment, with strong performance on real-world conversational use cases. Both models achieve state-of-the-art results on Indian language benchmarks, outperforming models significantly larger in size.

This release marks an important milestone for Sarvam. Building these models required developing end-to-end capability across data, training, inference, and product deployment. With that foundation in place, we are ready to scale to significantly larger and more capable models, including models specialised for coding, agentic, and multimodal conversational tasks.

Sarvam 105B is available on [![](https://www.google.com/s2/favicons?domain=links.sarvam.io&sz=32)Indus](https://links.sarvam.io/indus-app). Both models are accessible via our API at the [![](https://www.google.com/s2/favicons?domain=dashboard.sarvam.ai&sz=32)API dashboard](https://dashboard.sarvam.ai/). Weights can be downloaded from AI Kosh ([![](https://www.google.com/s2/favicons?domain=aikosh.indiaai.gov.in&sz=32)30B](https://aikosh.indiaai.gov.in/web/models/details/sarvam2_30b_a2b_4.html),[![](https://www.google.com/s2/favicons?domain=aikosh.indiaai.gov.in&sz=32)105B](https://aikosh.indiaai.gov.in/web/models/details/sarvam_105b.html)) and Hugging Face ([![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)30B](https://huggingface.co/sarvamai/sarvam-30b),[![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)105B](https://huggingface.co/sarvamai/sarvam-105b)). If you want to run inference locally with Transformers, vLLM, and SGLang, please refer to the Hugging Face models page for sample implementations.

## Architecture

Both models share a common architectural principle: high-capacity reasoning with efficient training and deployment. At the core is a Mixture-of-Experts (MoE) Transformer backbone that uses sparse expert routing to scale parameter count without increasing the compute required per token, while keeping inference costs practical. The architecture supports long-context inputs through rotary positional embeddings, RMSNorm-based stabilization, and attention designs optimized for efficient KV-cache usage during inference.

While the two models share the same design philosophy, they differ in scale and attention mechanism. Sarvam 30B uses Grouped Query Attention (GQA) to reduce KV-cache memory while maintaining strong performance. Sarvam 105B extends the architecture with greater depth and Multi-head Latent Attention (MLA), a compressed attention formulation that further reduces memory requirements for long-context inference.

Both models use sparse expert feedforward layers with 128 experts, but differ in expert capacity and routing configuration. This allows the larger model to scale to higher total parameters while keeping active compute bounded.

## Training

All stages of the training pipeline were developed and executed in-house. This includes the model architecture, data curation and synthesis pipelines, reasoning supervision frameworks, and reinforcement learning infrastructure. Building everything from scratch gave us direct control over data quality, training dynamics, and capability development across every stage of training, which is a core requirement for a sovereign stack.

### Pre-training

Our 30B and 105B models were trained on large datasets, with 16T tokens for the 30B and 12T tokens for the 105B. The pre-training data spans code, general web data, specialized knowledge corpora, mathematics, and multilingual content. After multiple ablations, the final training mixture was balanced to emphasize reasoning, factual grounding, and software capabilities. We invested significantly in synthetic data generation pipelines across all categories. The multilingual corpus allocates a substantial portion of the training budget to the 10 most-spoken Indian languages.

Pre-training was conducted in three phases, covering long-horizon pre-training, mid-training, and a long-context extension phase. We used sigmoid-based routing scores rather than traditional softmax gating, which improves expert load balancing and reduces routing collapse during training. An expert-bias term stabilizes routing dynamics and encourages more uniform expert utilization across training steps. We observed that the 105B model achieved benchmark superiority over the 30B remarkably early in training, suggesting efficient scaling behavior.

### Supervised Finetuning

During supervised fine-tuning, the model is trained on a large corpus of high-quality prompts curated for difficulty, quality, and domain diversity. Prompts are sourced from open datasets and labeled using custom models to identify domains and analyze distribution coverage. To address gaps in underrepresented or low-difficulty areas, additional prompts are synthetically generated based on the pre-training domain mixture. Empirical analysis showed that most publicly available datasets are dominated by low-quality, homogeneous, and easy prompts, which limits continued learning. To mitigate this, we invested significant effort in building high-quality prompts across domains. All corresponding completions are produced internally and passed through rigorous quality filtering. The dataset also includes extensive agentic traces generated from both simulated environments and real-world repositories, enabling the model to learn tool interaction, environment reasoning, and multi-step decision making.

For safety fine-tuning, we developed a dataset covering both standard and India-specific risk scenarios. This effort was guided by a unified taxonomy and an internal model specification inspired by public frontier model constitutions. To surface and address challenging failure modes, the dataset was further augmented with adversarial and jailbreak-style prompts mined through automated red-teaming. These prompts were paired with policy-aligned, safe completions for supervised training.

### Reinforcement Learning

The reinforcement learning stage uses a large and diverse prompt distribution spanning mathematics, coding, STEM reasoning, web search, and tool usage across both single-turn and multi-turn environments. Rewards are derived from a combination of verifiable signals, such as correctness checks and execution results, and rubric-based evaluations that assess instruction adherence, formatting, response structure, and overall quality. To maintain an effective learning curriculum, prompts are pre-filtered using open-source models and early checkpoints to remove tasks that are either trivially solvable or consistently unsolved. During training, an adaptive sampling mechanism dynamically allocates rollouts based on an information-gain metric derived from the current pass rate of each prompt. Under a fixed generation budget, rollout allocation is formulated as a knapsack-style optimization, concentrating compute on tasks near the model's capability frontier where learning signal is strongest.

The RL system is implemented with an asynchronous GRPO architecture that decouples generation, reward computation, and policy updates, enabling efficient large-scale training while maintaining high GPU utilization. Trajectory staleness is controlled by limiting the age of sampled trajectories relative to policy updates, balancing throughput with training stability. The system omits KL-divergence regularization against a reference model, avoiding the optimization conflict between reward maximization and policy anchoring. Policy optimization instead uses a custom group-relative objective inspired by CISPO, which improves stability over standard clipped surrogate methods. Reward shaping further encourages structured reasoning, concise responses, and correct tool usage, producing a stable RL pipeline suitable for large-scale MoE training with consistent learning and no evidence of reward collapse.

## Benchmarks

### Sarvam 105B

Sarvam 105B matches or outperforms most open and closed-source frontier models of its class across knowledge, reasoning, and agentic benchmarks. On Indian language benchmarks, it significantly outperforms all models we evaluated.

Benchmark| Sarvam-105B| GLM-4.5-Air (106B)| GPT-OSS-120B| Qwen3-Next-80B-A3B-Thinking  
---|---|---|---|---  
GENERAL  
Math500| 98.6| 97.2| 97.0| 98.2  
Live Code Bench v6| 71.7| 59.5| 72.3| 68.7  
MMLU| 90.6| 87.3| 90.0| 90.0  
MMLU Pro| 81.7| 81.4| 80.8| 82.7  
Arena Hard v2| 71.0| 68.1| 88.5| 68.2  
IF Eval| 84.8| 83.5| 85.4| 88.9  
REASONING  
GPQA Diamond| 78.7| 75.0| 80.1| 77.2  
AIME 25 (w/ tools)| 88.3 (96.7)| 83.3| 90.0| 87.8  
HMMT (Feb 25)| 85.8| 69.2| 90.0| 73.9  
HMMT (Nov 25)| 85.8| 75.0| 90.0| 80.0  
Beyond AIME| 69.1| 61.5| 51.0| 68.0  
AGENTIC  
BrowseComp| 49.5| 21.3| 

  * 
| 38.0  
SWE Bench Verified (SWE-Agent Harness)| 45.0| 57.6| 50.6| 34.46  
Tau2 (avg.)| 68.3| 53.2| 65.8| 55.0  
  
Scroll

Scroll

Sarvam 105B - All Benchmarks

**General capabilities**

Sarvam 105B shows strong, balanced performance across core capabilities including mathematics, coding, knowledge, and instruction following. It achieves 98.6 on Math500, matching the top models in the comparison, and 71.7 on LiveCodeBench v6, outperforming most competitors on real-world coding tasks. On knowledge benchmarks, it scores 90.6 on MMLU and 81.7 on MMLU Pro, remaining competitive with frontier-class systems. With 84.8 on IF Eval, the model demonstrates a well-rounded capability profile across the major workloads expected of modern language models.

**Reasoning performance**

Sarvam 105B performs strongly on multi-step reasoning benchmarks, reflecting the training emphasis on complex problem solving. On AIME 25, the model achieves 88.3 Pass@1, improving to 96.7 with tool use, indicating effective integration between reasoning and external tools. It scores 78.7 on GPQA Diamond and 85.8 on HMMT, outperforming several comparable models on both. On Beyond AIME (69.1), which requires deeper reasoning chains and harder mathematical decomposition, the model leads or matches the comparison set. Taken together, these results reflect consistent strength in sustained reasoning and difficult problem-solving tasks.

**Agentic capabilities**

Sarvam 105B is optimized for agentic workloads involving tool use, long-horizon reasoning, and environment interaction. This is reflected in strong results on benchmarks designed to approximate real-world workflows. On BrowseComp, the model achieves 49.5, outperforming several competitors on web-search-driven tasks. On Tau2 (avg.), a benchmark measuring long-horizon agentic reasoning and task completion, it achieves 68.3, the highest score among the compared models. These results indicate that the model can effectively plan, retrieve information, and maintain coherent reasoning across extended multi-step interactions.

#### **Comparison with Larger Models**

A useful comparison is within the same scaling regime, since training compute, dataset size, and infrastructure scale increase dramatically with each generation of frontier models. The newest models from other labs are trained with significantly larger clusters and budgets. Across a range of previous-generation models that are substantially larger, Sarvam 105B remains competitive. We have now established the effectiveness of our training and data pipelines, and will scale training to significantly larger model sizes.

Benchmark| Sarvam-105B| Deepseek R1 0528| Gemini-2.5-Flash| o4-mini| Claude 4 Sonnet  
---|---|---|---|---|---  
AIME25| 88.3| 87.5| 72.0| 92.7| 70.5  
HMMT Feb 2025| 85.8| 79.4| 64.2| 83.3| 75.6  
GPQA Diamond| 78.7| 81.0| 82.8| 81.4| 75.4  
Live Code Bench v6| 71.7| 73.3| 61.9| 80.2| 55.9  
MMLU Pro| 81.7| 85.0| 82.0| 81.9| 83.7  
Browse Comp| 49.5| 3.2| 20.0| 28.3| 14.7  
SWE Bench Verified| 45.0| 57.6| 48.9| 68.1| 66.6  
Tau2 Bench| 68.3| 62.0| 49.7| 65.9| 64.0  
HLE| 11.2| 8.5| 12.1| 14.3| 9.6  
  
Scroll

Scroll

Comparison of Sarvam 105B with Larger Models

### Sarvam 30B

Sarvam 30B is designed as an efficient reasoning model for practical deployment, combining strong capability with low active compute. With only 2.4B active parameters, it performs competitively with much larger dense and MoE models across a wide range of benchmarks. The evaluations below highlight its strengths across general capability, multi-step reasoning, and agentic tasks, indicating that the model delivers strong real-world performance while remaining efficient to run.

Benchmark| Sarvam-30B| Gemma 27B It| Mistral-3.2-24B-Instruct-2506| OLMo 3.1 32B Think| Nemotron-3-Nano-30B| Qwen3-30B-Thinking-2507| GLM 4.7 Flash| GPT-OSS-20B  
---|---|---|---|---|---|---|---|---  
GENERAL  
Math500| 97.0| 87.4| 69.4| 96.2| 98.0| 97.6| 97.0| 94.2  
Humaneval| 92.1| 88.4| 92.9| 95.1| 97.6| 95.7| 96.3| 95.7  
MBPP| 92.7| 81.8| 78.3| 58.7| 91.9| 94.3| 91.8| 95.3  
Live Code Bench v6| 70.0| 28.0| 26.0| 73.0| 68.3| 66.0| 64.0| 61.0  
MMLU| 85.1| 81.2| 80.5| 86.4| 84.0| 88.4| 86.9| 85.3  
MMLU Pro| 80.0| 68.1| 69.1| 72.0| 78.3| 80.9| 73.6| 75.0  
Arena Hard v2| 49.0| 50.1| 43.1| 42.0| 67.7| 72.1| 58.1| 62.9  
REASONING  
GPQA Diamond| 66.5| 

  * 
| 

  * 
| 57.5| 73.0| 73.4| 75.2| 71.5  
AIME 25 (w/ tools)| 80.0 (96.7)| 

  * 
| 

  * 
| 78.1 (81.7)| 89.1 (99.2)| 85.0| 91.6| 91.7 (98.7)  
HMMT Feb 2025| 73.3| 

  * 
| 

  * 
| 51.7| 85.0| 71.4| 85.0| 76.7  
HMMT Nov 2025| 74.2| 

  * 
| 

  * 
| 58.3| 75.0| 73.3| 81.7| 68.3  
Beyond AIME| 58.3| 

  * 
| 

  * 
| 48.5| 64.0| 61.0| 60.0| 46.0  
AGENTIC  
BrowseComp| 35.5| 

  * 
| 

  * 
| 

  * 
| 23.8| 2.9| 42.8| 28.3  
SWE-Bench Verified| 34.0| 

  * 
| 

  * 
| 

  * 
| 38.8| 22.0| 59.2| 34.0  
Tau2 (avg.)| 45.7| 

  * 
| 

  * 
| 

  * 
| 49.0| 47.7| 79.5| 48.7  
  
Scroll

Scroll

Sarvam 30B - All Benchmarks (Gemma and Mistral are compared for completeness. Since they are not reasoning or agentic models, corresponding cells are left empty)

**General capabilities**

Sarvam 30B performs strongly across core language modeling tasks, particularly in mathematics, coding, and knowledge benchmarks. It achieves 97.0 on Math500, matching or exceeding several larger models in its class. On coding benchmarks, it scores 92.1 on HumanEval and 92.7 on MBPP, and 70.0 on LiveCodeBench v6, outperforming many similarly sized models on practical coding tasks. On knowledge benchmarks, it scores 85.1 on MMLU and 80.0 on MMLU Pro, remaining competitive with other leading open models.

**Reasoning performance**

Sarvam 30B performs strongly on multi-step reasoning benchmarks, reflecting its ability to handle complex logical and mathematical problems. On AIME 25, it achieves 88.3 Pass@1, improving to 96.7 with tool use, indicating effective integration between reasoning and external tools. It scores 66.5 on GPQA Diamond and performs well on challenging mathematical benchmarks including HMMT Feb 2025 (73.3) and HMMT Nov 2025 (74.2). On Beyond AIME (58.3), the model remains competitive with larger models. Taken together, these results indicate that Sarvam 30B sustains deep reasoning chains and expert-level problem solving, significantly exceeding typical expectations for models with similar active compute.

**Agentic capabilities**

Sarvam 30B supports native tool calling and performs consistently on benchmarks designed to evaluate agentic workflows involving planning, retrieval, and multi-step task execution. On BrowseComp, it achieves 35.5, outperforming several comparable models on web-search-driven tasks. On Tau2 (avg.), it achieves 45.7, indicating reliable performance across extended interactions. SWE-Bench Verified remains challenging across models; Sarvam 30B shows competitive performance within its class. Taken together, these results indicate that the model is well suited for real-world agentic deployments requiring efficient tool use and structured task execution, particularly in production environments where inference efficiency is critical.

### Indian Language Performance

To evaluate Indian language capabilities, we developed a new benchmark using a pairwise comparison framework with an LLM-as-judge protocol. A key goal of this benchmark is to reflect how language is actually used in India today. This means evaluating each language in two script styles, native script representing formal written usage and romanized Latin script representing colloquial usage commonly seen in messaging and online communication.

The benchmark is organized into four domains: general chat, STEM, mathematics, and coding. It originates from 110 English source prompts, with 50 covering general chat and 20 each for STEM, mathematics, and coding. Each prompt is translated into 22 scheduled Indian languages and provided in both native and romanized script.

Evaluating correctness for complex reasoning prompts directly in low-resource languages can be noisy and inconsistent. To address this, we generated high-quality reference answers in English using Claude Opus 4, which are used only to evaluate the usefulness dimension, covering relevance, completeness, and correctness, for answers generated in Indian languages.

The evaluation uses a pairwise comparison methodology with Gemini 3 as the judge model. The judge evaluates responses across four dimensions: fluency, language/script correctness, usefulness, and verbosity. The evaluation dataset and corresponding prompts are available [![](https://www.google.com/s2/favicons?domain=huggingface.co&sz=32)here](https://huggingface.co/datasets/sarvamai/indivibe).

Sarvam 105B wins on average 90% across all benchmarked dimensions and on average 84% on STEM. math, and coding.

Sarvam 30B wins on average 89% of comparisons across all benchmarked dimensions and 87% on STEM, mathematics, and coding.

### Tokenizer Efficiency

The Sarvam tokenizer is optimized for efficient tokenization across all 22 scheduled Indian languages, spanning 12 different scripts, directly reducing the cost and latency of serving in Indian languages. It outperforms other open-source tokenizers in encoding Indic text efficiently, as measured by the fertility score, which is the average number of tokens required to represent a word. It is significantly more efficient for low-resource languages such as Odia, Santali, and Manipuri (Meitei) compared to other tokenizers. The chart below shows the average fertility of various tokenizers across English and all 22 scheduled languages.

## Inference Optimization

### **Sarvam 30B**

Sarvam 30B was built with an inference optimization stack designed to maximize throughput across deployment tiers, from flagship data-center GPUs to developer laptops. Rather than relying on standard serving implementations, the inference pipeline was rebuilt using architecture-aware fused kernels, optimized scheduling, and disaggregated serving.

Microsecond-level profiling of the execution stack identified memory stalls, kernel launch overhead, and inefficient scheduling as primary bottlenecks. Addressing these yielded substantial throughput improvements across all hardware classes and sequence lengths. The optimization strategy focuses on three key components.

  * **Kernel-level rewrites using fused attention** and matmul pipelines tailored for each hardware target
  * **Advanced scheduling and batching strategies** that improve GPU utilization under realistic multi-user loads
  * **Disaggregated serving pipelines** that remove bottlenecks between prefill and decode stages



These optimizations yield significantly higher tokens per second per GPU at the same latency targets, enabling higher user concurrency and lower infrastructure costs.

#### **High-End Server Performance (H100)**

On H100-class infrastructure, Sarvam 30B achieves substantially higher throughput per GPU across all sequence lengths and request rates compared to the Qwen3 baseline, consistently delivering 3x to 6x higher throughput per GPU at equivalent tokens per second per user operating points.

#### **Performance on cost-efficient deployments (L40S)**

Sarvam 30B runs efficiently on mid-tier accelerators such as L40S, enabling production deployments without relying on premium GPUs. Under tighter compute and memory bandwidth constraints, the optimized kernels and scheduling strategies deliver**1.5x to 3x throughput improvements** at typical operating points. The improvements are more pronounced at longer input and output sequence lengths (28K / 4K), where most real-world inference requests fall.

#### **Edge Performance (MacBook Pro with MXFP4)**

Sarvam 30B is also optimized for local execution on Apple Silicon systems using MXFP4 mixed-precision inference. On MacBook Pro M3, the optimized runtime achieves**20 to 40% higher token throughput** across common sequence lengths. These improvements make local experimentation significantly more responsive and enable lightweight edge deployments without requiring dedicated accelerators.

### **Sarvam 105B**

Sarvam 105B is optimized for server-centric hardware, following a similar process to the one described above with special focus on MLA (Multi-head Latent Attention) optimizations. These include custom shaped MLA optimization, vocabulary parallelism, advanced scheduling strategies, and disaggregated serving. The comparisons above illustrate the performance advantage across various input and output sizes on an H100 node.

### **Tokenizer and Inference Optimization**

Combined with the efficient Indic tokenizer, the performance delta increases significantly for the same SLA. For the 30B model, the delta increases by as much as 10x, reaching performance levels previously not achievable for models of this class on Indic generation.

Note: performance numbers are standalone model measurements without disaggregated inference.

## Demos

The following demonstrations show the practical capabilities of the Sarvam model family across real-world applications, spanning webpage generation, multilingual conversational agents, complex STEM problem solving, and educational tutoring. The examples reflect the models' strengths in reasoning, tool usage, multilingual understanding, and end-to-end task execution, and illustrate how Sarvam models can be integrated into production systems to build interactive applications, intelligent assistants, and developer tools.

### Webpage creation

The widgets below demonstrate Sarvam 105B's agentic capabilities through end-to-end project generation using a Claude Code harness, showing the model's ability to build complete websites from a simple prompt specification.

#### **Pokédex**

### Pokédex

Web App

A fully interactive Pokédex web app, generated entirely by our 105B model from a single prompt. Search, filter by type, and browse detailed stats.

The goal was to generate a complete, production-ready webpage including all HTML, CSS, and JavaScript required to run the application without frameworks or build tools. The model used the PokéAPI to dynamically load Pokémon data, implementing pagination, search, filtering, and a detailed modal view, all from the prompt shown below.

### Prompt for a Pokedex website

Build a sample Pokédex web app as a single index.html file with embedded CSS and JS.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ POKÉAPI REFERENCE (base URL: [![](https://www.google.com/s2/favicons?domain=pokeapi.co&sz=32)https://pokeapi.co/api/v2](https://pokeapi.co/api/v2)) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## List endpoint

Copy
    
    
    GET /pokemon?limit=151&offset=0
    Returns:
    {
      "count": 1302,
      "results": [
        { "name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/" },
        { "name": "ivysaur",   "url": "https://pokeapi.co/api/v2/pokemon/2/" },
        ...
      ]
    }
    

## Individual Pokémon endpoint

Copy
    
    
    GET /pokemon/{id or name}
    Example: GET /pokemon/1   or   GET /pokemon/bulbasaur
    
    Key fields in response:
    {
      "id": 1,
      "name": "bulbasaur",
      "height": 7,          // in decimetres
      "weight": 69,         // in hectograms
      "base_experience": 64,
    
      "sprites": {
        "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
        "other": {
          "official-artwork": {
            "front_default": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png"
          }
        }
      },
    
      "types": [
        { "slot": 1, "type": { "name": "grass", "url": "..." } },
        { "slot": 2, "type": { "name": "poison", "url": "..." } }
      ],
    
      "stats": [
        { "base_stat": 45, "stat": { "name": "hp" } },
        { "base_stat": 49, "stat": { "name": "attack" } },
        { "base_stat": 49, "stat": { "name": "defense" } },
        { "base_stat": 65, "stat": { "name": "special-attack" } },
        { "base_stat": 65, "stat": { "name": "special-defense" } },
        { "base_stat": 45, "stat": { "name": "speed" } }
      ],
    
      "abilities": [
        { "ability": { "name": "overgrow" }, "is_hidden": false },
        { "ability": { "name": "chlorophyll" }, "is_hidden": true }
      ]
    }
    

## Sprite URL shortcut (no API call needed)

You can construct sprite URLs directly without fetching: Thumbnail: [![](https://www.google.com/s2/favicons?domain=raw.githubusercontent.com&sz=32)https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/%7Bid%7D.png) Official artwork: [![](https://www.google.com/s2/favicons?domain=raw.githubusercontent.com&sz=32)https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{id}.png](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/%7Bid%7D.png)

## All 18 types and suggested badge colors

normal: #A8A878 fire: #F08030 water: #6890F0 electric: #F8D030 grass: #78C850 ice: #98D8D8 fighting: #C03028 poison: #A040A0 ground: #E0C068 flying: #A890F0 psychic: #F85888 bug: #A8B820 rock: #B8A038 ghost: #705898 dragon: #7038F8 dark: #705848 steel: #B8B8D0 fairy: #EE99AC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ REQUIREMENTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  * Single index.html, no frameworks, no build tools
  * Display all 1302 Pokémon, paginated at 40 per page, with previous/next controls and a page indicator (e.g. "Page 3 of 33"). Fetching should happen per page - only load the Pokémon needed for the current page, not everything upfront.
  * Responsive card grid showing: sprite (thumbnail URL), name, ID (#001 format), type badges
  * Clicking a card opens a modal with: official artwork, all 6 stats as labeled progress bars (max stat = 255), height (convert dm → m), weight (convert hg → kg), abilities
  * Real-time search by name or ID - searching should scan across all Pokémon, not just the current page
  * Filter by type using clickable buttons
  * Skeleton loading cards while the current page is being fetched
  * Classic Pokédex color scheme: red (#CC0000) primary, white cards, dark text
  * Cache fetched Pokémon data to avoid redundant network calls when revisiting a page



Create index.html and make it fully functional end to end.

#### **Product Landing Page**

### Website Design

Web App

A complete website landing page, designed and coded by our 105B model in a single pass. Scroll through to explore the full layout, animations, and interactions.

The task was to build a complete website for Sarvam, capturing the spirit of an Indian AI company building for a billion people while matching a world-class visual standard across typography, motion, layout, and interaction design. The full prompt is shown below.

### Prompt for Sarvam's website

Build me a stunning, production-grade website for **Sarvam AI** \- an Indian AI company whose mission is to build AI for a billion people, with deep roots in India's linguistic and cultural diversity. The name "Sarvam" (सर्वम्) means "everything" in Sanskrit.

**Aesthetic Direction:** Go for a refined Indian modernism - inspired by Mughal jali lattice geometry, the warmth of saffron and marigold, and the precision of frontier AI engineering. Think: ancient India meets GPU clusters. Confident, warm, architecturally elegant, and technically serious. Not kitsch - think the Taj Mahal meets a data center.

**Color Palette:**

  * Background: `#0A0A0F` (near-black with blue undertone)
  * Primary accent: `#FF6B35` (warm saffron-orange)
  * Secondary accent: `#00C9A7` (teal-green for tech credibility)
  * Body text: `#C8B8A2` (warm aged parchment - not sterile white)
  * Highlight white: `#FAFAF7` (slightly warm)



**Typography:**

  * Display/Hero: Playfair Display (classical, Indic-adjacent serif)
  * Subheadings: Syne (geometric, modern)
  * Body: Literata (refined long-form reading)
  * Code: Fira Code



**Visual Effects & Textures:**

  * Subtle grain overlay across the entire page
  * Soft saffron radial glow behind hero elements
  * SVG-based jali lattice patterns as decorative dividers and background watermarks
  * Scroll-triggered text reveals using IntersectionObserver with vertical clip-mask wipes
  * Sticky nav that starts transparent and gains a `backdrop-filter: blur(20px)` dark blur on scroll
  * Magnetic hover effect on CTA buttons with a pulsing saffron ring animation



**Page Sections to Build:**

  1. **Navbar** \- Logo shows both Devanagari "सर्वम्" and Roman "Sarvam AI" side by side as SVG. Links: Products, Research, API, About, Blog. Right-side CTA: "Get API Access" with glowing saffron pulse.

  2. **Hero** \- Full viewport height. Massive Playfair Display headline: _"AI for a Billion People."_ Subline in Syne: _"Built for India's languages, cultures, and contexts - from the ground up."_ Below it, two CTAs: "Explore the API" (filled saffron) and "Read our Research" (ghost/outlined). Background: animated particle field subtly shaped like the Indian subcontinent, with glowing nodes at major Indian cities. Faint jali pattern overlaid at 5% opacity.

  3. **Language Strip** \- A horizontally scrolling ticker (auto-animated, no pause) showing Sarvam's supported Indian languages in their native scripts: हिन्दी · தமிழ் · తెలుగు · ಕನ್ನಡ · മലയാളം · বাংলা · ગુજરાતી · ਪੰਜਾਬੀ · ଓଡ଼ିଆ · মৈতৈলোন্ · and more. Each script in its own warm-toned color. This strip signals scope instantly.

  4. **Products Section** \- Three cards in an asymmetric grid (one wide, two stacked). Products: **Sarvam-1** (flagship LLM), **Shuka** (voice AI), **Translate API** (real-time Indian language translation). Each card has a glowing accent border, a subtle animated background, a one-line description, and a "Learn more →" link. Cards lift and glow on hover.

  5. **Research Section** \- Dark editorial layout. Left side: a large pull quote in Playfair Display italic - _"We don't adapt Western models to India. We build from Bharat."_ Right side: three recent research paper cards with title, abstract snippet, and a tag (e.g., "NLP", "Speech", "Indic LLMs"). A "View all research →" link at the bottom.

  6. **API / Developer Section** \- Deep dark panel with a live code snippet shown in Fira Code with syntax highlighting. The snippet shows a simple API call to Sarvam's translation endpoint with a JSON response in Hindi. Below the code: three stat cards - "11+ Languages", "< 200ms latency", "99.9% uptime". A CTA: "Start building free →"

  7. **About / Mission Section** \- Full-width cinematic panel. Background: a slow parallax image of India from above (satellite-style, muted and dark). Overlaid large text: _"Sarvam was founded with one belief - that the next billion internet users deserve AI that truly understands them."_ Founder names beneath in small Syne caps.

  8. **Footer** \- Three columns: Links (Products, Research, Careers, Blog), Socials (GitHub, Twitter/X, LinkedIn), and a newsletter signup. Bottom bar: copyright, privacy policy, terms. The Devanagari logo watermarked faintly in the background at 3% opacity.




**Technical Requirements:**

  * Single HTML file with embedded CSS and JS
  * Google Fonts for typography
  * Smooth scroll behavior throughout
  * All animations CSS-first, JS only where necessary
  * Fully responsive down to 375px mobile
  * Accessible - proper semantic HTML, ARIA labels, sufficient color contrast on interactive elements



Make it feel like it was designed by a world-class studio hired specifically to capture the soul of Indian AI. Every detail should feel intentional and unmistakably Sarvam.

### JEE Mains 2026

Sarvam 105B was evaluated on the JEE Main 2026 paper from Shift 2, conducted on 28 January 2026, to demonstrate its STEM reasoning capabilities. The question paper and solutions were sourced from:[![](https://www.google.com/s2/favicons?domain=allen.in&sz=32)https://allen.in/jee-main/january-2026-question-paper-with-solutions](https://allen.in/jee-main/january-2026-question-paper-with-solutions)

The evaluation was carried out in two phases:

  1. **Text-Only Evaluation:** For text-only questions, Sarvam 105B was evaluated directly on questions containing purely textual content.
  2. **Diagram-Based Evaluation:** For questions that included diagrams, Gemini-3-Pro was used to generate structured textual descriptions of the visuals, which were then provided as input to Sarvam 105B for answer generation.



The tables below summarize Sarvam 105B's performance across Physics, Chemistry, and Mathematics under Pass@1 and Pass@2 evaluation settings.

Under Pass@1, the model shows strong first-attempt accuracy across all subjects. In Mathematics, it achieves a perfect 25/25. In Chemistry, it scores 23/25, with near-perfect performance on both text-only and diagram-derived questions. Physics shows similarly strong performance at 22/25, with most errors occurring in diagram-based reasoning.

Under Pass@2, performance improves to perfect scores across all subjects. Physics improves from 22/25 to 25/25, Chemistry from 23/25 to 25/25, and Mathematics maintains a perfect 25/25. Diagram-based questions in both Physics and Chemistry achieve full marks at Pass@2, indicating that the model reliably resolves visual reasoning tasks when given structured textual representations.

Subject| Text Only| Diagrams| Overall  
---|---|---|---  
Physics| 18/18| 7/7| 25/25  
Chemistry| 20/20| 5/5| 25/25  
Mathematics| 25/25| 

  * 
| 25/25  
  
Scroll

Scroll

JEE Mains 2026 - Pass@2

#### **Tutor Mode**

Tutor Mode is an internal project where the [![](https://www.google.com/s2/favicons?domain=links.sarvam.io&sz=32)Indus ](https://links.sarvam.io/indus-app)stack operates with a system prompt optimized for student-teacher conversations. The example below shows Sarvam 105B helping a student solve a JEE problem through interactive dialog rather than providing the answer directly. The model guides the student by asking probing questions, building toward the underlying concepts before arriving at the answer. This also demonstrates the model's role-playing ability.

Note: the questions below are taken from the same JEE Mains paper solved above.

PhysicsMathsChemistry

Physics

+3

Artifacts

the mean free path of a molecule of diameter 5 x 10^-10 m at the temperature 41°c and pressure 1.38 x 10^5 pa, is given as ____ m. (given k_b = 1.38 x 10^-23 j/k).

options -

  * 2√2 x 10^-10
  * 10√2 x 10^-8
  * 2√2 x 10^-8
  * 2 x 10^-8



Hi there! I see you're working on a problem about the **mean free path** of a gas molecule. That's a classic concept in kinetic theory.

Before we dive into the math, could you let me know which grade you're in? Also, when you hear the term "mean free path," what do you think it depends on? For example, if you imagine molecules in a gas, what physical factors would make it harder for a molecule to travel a long distance without hitting something?

im not really sure about the concepts behind this. im preparing for jee mains and this topic always confuses me.

No worries! JEE Mains problems often look more intimidating than they actually are. Let's break it down.

The **mean free path** (λ\lambdaλ) is simply the average distance a molecule travels between two successive collisions. Think of it like walking through a crowded room; how far you can get before bumping into someone depends on a few things you already intuitively know.

  * **Size of molecules ( ddd):** Bigger molecules are easier to hit.
  * **Density/Number of molecules:** More people in the room means more bumps.
  * **Temperature ( TTT) and Pressure (PPP):** These dictate how packed the molecules are.



If you had to guess, would the distance between hits (λ\lambdaλ) be **larger** or **smaller** if the pressure (PPP) increased?

i think if the pressure is higher, the molecules are packed tighter, so they would hit each other more often. that should make the distance smaller, right?

Spot on! Your intuition is leading you exactly where we need to go.

Here is how those factors relate mathematically:

  * **λ ∝1d2\lambda \propto \frac{1}{d^2}λ∝d21​**: If the molecule is twice as wide, it's actually four times more likely to collide (because the _area_ it occupies matters).
  * **λ ∝1P\lambda \propto \frac{1}{P}λ∝P1​**: Higher pressure means molecules are squeezed together, leading to more frequent collisions.
  * **λ ∝T\lambda \propto Tλ∝T**: At higher temperatures (for a fixed pressure), gas expands and molecules move further apart.



You mentioned knowing PV=nRTPV = nRTPV=nRT. We can actually use that to find the formula for λ\lambdaλ. Since we are looking for a formula involving diameter (ddd), pressure (PPP), and temperature (TTT), let's try to visualize the "collision zone" first.

i know pv = nrt, but i cant remember the specific formula for mean free path. how do we get from one to the other?

That's a great starting point because PV=nRTPV = nRTPV=nRT is the heart of gas behavior!

Let's visualize why a molecule collides. Imagine a molecule with diameter ddd moving through space. It will hit any other molecule whose center comes within a distance ddd of its own center.

This means our molecule effectively acts like a "bulldozer" with an effective diameter of 2d2d2d. If any other molecule's center falls within this "danger zone," a collision happens.

If the effective collision diameter is 2d2d2d, what would be the **cross-sectional area** of that "danger zone" circle? (Recall the area of a circle is πr2\pi r^2πr2).

is it pi(2d)^2?

Close! While the "danger zone" diameter is 2d2d2d, the actual radius involved for the center-to-center hit is ddd.

So, the **collision cross-section area** (σ\sigmaσ) is: σ=πd2\sigma = \pi d^2σ=πd2

Now, imagine this molecule zips forward. It sweeps out an imaginary cylinder. Any molecule inside this cylinder gets hit.

In the derivation, we find that the mean free path λ\lambdaλ is inversely proportional to this area and the number of molecules per unit volume (nnn). However, because _all_ molecules are moving (not just one), we add a factor of 2\sqrt{2}2​ to account for the average relative velocity.

This gives us the final JEE formula: λ=kBT2πd2P\lambda = \frac{k_B T}{\sqrt{2} \pi d^2 P}λ=2​πd2PkB​T​

Do you see where the values from your question (kBk_BkB​, TTT, ddd, and PPP) fit into this?

oh, i see! but the question gives kb as 1.38 x 10^-23. where does that go in the calculation?

It fits perfectly! The kBk_BkB​ in the question is the **Boltzmann constant** , and it sits right in the numerator of our formula:

λ=kBT2πd2P\lambda = \frac{k_B T}{\sqrt{2} \pi d^2 P}λ=2​πd2PkB​T​

By plugging the values in, the units will cancel out to give you the distance in meters. Let's list what we have:

  * kB=1.38×10−23k_B = 1.38 \times 10^{-23}kB​=1.38×10−23 J/K
  * P=1.38×105P = 1.38 \times 10^{5}P=1.38×105 Pa
  * d=5×10−10d = 5 \times 10^{-10}d=5×10−10 m
  * T=41°CT = 41°CT=41°C



Before we calculate, we must convert the temperature to **Kelvin**. Do you remember how to turn Celsius into Kelvin?

yes, i add 273. so 41 + 273 = 314 k. now i just plug them all in?

Exactly! You've got the temperature right (314K314 K314K, or 314.15K314.15 K314.15K for precision).

Now, here is a pro-tip for JEE math: look for things that **cancel out**. Notice that kBk_BkB​ is 1.38×10−231.38 \times 10^{-23}1.38×10−23 and PPP is 1.38×1051.38 \times 10^51.38×105.

When you put them in the formula: λ=(1.38×10−23)×3142×π×(5×10−10)2×(1.38×105)\lambda = \frac{(1.38 \times 10^{-23}) \times 314}{\sqrt{2} \times \pi \times (5 \times 10^{-10})^2 \times (1.38 \times 10^5)}λ=2​×π×(5×10−10)2×(1.38×105)(1.38×10−23)×314​

The 1.381.381.38 in the top and bottom will cancel out immediately! That makes your life much easier.

Would you like to try simplifying the powers of 101010 next? What do you get for the denominator's power of 101010 when you square ddd (5×10−105 \times 10^{-10}5×10−10 m)?

i tried calculating it all and i think it simplifies to something like 2.82 x 10^-8. does that mean the answer is option c?

You nailed it! Option C (22×10−82\sqrt{2} \times 10^{-8}22​×10−8) is correct. 🎉

When you finish the calculation, you get approximately 2.82×10−82.82 \times 10^{-8}2.82×10−8 m. Since 2≈1.414\sqrt{2} \approx 1.4142​≈1.414, then 222\sqrt{2}22​ is indeed ≈2.828\approx 2.828≈2.828.

**Summary of your success:**

  1. Converted TTT to Kelvin (314.15K314.15 K314.15K).
  2. Identified the collision cross-section πd2\pi d^2πd2.
  3. Used the corrected mean free path formula λ=kBT2πd2P\lambda = \frac{k_B T}{\sqrt{2} \pi d^2 P}λ=2​πd2PkB​T​.
  4. Managed the powers of 101010 correctly.



Would you like me to find another practice problem on **RMS velocity** or **Graham's Law** to keep this momentum going?

[Ask anything . . .](https://indus.sarvam.ai/)

### Codeforces

The coding capabilities of Sarvam 30B and Sarvam 105B were evaluated using real-world competitive programming problems from Codeforces (Div3,[![](https://www.google.com/s2/favicons?domain=codeforces.com&sz=32)link](https://codeforces.com/contest/2195)). The evaluation involved generating Python solutions and manually submitting them to the Codeforces platform to verify correctness. Correctness is measured at pass@1 and pass@4 as shown in the table below.

[Codeforces Round 1080 (Div. 3)](https://codeforces.com/contest/2195)

Problems A–H · Python 3

Problem| Sarvam 30B| Sarvam 105B  
---|---|---  
| pass@1| pass@4| pass@1| pass@4  
ASieve of Erato67henesNumber Theory| [](https://codeforces.com/contest/2195/submission/364437466)| | [](https://codeforces.com/contest/2195/submission/364446328)|   
BHeapify 1Implementation| [](https://codeforces.com/contest/2195/submission/364437611)| | [](https://codeforces.com/contest/2195/submission/364446352)|   
CDice Roll SequenceDP| [](https://codeforces.com/contest/2195/submission/364437713)| | [](https://codeforces.com/contest/2195/submission/364446364)|   
DAbsolute CinemaMath| [](https://codeforces.com/contest/2195/submission/364437810)| | [](https://codeforces.com/contest/2195/submission/364446394)|   
EIdiot First SearchTrees / DFS| [](https://codeforces.com/contest/2195/submission/364437929)| [](https://codeforces.com/contest/2195/submission/364438338)| [](https://codeforces.com/contest/2195/submission/364447089)|   
FParabola IndependenceGraphs / DP| [](https://codeforces.com/contest/2195/submission/364437998)| [](https://codeforces.com/contest/2195/submission/364438615)| [](https://codeforces.com/contest/2195/submission/364447210)|   
GIdiot First Search and QueriesData Structures| [](https://codeforces.com/contest/2195/submission/364438057)| [](https://codeforces.com/contest/2195/submission/364439484)| [](https://codeforces.com/contest/2195/submission/364447354)| [](https://codeforces.com/contest/2195/submission/364469721)  
HCodeforces Heuristic Contest 001Geometry| [](https://codeforces.com/contest/2195/submission/364438093)| [](https://codeforces.com/contest/2195/submission/364439863)| [](https://codeforces.com/contest/2195/submission/364449155)| [](https://codeforces.com/contest/2195/submission/364472800)  
Solved| 4/8| 5/8| 6/8| 6/8  
  
Answers are generated using the following system prompt, with code snippets extracted from markdown fences and think tokens stripped from within`<think>`tags.

### Codeforces System Prompt

You are a world-class competitive programmer competing in a live Codeforces contest. Winning this contest is critical - every problem matters and failure is not an option.

Before writing any code:

Read the problem statement extremely carefully. Re-read the constraints, edge cases, and examples. Do not misread a single detail.

Think deeply about the optimal algorithmic approach. Consider time and space complexity relative to the given constraints. A brute-force solution that TLEs is worthless.

Mentally trace through the examples to verify your approach before coding. If something feels off, stop and rethink - do not rush.

Watch out for traps: integer overflow, off-by-one errors, unhandled edge cases (n=1, empty input, maximum constraints).

Double-check your solution's correctness and efficiency one final time before outputting it.

Run on the test cases provided in the problem statement and verify the correctness of the solution.

Write the most optimized, correct solution possible. Use efficient I/O, optimal data structures, and the best known algorithm for the problem. Every millisecond and every byte of memory counts.

Output ONLY the complete solution code - no explanation, no markdown fences, no comments about your approach.

The code must read from stdin and write to stdout.

Language: {lang_version}

The Codeforces contest used for this evaluation took place in February 2026, while the knowledge cutoff of both models is June 2025, making it unlikely that the models had seen these questions. Strong performance in this setting provides evidence of genuine generalization and real problem-solving capability.

### Samvaad: Conversational Agents

Sarvam 30B has been fine-tuned for production deployment of conversational agents on [![](https://www.google.com/s2/favicons?domain=www.sarvam.ai&sz=32)**Samvaad**](https://www.sarvam.ai/products/conversational-agents) , Sarvam's Conversational AI platform. Compared to models of similar size, it shows clear performance improvements in both conversational quality and latency.

Key strengths include strong proficiency in Indian languages, particularly accurate handling of numerical information within those languages, and reliable execution of tool calls during multilingual interactions. Latency gains come from a combination of fewer active parameters than comparable models, targeted inference optimizations, and reduced tokenizer overhead.

The two examples below show telephonic conversations handled by Sarvam 30B in Hindi and Tamil.

Banking Assistant

Hindi

Crop Survey

Tamil

0:00

0:00

Play Conversation

### Indus: AI Assistant for India

Sarvam 105B powers [![](https://www.google.com/s2/favicons?domain=links.sarvam.io&sz=32)Indus](https://links.sarvam.io/indus-app), Sarvam's chat application, operating with a system prompt optimized for conversations. The example demonstrates the model's ability to understand Indic queries, execute tool calls effectively, and reason accurately. Web search is conducted in English to access current and comprehensive information, while the model interprets the query and delivers a correct response in Telugu.

ఈ మధ్య పికిల్‌బాల్ గురించి నేను చాలా వింటున్నాను

+3

Artifacts

ఈ మధ్య పికిల్‌బాల్ గురించి నేను చాలా వింటున్నాను. నేను విజయవాడలో ఉంటాను, బెంజ్ సర్కిల్ దగ్గరలో పికిల్‌బాల్ కోర్టులు ఏవైనా ఉన్నాయా? ఈ ఆట కోసం నేను ఏమేం కొనుగోలు చేయాలి? మొత్తం ఎంత ఖర్చవుతుంది? అలాగే ఒక బిగినర్‌గా, నేను ముందుగా క్లాసెస్ తీసుకోవాలా లేక నేరుగా ఆట మొదలుపెట్టవచ్చా? దీని రూల్స్ గురించి , కొత్తగా ఆడేవాళ్లు చేసే తప్పుల గురించి కొన్ని టిప్స్ ఇస్తే బాగుంటుంది.

Thinking

search
    
    
    {
      "query": "pickleball courts Vijayawada Benz Circle Andhra Pradesh",
      "search_type": "general"
    }

మీరు విజయవాడలో పికిల్‌బాల్ ఆడాలని అనుకుంటున్నందుకు చాలా సంతోషం! బెంజ్ సర్కిల్‌కు దగ్గరలో ఉన్న కోర్టులు, పరికరాలు మరియు బిగినర్ టిప్స్ గురించి వివరాలన్నీ తెలుసుకోవడానికి నేను మీకు సహాయం చేస్తాను.
    
    
    1. Top Pickleball Courts in Vijayawada near me
    2. The Pickleball Republic - Siddhartha Nagar, Vijayawada
    3. PickleBall Arena (@pickleballarena_vijayawada)
    4. Associations Of Sports in Benz Circle, Vijayawada - Justdial
    5. Sports Venues in Benz-circle-vijayawada: Book Top ...

Thinking

search
    
    
    {
      "query": "pickleball equipment cost India beginner paddle shoes racket",
      "search_type": "general"
    }
    
    
    1. Buy Pickleball Equipment Paddles, Balls, Nets Online in ...
    2. Buy Pickleball Paddles Online at Best Prices In India
    3. Pickleball Equipment
    4. Buy Pickleball Paddles Online in India at Best Prices
    5. Buy HEAD Pickleball Paddle at Best Price in India

Thinking

search
    
    
    {
      "query": "pickleball beginner rules tips common mistakes how to play",
      "search_type": "general"
    }
    
    
    1. 15 Common Pickleball Errors Ruining Your Game
    2. How to Play Pickleball: 9 Rules Every Beginner Should Know
    3. 5 common beginner mistakes in pickleball
    4. Common Pickleball Mistakes: 5 Errors Beginners Make
    5. How to Play Pickleball: The Ultimate Guide on Pickleball Rules

Thinking

search
    
    
    {
      "query": "pickleball court rental price Vijayawada hourly rate",
      "search_type": "general"
    }
    
    
    1. 🏓 Play Pickleball at the Lowest Price Ever in VIJAYAWADA ...
    2. Dink It Pickleball - Vijayawada - Guru Nanak Colony ...
    3. Pickleball in Vijayawada! Play at The Pickleball Republic
    4. 🏓 Play Pickleball at the Lowest Price Ever in VIJAYAWADA ...
    5. 5️⃣0️⃣0️⃣ 1 month swimming pool(including training)+ ...

Thinking

చాలా మంచి ఛాయిస్! పికిల్‌బాల్ అనేది ఆడటానికి చాలా సరదాగా, ఉత్సాహంగా ఉండే ఆట. విజయవాడలో ఈ ఆట గురించి సమాచారం ఇస్తాను:

## 🏓 మీ దగ్గరలో (బెంజ్ సర్కిల్) కోర్టులు

**సమీపంలో అందుబాటులో ఉన్నవి:**

  * **DINK IT Pickleball** \- గురునానక్ కాలనీ (బెంజ్ సర్కిల్ నుండి సుమారు 1.2 కిలోమీటర్ల దూరం)
  * **ది పికిల్‌బాల్ రిపబ్లిక్** \- సిద్ధార్థ్ నగర్, పోలిక్లినిక్ రోడ్డు దగ్గర ,
  * **PickleBall Arena** \- జోజీ నగర్, భవానిపురం ,
  * **Pickle And Brew** \- భరత్ నగర్ (ఇది కొంచెం దూరం ఉంటుంది)



**కోర్టు ధరలు:**

  * ప్రాథమిక కోర్టులు: గంటకు ₹200
  * ప్రీమియం కోర్టులు: గంటకు ₹600 ,
  * విద్యార్థులకు: ₹500/-



**సమయాలు:** చాలా చోట్ల సోమవారం నుండి ఆదివారం వరకు అందుబాటులో ఉంటాయి. కొన్ని చోట్ల ఉదయం 6 గంటల నుండి రాత్రి వరకు సమయం ఉంటుంది .

## 🛍️ కొనుగోలు చేయాల్సిన వస్తువులు (ఖర్చు వివరాలు)

**బిగినర్ల కోసం (ప్రారంభ ధరలు):**

  * **పికిల్‌బాల్ ప్యాడిల్** : ₹1,890 - ₹4,999 , ,
  * **బంతి** : ప్యాడిల్‌తో కలిపి వచ్చే సెట్‌లో 3 బంతులు ఉంటాయి
  * **షూస్** : మార్కింగ్ లేని రబ్బరు సోల్ ఉన్న షూస్ తప్పనిసరి
  * **బ్యాగ్** : వస్తువులను తీసుకెళ్లడానికి బ్యాగ్ తీసుకుంటే మంచిది



**పూర్తి సెట్‌లు** (2 ప్యాడిల్స్ + 3 బంతులు + బ్యాగ్): ₹3,515 - ₹4,999 ,

**అద్దెకు కూడా లభిస్తాయి** : కోర్టులో గంటకు ₹50/- చొప్పున ప్యాడిల్ అద్దెకు తీసుకోవచ్చు

## 🎯 బిగినర్స్ కోసం సలహా

**ముందే క్లాసెస్‌కు వెళ్లాలా లేక నేరుగా ఆడించాలా?** **ముందే క్లాసెస్‌కు వెళ్లడం మంచిది** : ఎందుకంటే:

  * సరిగ్గా పట్టుకోవడం (grip) నేర్చుకోవచ్చు
  * రూల్స్ వివరంగా తెలుస్తాయి
  * ఎవరైనా శిక్షకులు (coaches) అందుబాటులో ఉంటారు
  * ఇతరులతో ఆడుతూ ప్రాక్టీస్ చేసే అవకాశం ఉంటుంది



**ముఖ్యమైన రూల్స్:**

  1. **సర్వ్** : అండర్ హ్యాండ్ పద్ధతిలో, కింద నుండి పైకి కొట్టాలి
  2. **నో-వాలీ జోన్** : నెట్ దగ్గర నేరుగా బంతిని కొట్టకూడదు ("కిచెన్" రూల్)
  3. **డబుల్ బౌన్స్ రూల్** : సర్వ్ చేసిన తర్వాత సర్వ్ చేసిన వారు, వారి భాగస్వాములు బంతిని ఒకసారి కొట్టాలి
  4. **స్కోరింగ్** : కేవలం సర్వ్ చేసిన వారు మాత్రమే పాయింట్లు సాధించగలరు



**బిగినర్స్ చేసే సాధారణ తప్పులు & పరిష్కారాలు:**

  * **నెట్‌కు చాలా దగ్గరగా నిలబడటం** : నెట్ నుండి 3-4 అడుగుల దూరం పాటించాలి
  * **సరిగ్గా పట్టుకోకపోవడం** : ప్యాడిల్‌ను సరిగ్గా పట్టుకోవడం నేర్చుకోవాలి
  * **నెట్‌కు వేగంగా వెళ్లడం** : సర్వ్ చేసిన వెంటనే నెట్‌కు వెళ్లకుండా, బంతి అటు ఇటు తగిలేలా చూడాలి
  * **కిచెన్ రూల్ పాటించకపోవడం** : నెట్ దగ్గర నేరుగా బంతిని కొట్టకూడదు
  * **పాదాలను కదపకపోవడం** : నిలకడగా ఉండి, త్వరగా స్పందించడం ప్రాక్టీస్ చేయాలి



**నేర్చుకోవడానికి కొన్ని చిట్కాలు:**

  * మీకంటే అనుభవం ఉన్న వారితో ఆడుతూ, వారి నుండి నేర్చుకోవడానికి ప్రయత్నించండి
  * మొదట సాఫ్ట్ షాట్లు (dinks) ప్రాక్టీస్ చేయండి, ఆ తర్వాత వేగంగా కొట్టడం నేర్చుకోండి
  * 2-3 సార్లు ఆడిన తర్వాత మీ స్థాయిని బట్టి కోర్టును బుక్ చేసుకోండి
  * ప్యాడిల్‌తో పాటు మంచి షూస్ కూడా కొనుగోలు చేయండి - అవి ఆటలో చాలా ముఖ్యం



**మొత్తం ప్రారంభ ఖర్చు** : మీరు కోర్టు సమయం కోసం గంటకు ₹300-400 ఖర్చు చేస్తే, మీకు మంచి ప్యాడిల్ కావాలంటే ఒక సెట్‌కు సుమారు ₹4,000-6,000 ఖర్చు అవుతుంది.

మీరు నేరుగా DINK IT Pickleball (బెంజ్ సర్కిల్ నుండి దగ్గరగా ఉంటుంది) కి వెళ్లి అక్కడి శిక్షకులతో మాట్లాడితే, వారు మీకు ఆటను నేర్పించడానికి సహాయం చేస్తారు. అక్కడ ప్యాడిల్స్ కూడా అద్దెకు దొరుకుతాయి కాబట్టి, మీరు వెంటనే ఆటను ప్రారంభించవచ్చు!

మీకు ఇంకా ఏమైనా వివరాలు కావాలా? ఉదాహరణకు ఉత్తమ కోర్టులను ఎలా బుక్ చేసుకోవాలి లేదా పికిల్‌బాల్ ఆడే ఇతర వ్యక్తులను ఎలా కలవాలి అనే విషయాలు చెప్పమంటారా?

[[19]5 common beginner mistakes in pickleball](https://www.selkirk.com/blogs/pickleball-education/5-common-beginner-mistakes?srsltid=AfmBOortrlwbQ5H-S5-0ZeDh7y3-OAseK0b8qTvz-PwDADhZbDCDcJXu)[[27]Dink It Pickleball - Vijayawada - Guru Nanak Colony ...](https://playo.co/venues/guru-nanak-colony-vijayawada/dink-it-pickleball-vijayawada-guru-nanak-colony-vijayawada)[[29]Top Lawn Tennis Courts in Vijayawada near me](https://www.justdial.com/Vijayawada/Lawn-Tennis-Courts/nct-11149970)[[7]Buy Pickleball Equipment Paddles, Balls, Nets Online in ...](https://scssports.in/collections/pickleball?srsltid=AfmBOoq_ghucj0oczzy9rde_j8WzyjvnHaWNH8ILhlijkv4SYubk4MQ9)[[22]10 Common Mistakes Beginners Pickleball Often Do](https://www.rockstaracademy.com/blog/common-pickleball-mistakes)[[6]PickleBall Arena - Vijayawada - Joji Nagar, Vijayawada](https://playo.co/venues/joji-nagar-vijayawada/pickleball-arena-vijayawada-joji-nagar-vijayawada)

[Ask anything . . .](https://indus.sarvam.ai/)

## Conclusion

Sarvam 30B and Sarvam 105B represent a significant step in building high-performance, open foundation models in India. By combining efficient Mixture-of-Experts architectures with large-scale, high-quality training data and deep optimization across the entire stack, from tokenizer design to inference efficiency, both models deliver strong reasoning, coding, and agentic capabilities while remaining practical to deploy.

A defining strength of the Sarvam model family is its investment in the Indian AI ecosystem, reflected in strong performance across Indian languages, tokenization optimized for diverse scripts, and safety and evaluation tailored to India-specific contexts. Combined with Apache 2.0 open-source availability, these models serve as foundational infrastructure for sovereign AI development.

This release also marks a milestone in internal capabilities. Through this effort, Sarvam has developed the know-how to build high-quality datasets at scale, train large models efficiently, and achieve strong results at competitive training budgets. With these foundations in place, the next step is to scale further, training significantly larger and more capable models.

## Acknowledgements

These models were trained using compute provided through the IndiaAI Mission, under the Ministry of Electronics and Information Technology, Government of India. Nvidia collaborated closely on the project, contributing libraries used across pre-training, alignment, and serving. We're also grateful to the developers who used earlier Sarvam models and took the time to share feedback. We're open-sourcing these models as part of our ongoing work to build foundational AI infrastructure in India.

Curious what else we're building? Explore our APIs and start creating. 

Curious what else we're building?

Explore our APIs and start creating.

[Get Started](https://indus.sarvam.ai)
