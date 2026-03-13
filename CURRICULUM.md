# Autoresearch Curriculum

**Learn how LLMs actually work — by training one yourself.**

This is a hands-on curriculum built on top of [autoresearch](https://github.com/troyscott/autoresearch). No math prerequisites. No PhD required. You'll train a small GPT model, break it on purpose, fix it, and build intuition for how the technology behind ChatGPT, Claude, and every other LLM actually works.

---

## Who This Is For

You're a business or technology professional who:
- Uses LLMs daily but doesn't understand what's happening under the hood
- Has Python basics (can read code, run scripts, use a terminal)
- Wants to go deeper than API wrappers and prompt engineering
- Has access to a GPU (RunPod, Lambda, or your own NVIDIA card)

You do **not** need: linear algebra, calculus, a CS degree, or prior ML experience.

## What You'll Learn

By the end of this curriculum, you will:
- Understand what a transformer is and how it processes text
- Know what hyperparameters control and how to tune them
- Be able to read training logs and diagnose problems
- Have hands-on experience modifying a real training script
- Understand what an autonomous AI research agent does and how to run one

## How It Works

Every module follows the same loop:

1. **Read** — learn a concept with a plain-English analogy
2. **Predict** — before running anything, write down what you *think* will happen
3. **Experiment** — make one change to `train.py`, run training for 5 minutes
4. **Reflect** — compare your prediction to reality, update your mental model

This is how real ML researchers work. The only difference is you're doing it with a safety net — a single file, a 5-minute time budget, and git to undo mistakes.

## Time Estimates

| Module | Topic | Time |
|--------|-------|------|
| 1 | Orientation | 30 min |
| 2 | The Transformer | 60 min |
| 3 | Hyperparameters | 90 min |
| 4 | Architecture Experiments | 90 min |
| 5 | The Optimizer | 60 min |
| 6 | Reading Your Results | 45 min |
| 7 | Autonomous Research | 2-8 hours (mostly waiting) |
| 8 | Next Steps | 30 min |

**Total: ~7-14 hours** (spread over a weekend or a week of evenings)

---

## Module 1: Orientation — "What Are We Even Doing?"

### The Big Picture

Think of this project like a science lab. There are three roles:

- **The lab rat** — a small GPT model (~124M parameters). It can't do anything useful yet. It just learns patterns in text.
- **The scientist** — you (or later, an AI agent like Claude). You modify the training recipe and observe the results.
- **The lab notebook** — `results.tsv`, where every experiment gets logged.

The rat doesn't know it's in an experiment. It just trains. The scientist's job is to figure out which changes make the rat smarter (lower loss) without blowing up the lab (running out of GPU memory).

### The Three Files That Matter

```
autoresearch/
├── prepare.py    # Downloads data and builds a tokenizer. DO NOT EDIT.
├── train.py      # The training recipe. THIS IS WHAT YOU EDIT.
└── program.md    # Instructions for AI agents. Read it later.
```

That's it. The entire codebase is ~1,000 lines of Python.

### Setup

```bash
# Install the uv package manager (if you don't have it)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and set up
git clone https://github.com/troyscott/autoresearch.git
cd autoresearch
uv sync

# Download data and train a tokenizer (~2 minutes)
uv run prepare.py
```

### Your First Training Run

```bash
uv run train.py
```

This trains a small GPT model for 5 minutes. When it finishes, you'll see output like this:

```
---
val_bpb:          1.234567
training_seconds: 300.1
total_seconds:    340.2
peak_vram_mb:     12345.6
mfu_percent:      45.67
total_tokens_M:   234.5
num_steps:        450
num_params_M:     124.3
depth:            8
```

### What Each Metric Means

| Metric | Plain English | Analogy |
|--------|--------------|---------|
| `val_bpb` | How surprised the model is by text it hasn't seen. Lower = better. | Like a student's test score — but inverted. 1.0 is pretty good, 2.0 is struggling. |
| `peak_vram_mb` | How much GPU memory was used. | Like RAM usage on your laptop. If it exceeds your GPU's capacity, training crashes. |
| `mfu_percent` | What fraction of the GPU's theoretical speed you're actually using. | Like fuel efficiency — 50% MFU means you're using half the GPU's potential. |
| `training_seconds` | Wall-clock training time (excluding startup/compilation). | The experiment timer. Always ~300 seconds (5 minutes). |
| `total_tokens_M` | How many millions of tokens the model saw during training. | Like "pages read" during a study session. More tokens = more practice. |
| `num_steps` | Number of optimizer steps (weight updates). | Each step is one "lesson" for the model. |
| `num_params_M` | Number of trainable parameters in millions. | The model's "brain size." More params = more capacity, but also more memory. |
| `depth` | Number of transformer layers. | How many times the model re-reads and re-thinks the text. |

### Experiment Card 1: Run the Baseline

**Goal:** Get comfortable with the workflow.

1. Run `uv run train.py` and wait ~5 minutes
2. Write down the `val_bpb` and `peak_vram_mb` values
3. These are your **baseline numbers** — every future experiment compares against them

That's it. You just trained a language model from scratch.

---

## Module 2: The Transformer — "How Does This Thing Work?"

### The Assembly Line Analogy

A transformer is like a document-processing assembly line. Raw text goes in one end. Predictions about the next word come out the other. In between, the text passes through a series of identical workstations (layers), each doing two jobs:

1. **Attention** — "What context matters here?"
2. **MLP** — "Given that context, what should I think?"

### Block-by-Block Tour of train.py

Open `train.py` and follow along. Every component has a real-world analogy:

#### Embeddings (line 130-131: `wte`)

```python
"wte": nn.Embedding(config.vocab_size, config.n_embd),
```

**What it does:** Converts each token (a number representing a word-piece) into a vector of 768 numbers.

**Analogy:** A dictionary that converts words into GPS coordinates. "Cat" might become `[0.2, -0.5, 0.8, ...]`. Similar words end up at nearby coordinates. The model starts with random coordinates and learns better ones during training.

#### Attention (lines 61-96: `CausalSelfAttention`)

```python
q = self.c_q(x)  # "What am I looking for?"
k = self.c_k(x)  # "What do I contain?"
v = self.c_v(x)  # "What information do I share?"
```

**What it does:** Each token looks at every previous token and decides which ones are relevant. It computes Query ("what am I looking for?"), Key ("what do I have?"), and Value ("what should I share?") vectors.

**Analogy:** A meeting where everyone sits in a row. Each person can only look at people to their left (causal = no peeking at the future). They vote on who has the most relevant information, then collect a weighted summary. The word "bank" in "river bank" pays heavy attention to "river" to understand its meaning.

#### Sliding Windows (lines 195-206: `window_sizes`)

```python
WINDOW_PATTERN = "SSSL"  # S=half context, L=full context
```

**What it does:** Some layers only let tokens look at nearby tokens (short window), while others see the full context (long window).

**Analogy:** Like reading a document — sometimes you focus on the current paragraph (short window), and sometimes you reference the introduction (long window). The pattern `SSSL` means three local-focus layers followed by one big-picture layer, repeated.

#### MLP (lines 99-109: `MLP`)

```python
x = self.c_fc(x)       # expand to 4x wider
x = F.relu(x).square() # activate (ReLU²)
x = self.c_proj(x)     # project back down
```

**What it does:** After attention gathers context, the MLP "thinks" about it. It expands the representation to 4x wider, applies a non-linear activation function (ReLU²), then compresses back.

**Analogy:** After the meeting (attention), each person goes to their desk and does focused thinking. They spread their notes out on a big desk (expand 4x), process them (activation), then summarize back into a compact memo (compress).

#### Residual Connections (lines 118-121: `Block.forward`)

```python
x = x + self.attn(norm(x), ...)  # add attention output to input
x = x + self.mlp(norm(x))        # add MLP output to input
```

**What it does:** Instead of replacing the input, each layer *adds* its output to the input. This creates a "skip connection."

**Analogy:** Like keeping your original notes while adding new ones. Each layer adds refinements on top, rather than starting from scratch. This makes training much more stable — if a layer has nothing useful to add, it can learn to output zeros and pass the input through unchanged.

#### Normalization (line 43-44: `norm`)

```python
def norm(x):
    return F.rms_norm(x, (x.size(-1),))
```

**What it does:** Scales the numbers in each vector so they don't grow too large or too small.

**Analogy:** Like keeping everyone on the same measuring system. Without normalization, some layers might work in "meters" while others work in "millimeters" — the numbers would explode or vanish.

#### Residual Lambdas (lines 134-135, 277)

```python
self.resid_lambdas = nn.Parameter(torch.ones(config.n_layer))
self.x0_lambdas = nn.Parameter(torch.zeros(config.n_layer))
# ...
x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
```

**What it does:** Each layer has learnable weights that control how much of the running representation (`x`) versus the original input (`x0`) to use.

**Analogy:** Like a mixing board in a recording studio. `resid_lambdas` controls the volume of the "processed" signal, and `x0_lambdas` controls how much of the "original, unprocessed" signal to mix back in.

#### Value Embeddings (lines 139-142, 278)

```python
self.value_embeds = nn.ModuleDict({...})
# ...
ve = self.value_embeds[str(i)](idx)
```

**What it does:** Some layers get an extra embedding that feeds directly into the attention values. This gives the model a shortcut to access token identity without it having to survive through all the previous layers.

**Analogy:** Like having the original document on your desk alongside your evolving notes. Even deep in the assembly line, you can glance back at the raw source material.

#### Logit Softcapping (lines 282-285)

```python
softcap = 15
logits = softcap * torch.tanh(logits / softcap)
```

**What it does:** Prevents the model's output scores from growing too extreme. Squashes values into the range [-15, 15].

**Analogy:** Like a governor on an engine — prevents the model from being *too* confident about any prediction, which helps training stability.

### Recommended Reading

If you want to go deeper on any component:
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) by Jay Alammar — the best visual explanation
- *Build a Large Language Model (From Scratch)* by Sebastian Raschka — Chapters 3-4 cover attention and transformers

