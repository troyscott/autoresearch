# Autoresearch Use Cases

Below are practical use case examples for leveraging the autoresearch framework — an autonomous AI research loop that iteratively improves LLM training code through automated experimentation.

---

## 1. Overnight Hyperparameter Search

**Scenario:** You have a single H100 GPU and want to find the best learning rates, batch sizes, and warmdown schedules for your model — but don't want to babysit a grid search.

**How it works:**
- Point your AI agent at `program.md` before going to bed.
- The agent systematically tweaks values like `MATRIX_LR`, `EMBEDDING_LR`, `TOTAL_BATCH_SIZE`, and `WARMDOWN_RATIO` in `train.py`.
- Each experiment trains for exactly 5 minutes, and the agent keeps improvements and reverts failures.
- You wake up to `results.tsv` with ~100 experiments and a `train.py` that reflects the best configuration found.

**Value:** Replaces manual grid/random search with an intelligent, autonomous agent that reasons about which hyperparameters to try next based on prior results.

---

## 2. Architecture Exploration

**Scenario:** You want to explore whether alternative architectures (different attention patterns, activation functions, normalization strategies, MLP designs) can outperform the default GPT setup under a fixed compute budget.

**Example experiments the agent might try:**
- Swapping `relu().square()` for SwiGLU or GELU activations
- Changing the sliding window pattern from `"SSSL"` to `"SSLL"` or all-local `"S"`
- Adjusting the number of KV heads (grouped-query attention variants)
- Modifying the depth/width tradeoff via `ASPECT_RATIO` and `DEPTH`
- Adding or removing value embeddings, skip connections, or residual scaling

**Value:** Rapidly tests dozens of architectural ideas under identical, fair conditions (same time budget, same evaluation metric) — something that would take a human researcher days of manual iteration.

---

## 3. Optimizer Research

**Scenario:** The codebase uses a hybrid Muon + AdamW optimizer. You want to explore whether alternative optimizer configurations or entirely different optimization strategies yield better results.

**Example experiments:**
- Tuning Muon momentum schedules and learning rate scaling
- Adjusting AdamW beta values and weight decay
- Experimenting with warmup/warmdown ratios
- Modifying the cautious weight decay or NorMuon variance reduction parameters
- Trying different parameter groupings (which params get Muon vs. AdamW)

**Value:** Optimizer tuning is notoriously tedious. An autonomous agent can explore the space methodically while tracking every result, building up an empirical picture of what works.

---

## 4. Educational Tool for ML Students

**Scenario:** A student learning about transformer architectures wants hands-on experience seeing how different design choices affect model performance — without needing deep ML expertise.

**How to use it:**
1. Run `uv sync && uv run prepare.py` to set up the environment.
2. Manually edit `train.py` to try an idea (e.g., double the model depth, halve the batch size).
3. Run `uv run train.py` and observe the `val_bpb` result after 5 minutes.
4. Or, let the AI agent run autonomously and study the `results.tsv` log to see which ideas worked and which didn't.

**Value:** The fixed 5-minute time budget makes experimentation low-cost. Students can rapidly build intuition about what matters in LLM training (depth vs. width, learning rates, attention patterns) by reviewing agent-generated experiment logs.

---

## 5. Benchmarking Hardware Platforms

**Scenario:** You want to compare how different GPU platforms (H100, A100, RTX 4090, etc.) perform for LLM training under identical conditions.

**How it works:**
- Run the same baseline `train.py` on each platform.
- The fixed 5-minute wall-clock budget means each platform trains as many tokens as it can within the budget.
- Compare `val_bpb`, `total_tokens_M`, `mfu_percent`, and `peak_vram_mb` across platforms.
- Optionally, let the agent optimize `train.py` independently on each platform to find the best configuration for each GPU.

**Value:** Provides a standardized, reproducible benchmark for comparing GPU training throughput and efficiency on a real LLM workload — not just synthetic benchmarks.

---

## 6. Research Team Competitions

