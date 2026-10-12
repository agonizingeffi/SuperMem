# LongMemEval Evaluation Scripts

This directory contains SuperMem evaluation scripts for the **LongMemEval** benchmark.

## Overview

LongMemEval is a comprehensive benchmark for evaluating long-term memory in LLMs. We provide two core scripts to demonstrate SuperMem's capabilities in memory construction, retrieval-augmented generation (RAG), and periodic memory consolidation.

## Evaluation Scripts

### 1. Main Evaluation

This script performs the complete evaluation pipeline:

* **Memory Construction**: Dynamically adds session-based conversations into the memory store.
* **Topic Segmentation & Compression**: Automatically handles long-context sessions using LLMLingua-2.
* **RAG & QA**: Retrieves relevant memories to answer targeted questions.
* **LLM-based Judging**: Uses a GPT-based judge to verify answer accuracy across multiple categories (Temporal, Knowledge Update, etc.).

**How to run:**

1. Configure your `api_key` and `base_url` inside the script.
2. Ensure the `longmemeval_s.json` dataset is in the correct path.
3. Execute the command for your LLM provider:

   **For OpenAI / GPT-compatible APIs:**
   ```bash
   python run_supermem_gpt.py
   ```

   **For Qwen / DeepSeek / other OpenAI-compatible APIs:**
   ```bash
   python run_supermem_qwen.py
   ```

   Both scripts implement the same evaluation pipeline; the only difference is the model provider and API configuration. The root `README.md` Quick Start uses `run_supermem_qwen.py` as the default example.

### 2. Offline Memory Update

This utility script demonstrates SuperMem's Offline Update mechanism. It processes existing memory collections to merge redundant information and refine the memory store.

**How to run:**

1. Set the `base_dir` to point to your stored memory collections.
2. Execute the following command:

```bash
python offline_update.py
```

## Key Configuration Parameters

Both evaluation scripts share a common configuration block. The parameters below are frequently asked about:

### `messages_use`

Controls which side of each conversation turn is indexed into memory.

| Value | Behavior |
|---|---|
| `"user_only"` | Index only user messages (**default** in both scripts) |
| `"assistant_only"` | Index only assistant (model) messages |
| `"hybrid"` | Index both user and assistant messages per turn |