### Experiment Card 2: What Happens Without the MLP?

**Goal:** See how important the "thinking step" is.

**Predict first:** If we remove the MLP from each layer, will `val_bpb` get better, worse, or stay the same? By how much? Write it down.

**Steps:**
1. Open `train.py`
2. Find the `Block.forward` method (line 118)
3. Comment out the MLP line:
```python
def forward(self, x, ve, cos_sin, window_size):
    x = x + self.attn(norm(x), ve, cos_sin, window_size)
    # x = x + self.mlp(norm(x))  # DISABLED
    return x
```
4. Run `uv run train.py`
5. Compare `val_bpb` to your baseline

**Reflect:** Was your prediction right? The MLP contains about 2/3 of the model's parameters. What does this tell you about the division of labor between attention and the MLP?

**Cleanup:** Undo your change with `git checkout train.py`

---

## Module 3: Hyperparameters — "The Knobs and Dials"

### What Are Hyperparameters?

In `train.py`, lines 432-451 define the "knobs" you can turn:

```python
ASPECT_RATIO = 64       # model_dim = depth * ASPECT_RATIO
HEAD_DIM = 128          # target head dimension for attention
WINDOW_PATTERN = "SSSL" # sliding window pattern

TOTAL_BATCH_SIZE = 2**19  # ~524K tokens per optimizer step
EMBEDDING_LR = 0.6
UNEMBEDDING_LR = 0.004
MATRIX_LR = 0.04
SCALAR_LR = 0.5
WEIGHT_DECAY = 0.2
ADAM_BETAS = (0.8, 0.95)
WARMUP_RATIO = 0.0
WARMDOWN_RATIO = 0.5
FINAL_LR_FRAC = 0.0

DEPTH = 8
DEVICE_BATCH_SIZE = 128
```