**Scenario:** A research lab or ML study group wants to run a friendly competition: who can achieve the lowest `val_bpb` on the same hardware?

**How it works:**
- Each participant forks the repo and creates their own `autoresearch/<name>` branch.
- Everyone starts from the same baseline and has the same 5-minute-per-experiment constraint.
- Participants can either manually iterate on `train.py` or customize `program.md` to guide the agent differently.
- After a fixed period (e.g., overnight), compare final `val_bpb` scores.

**Value:** Gamifies ML research. The constrained, reproducible setup creates a level playing field, and the agent-driven approach means participants compete on strategy (what to explore) rather than just engineering effort.

---

## 7. Ablation Studies

**Scenario:** You've added a feature to your model (e.g., value embeddings, residual lambdas, RoPE) and want to rigorously measure its contribution.

**How it works:**
- Start from the current best `train.py`.
- Instruct the agent (via `program.md`) to systematically remove one feature at a time and measure the impact on `val_bpb`.
- The agent commits each ablation, runs training, records the result, and reverts if the removal hurts.

**Value:** Automated ablation studies that would otherwise require careful manual setup. The git-based workflow preserves every variant for later review.

---

## 8. Meta-Research on Agent Prompting

**Scenario:** You want to study how different agent instructions in `program.md` affect research quality and progress.

**How it works:**
- Create multiple branches, each with a different `program.md` strategy:
  - One focused on aggressive architectural changes
  - One focused on conservative hyperparameter tuning
  - One that encourages combining near-misses
  - One with explicit research heuristics (e.g., "always try the opposite of what failed")
- Run each agent overnight and compare the trajectories in their respective `results.tsv` files.

**Value:** Turns the research process itself into a research question. Helps discover what kind of instructions produce the most effective autonomous AI researchers.

---

## 9. Rapid Prototyping for Paper Ideas

**Scenario:** A researcher reads a new paper describing a novel attention mechanism or training trick and wants to quickly test whether it helps on a small-scale LLM setup before investing in a full-scale run.

**How it works:**
- Implement the idea in `train.py` (or describe it in `program.md` and let the agent implement it).
- Run a 5-minute training experiment to get a quick signal.
- If `val_bpb` improves, invest in a larger-scale experiment elsewhere. If not, move on.

**Value:** 5-minute feedback cycles turn paper ideas into empirical results within minutes instead of hours or days. The single-file constraint forces clean, minimal implementations.

---

## 10. Custom Dataset Exploration

**Scenario:** You want to train small language models on domain-specific data (code, legal text, medical records) and find the best architecture for that domain.

**How it works:**
- Fork the repo and modify `prepare.py` to point at your custom dataset (e.g., swap in a Hugging Face dataset of code or a local parquet collection).
- Adjust `VOCAB_SIZE` and `MAX_SEQ_LEN` to match your domain's characteristics.
- Let the agent autonomously search for the best model configuration for your specific data distribution.

**Value:** Different data distributions benefit from different architectures. Autoresearch lets you discover domain-specific optima without manual tuning.

---

## Summary

| Use Case | Who Benefits | Key Advantage |
|---|---|---|
| Overnight hyperparameter search | Individual researchers | Hands-free optimization while you sleep |
| Architecture exploration | ML engineers | Fair comparison under fixed compute budget |
| Optimizer research | Optimization researchers | Systematic exploration of optimizer design space |
| Educational tool | Students | Low-cost experimentation, rapid intuition building |
| Hardware benchmarking | Infrastructure teams | Standardized, real-workload GPU comparison |
| Team competitions | Research groups | Gamified, reproducible ML challenges |
| Ablation studies | Paper authors | Automated, git-tracked feature contribution analysis |
| Meta-research on prompting | AI researchers | Study what makes effective autonomous agents |
| Rapid prototyping | Paper readers | 5-minute signal on new ideas |
| Custom dataset exploration | Domain specialists | Discover domain-specific model optima |