These are the settings the scientist can adjust *without* changing the model's architecture. Think of them like the settings on an oven — the recipe (architecture) stays the same, but you adjust the temperature and timing.

### The Key Knobs

#### Learning Rate — "The Thermostat"

The learning rate controls how big of a step the model takes when it updates its weights after each batch of data.

**Analogy:** Imagine you're tuning a thermostat. Too high, and the temperature swings wildly — overshooting and undershooting (training diverges, loss goes to NaN). Too low, and it takes forever to reach the right temperature (model barely improves in 5 minutes). The sweet spot is just right: fast progress without instability.

In this codebase, there are *four* separate learning rates because different parts of the model learn differently:
- `MATRIX_LR = 0.04` — the main transformer weights (uses Muon optimizer)
- `EMBEDDING_LR = 0.6` — the token embeddings (uses Adam)
- `UNEMBEDDING_LR = 0.004` — the output head (uses Adam)
- `SCALAR_LR = 0.5` — the per-layer mixing weights (uses Adam)

#### Batch Size — "Reading Reviews Before Buying"

`TOTAL_BATCH_SIZE = 2**19` means the model sees ~524,288 tokens before each weight update.

**Analogy:** Before making a purchase decision (weight update), you read customer reviews (data samples). Read too few reviews and your decision is noisy — you might overreact to one bad review. Read too many and you waste time — you already had enough information after 50 reviews, but you read 5,000.

Larger batch sizes give more stable gradients but fewer total steps in the 5-minute window.

#### Depth — "The Org Chart"

`DEPTH = 8` means 8 transformer layers stacked on top of each other. The model dimension is computed as `DEPTH * ASPECT_RATIO = 8 * 64 = 512`, rounded up to a multiple of `HEAD_DIM = 128`, giving `n_embd = 512`.

**Analogy:** Think of an organization. `DEPTH` is how many levels of management there are. `ASPECT_RATIO` controls how wide each level is (how many people per floor). A deep-and-narrow org (high depth, low width) has many layers of review but few people at each layer. A shallow-and-wide org (low depth, high width) has fewer layers but more parallel capacity.

With `ASPECT_RATIO = 64` fixed, changing `DEPTH` changes *both* the number of layers *and* the model width simultaneously.

### Guided Experiments

For each experiment below, follow the **Predict → Run → Reflect** loop. Record results in `results.tsv`.

#### Experiment Card 3: Double the Learning Rate

**Change:** `MATRIX_LR = 0.04` → `MATRIX_LR = 0.08`

**Predict:** Will training be faster? Will it diverge? Write it down.

**Run:** `uv run train.py`

**Reflect:** Did the model learn faster per step, or did it become unstable? Check whether `val_bpb` improved or worsened.

**Cleanup:** `git checkout train.py`

#### Experiment Card 4: Halve the Batch Size

**Change:** `TOTAL_BATCH_SIZE = 2**19` → `TOTAL_BATCH_SIZE = 2**18`

**Predict:** Smaller batch = noisier gradients but 2x more steps in the same time budget. Net positive or negative?

**Run:** `uv run train.py`

**Reflect:** Compare total steps (`num_steps`) and `val_bpb` to baseline.

**Cleanup:** `git checkout train.py`

#### Experiment Card 5: Shallower Model (DEPTH 8 → 4)

**Change:** `DEPTH = 8` → `DEPTH = 4`

**Predict:** Half the depth = roughly half the parameters. Will we lose a lot of quality? Will we gain speed?

**Run:** `uv run train.py`

**Reflect:** Compare `val_bpb`, `num_params_M`, `peak_vram_mb`, and `num_steps`. Did the smaller model compensate by getting more training steps?

**Cleanup:** `git checkout train.py`

#### Experiment Card 6: Deeper Model (DEPTH 8 → 16)

**Change:** `DEPTH = 8` → `DEPTH = 16`

**Predict:** Double the depth ≈ 4x the parameters (because width scales with depth too). Will more capacity help, or will the model be too big to train well in 5 minutes?

**Run:** `uv run train.py`

**Reflect:** Watch `peak_vram_mb`. Did it fit? Compare `num_steps` — the bigger model takes longer per step, so it gets fewer steps. Was the tradeoff worth it?

**Cleanup:** `git checkout train.py`

#### Experiment Card 7: Binary Search for Best Learning Rate

**Goal:** Find the `MATRIX_LR` that gives the best `val_bpb`.

**Method:**
1. Start with 0.04 (baseline), 0.02 (half), and 0.08 (double)
2. Take the two best, pick the midpoint, and run again
3. Repeat 2-3 more times
4. Log every run in `results.tsv`

This is how real researchers tune hyperparameters — systematic search, not guessing.

---

## Module 4: Architecture Experiments — "Building a Better Brain"

### The Recipe Analogy

Architecture experiments are like modifying a recipe. You're not changing the oven temperature (hyperparameters) — you're changing the ingredients. Each experiment removes, swaps, or adds a component to see if the dish improves.

**Ablation** = removing an ingredient to see if anyone notices. In ML, it means disabling a feature to measure its contribution.

### Guided Experiments

#### Experiment Card 8: Swap Activation Functions

The MLP uses ReLU² (line 107):
```python
x = F.relu(x).square()  # ReLU²
```

Try replacing it with GELU, a smoother activation used in many popular models:
```python
x = F.gelu(x)  # GELU
```

Or try SwiGLU, which requires a gated architecture (changes the MLP structure):
```python
# In MLP.__init__, change c_fc to produce 2x output for gating:
self.c_gate = nn.Linear(config.n_embd, 4 * config.n_embd, bias=False)
# In MLP.forward:
x = F.silu(self.c_gate(x)) * self.c_fc(x)
```

**Predict → Run → Reflect** for each variant.

#### Experiment Card 9: Change the Window Pattern

The default pattern `SSSL` (line 435) means three short-window layers followed by one long-window layer.

Try these alternatives:
- `WINDOW_PATTERN = "SL"` — alternating short and long
- `WINDOW_PATTERN = "S"` — all short windows (fast but limited context)
- `WINDOW_PATTERN = "L"` — all long windows (slow but full context)

**Predict:** Which pattern will give the best `val_bpb`? Which will be fastest?

#### Experiment Card 10: Remove Value Embeddings

Value embeddings (lines 139-142) give some layers a direct shortcut to token identity. To disable them:

```python
# In GPT.__init__, replace the value_embeds dict with an empty one:
self.value_embeds = nn.ModuleDict({})
```

**Predict:** These are extra parameters that cost memory. Are they worth it?

#### Experiment Card 11: Remove Residual Lambdas

Residual lambdas (lines 134-135) control per-layer mixing. To use standard residual connections instead:

```python
# In GPT.forward, replace line 277:
# x = self.resid_lambdas[i] * x + self.x0_lambdas[i] * x0
x = x  # standard residual (just pass through)
```

**Predict:** Will removing the learned mixing weights hurt performance?

#### Experiment Card 12: Full Ablation Study

**Goal:** Run all four ablations above and rank the components by importance.

Make a table:

| Component Removed | Baseline BPB | New BPB | Delta | Importance Rank |
|-------------------|-------------|---------|-------|-----------------|
| MLP (Module 2) | | | | |
| Value embeddings | | | | |
| Residual lambdas | | | | |
| Short windows (all L) | | | | |

Which component matters most? Which matters least? This is the kind of analysis that fills academic papers.

---

## Module 5: The Optimizer — "How the Model Learns"

### What's an Optimizer?

When the model makes a prediction and gets it wrong, the optimizer decides *how* to adjust the weights. It's the "learning algorithm."

This codebase uses **two optimizers working together** (lines 356-427):

- **AdamW** — for embeddings and scalar parameters. A well-proven, widely-used optimizer.
- **Muon** — for the main matrix parameters. A newer, more experimental optimizer that uses orthogonalization.

You don't need to understand the math. Just know that they're two different strategies for updating weights, and different parts of the model respond better to different strategies.

### Learning Rate Schedule — "Parking a Car"

The learning rate isn't constant. It follows a schedule (lines 518-525):

```python
WARMUP_RATIO = 0.0    # no warmup
WARMDOWN_RATIO = 0.5  # spend last 50% of time slowing down
FINAL_LR_FRAC = 0.0   # end at zero learning rate
```

**Analogy:** Parking a car. You drive at full speed in the open road (full LR during training), then slow down as you approach the parking spot (warmdown), and come to a complete stop (final LR = 0). If you don't slow down, you'll overshoot and crash into the wall (loss spikes at the end).

The default schedule: 0% warmup → 50% constant → 50% linear decay to zero.

### Momentum — "A Rolling Ball"

Muon uses momentum (line 528-529):
```python
def get_muon_momentum(step):
    frac = min(step / 300, 1)
    return (1 - frac) * 0.85 + frac * 0.95
```

**Analogy:** A ball rolling downhill. Momentum means the optimizer doesn't just look at the current gradient — it also considers the direction it was already moving. High momentum (0.95) means the ball is heavy and takes longer to change direction. Low momentum (0.85) means it's more responsive but less stable. The schedule ramps from 0.85 to 0.95 over the first 300 steps.

### Guided Experiments

#### Experiment Card 13: Change the Warmdown Ratio

**Changes to try:**
- `WARMDOWN_RATIO = 0.0` — no cooldown at all (stop abruptly)
- `WARMDOWN_RATIO = 0.25` — shorter cooldown
- `WARMDOWN_RATIO = 0.75` — longer cooldown

**Predict:** What happens if you don't slow down before stopping? What if you slow down too early?

#### Experiment Card 14: Adjust Adam Betas

```python
ADAM_BETAS = (0.8, 0.95)  # (beta1, beta2)
```

- `beta1` controls momentum in Adam (how much past gradients influence the current step)
- `beta2` controls the adaptive learning rate (how past gradient magnitudes influence step size)

**Try:** `(0.9, 0.999)` — the PyTorch default. Compare to the current `(0.8, 0.95)`.

**Predict:** The default betas here are unusually low. Will standard betas work better?

#### Experiment Card 15: Change Weight Decay

```python
WEIGHT_DECAY = 0.2
```

Weight decay is a regularization technique that slowly shrinks weights toward zero, preventing the model from relying too heavily on any single feature.

**Analogy:** Like a "use it or lose it" policy at work. Weights that aren't actively useful get gradually reduced.

**Try:** `0.0` (no weight decay) and `0.5` (aggressive weight decay).

---

## Module 6: Reading Your Results — "The Scientist's Notebook"

### From Experiments to Insights

By now, you've run 10-15 experiments. Time to analyze the data.

### Using the Analysis Notebook

```bash
uv run jupyter notebook analysis.ipynb
```

The notebook (`analysis.ipynb`) automatically loads `results.tsv` and produces:
1. **Outcome summary** — how many experiments were kept vs. discarded vs. crashed
2. **BPB over time** — a chart showing the progression of your experiments
3. **Top hits** — your biggest improvements, ranked by delta

### Key Concepts

#### Signal vs. Noise

Small differences in `val_bpb` (< 0.005) might just be random noise — different random seeds, slightly different data ordering, etc. Be skeptical of tiny improvements. Meaningful changes are typically 0.01+ BPB.

#### Diminishing Returns

Your first improvements will be big. Later experiments will yield smaller and smaller gains. This is normal — you're approaching the limits of what this model size can achieve in 5 minutes.

**Analogy:** Like squeezing a sponge. The first squeeze gets a lot of water out. Each subsequent squeeze gets less and less.

#### The Pareto Frontier

Some changes improve `val_bpb` but increase `peak_vram_mb`. Others save memory but hurt quality. The Pareto frontier is the set of configurations where you can't improve one metric without worsening the other.

**Analogy:** Like comparing cars — some are fast, some are fuel-efficient. The "best" cars are the ones where you can't get more speed without losing fuel efficiency. Those are on the Pareto frontier.

### Experiment Card 16: Write Your Lab Report

**Goal:** Analyze your results and write a 1-paragraph summary.

Answer these questions:
1. What was your biggest improvement over baseline?
2. Which hyperparameter had the largest effect?
3. Which architectural component was most important (from your ablation study)?
4. What surprised you?

This is the same analysis process used in ML research papers. You're doing real science.

---

## Module 7: Autonomous Research — "Let the AI Scientist Run"

### From Manual to Autonomous

Everything you've done so far — modifying `train.py`, running experiments, logging results — is exactly what the AI agent does. The difference: it doesn't sleep.

### Setting It Up

1. Install [Claude Code](https://docs.anthropic.com/en/docs/claude-code) or another AI coding agent
2. Point it at `program.md` in this repo
3. Let it run

The agent will:
- Read `train.py` and understand the architecture
- Make a change (one variable, one idea)
- Run training for 5 minutes
- Check if `val_bpb` improved
- Keep the change or revert it
- Repeat — indefinitely

### What to Expect

- **First hour:** The agent explores obvious knobs (learning rate, depth, batch size) — similar to what you did in Modules 3-5
- **Hours 2-4:** It starts trying architectural changes (activation functions, attention patterns)
- **Overnight (8+ hours):** It accumulates 50-100 experiments. Some will be creative, some will crash, many will be discarded

### Experiment Card 17: Run the Agent

**Steps:**
1. Start the agent before bed (or during a meeting)
2. Let it run for at least 2 hours
3. When you come back, analyze `results.tsv` with the analysis notebook

**Compare:**
- How many experiments did the agent run vs. you?
- Which of the agent's changes overlapped with yours?
- Did the agent find improvements you missed?
- What was the agent's strategy? (Read the experiment descriptions in `results.tsv`)

---

## Module 8: Next Steps — "Where to Go From Here"

### You've Built Intuition. Now Go Deeper.

You now understand more about LLM training than most people who *use* LLMs daily. Here's where to go next:

### Custom Datasets

The default dataset is `climbmix-400b-shuffle` — a general web text mixture. You can train on domain-specific data by modifying `prepare.py`:
- Code (train a coding assistant)
- Legal documents
- Medical literature
- Your company's internal docs (with appropriate permissions)

### Scaling Up

This curriculum uses a single GPU and 5-minute runs. Real training uses:
- Multi-GPU setups (data parallelism, tensor parallelism)
- Hours to weeks of training
- Billions of parameters

Frameworks for scaling: [torchtune](https://github.com/pytorch/torchtune), [LitGPT](https://github.com/Lightning-AI/litgpt), [nanochat](https://github.com/karpathy/nanochat)

### From Pretraining to Chat

The model you trained just predicts the next token. To make a chatbot, you'd need:
1. **SFT (Supervised Fine-Tuning)** — train on question/answer pairs
2. **RLHF (Reinforcement Learning from Human Feedback)** — train on human preferences

This is how ChatGPT, Claude, and Gemini are built: pretrain → SFT → RLHF.

### Recommended Reading

| Resource | What It Covers | When to Read |
|----------|---------------|-------------|
| [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) | Visual attention walkthrough | During Module 2 |
| *Build a Large Language Model (From Scratch)* by Sebastian Raschka | End-to-end LLM implementation | After completing curriculum |
| [Andrej Karpathy's "Neural Networks: Zero to Hero"](https://karpathy.ai/zero-to-hero.html) | Video lecture series, from basics to GPT | Any time, as supplementary |
| [The Little Book of Deep Learning](https://fleuret.org/francois/lbdl.html) by Francois Fleuret | Compact visual reference | Keep as a reference guide |

---

## Appendix A: Glossary

| Term | Plain English | Analogy |
|------|--------------|---------|
| **Attention** | Mechanism for tokens to look at each other | A meeting where everyone votes on who to listen to |
| **BPB (Bits Per Byte)** | How surprised the model is by new text | A student's test score (inverted — lower is better) |
| **Batch size** | How many examples the model sees before updating | Reading reviews before making a purchase |
| **Embedding** | Converting a token to a vector of numbers | GPS coordinates for words |
| **Epoch** | One complete pass through the training data | Re-reading a textbook cover to cover |
| **Gradient** | Direction to adjust weights to reduce loss | A compass pointing toward "better" |
| **Learning rate** | How big of a step to take in the gradient direction | Thermostat sensitivity |
| **Loss** | How wrong the model's predictions are | Distance from the target |
| **MFU** | Model FLOPS Utilization — GPU efficiency | Fuel efficiency of a car |
| **MLP** | Feed-forward network inside each transformer layer | Focused thinking after gathering context |
| **Momentum** | Using past gradients to smooth updates | A rolling ball — direction carries forward |
| **Muon** | An optimizer that orthogonalizes gradients | A GPS that ensures steps are efficient (no redundant directions) |
| **Parameters** | The model's learnable weights | Knobs on a mixing board |
| **ReLU²** | Activation function: max(0, x)² | A gate that blocks negative signals and amplifies positive ones |
| **Residual connection** | Adding layer input to layer output | Keeping original notes while adding new ones |
| **RoPE** | Rotary Position Embedding — encodes token position | Timestamps on messages in a chat |
| **Softcap** | Limiting logit magnitudes | A speed governor on an engine |
| **Token** | A word-piece (subword unit) | A syllable or word fragment |
| **Transformer** | The full model architecture | A document-processing assembly line |
| **Warmdown** | Gradually reducing learning rate at end of training | Slowing down before parking |
| **Weight decay** | Regularization that shrinks weights toward zero | "Use it or lose it" policy |

## Appendix B: Troubleshooting

| Problem | Symptom | Fix |
|---------|---------|-----|
| Out of memory (OOM) | `CUDA out of memory` error | Reduce `DEVICE_BATCH_SIZE` (try 64 or 32) |
| Training diverges | Loss goes to NaN or jumps to 100+ | Reduce learning rates (halve `MATRIX_LR`) |
| Very slow training | MFU below 20%, few steps completed | Check that Flash Attention 3 loaded; ensure no other processes on GPU |
| Prepare fails | Can't download data | Check internet connection; try `uv run prepare.py` again |
| Low BPB improvement | Results barely change between experiments | Your change may be too small; try bolder modifications |
| Training crashes immediately | Error on first step | Check your edit for syntax errors; run `python -c "import train"` to test |

## Appendix C: Cost Estimate (Cloud GPU)

Using [RunPod](https://www.runpod.io/) or similar cloud GPU providers:

| GPU | Cost/Hour (approx) | Modules 1-6 | Module 7 (overnight) | Total |
|-----|--------------------:|:-----------:|:--------------------:|:-----:|
| H100 80GB | ~$3.50/hr | ~$15 | ~$28 | ~$43 |
| A100 80GB | ~$2.00/hr | ~$9 | ~$16 | ~$25 |
| RTX 4090 | ~$0.75/hr | ~$3 | ~$6 | ~$9 |

*Note: RTX 4090 may need reduced `DEVICE_BATCH_SIZE`. See README for smaller GPU recommendations.*
