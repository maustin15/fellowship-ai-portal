# Week 4: nanoGPT on Shakespeare

I trained Karpathy's nanoGPT on the Shakespeare character dataset on my CPU. Run 1 uses the settings from the slides. Each other run changes one setting so I could see what it does to the loss.

## Results

| Run | What I changed | Parameters | Final train loss | Final val loss |
| --- | --- | --- | --- | --- |
| 1 | Baseline (2000 iters, 4 layers, 128 embd, eval_iters 20) | 0.80M | 1.7648 | 1.8857 |
| 2 | max_iters 3000 | 0.80M | 1.6143 | 1.7970 |
| 3 | n_layer 6 | 1.19M | 1.8024 | 1.9197 |
| 4 | n_embd 256 | 3.16M | 1.5554 | 1.7528 |
| 5 | eval_iters 100 | 0.80M | 1.7904 | 1.9062 |

Every run started around 4.17 loss at step 0.

## What I noticed

**The loss goes down, fast at first and then slower.** In the baseline it dropped from 4.17 to 2.43 in the first 250 steps, then took the remaining 1750 steps to get to 1.76. Most of the easy learning happens early.

**More iterations lowered the loss.** Going from 2000 to 3000 steps took val loss from 1.89 to 1.80. The model just gets more practice. It also took about 50% longer.

**More layers did not help here.** 6 layers ended slightly worse than 4 (1.92 vs 1.89 val loss). A deeper model has more to learn, so 2000 steps probably isn't enough training for it to pay off. It was also slower per step (about 27ms vs 18ms).

**Bigger embeddings helped the most.** Doubling n_embd from 128 to 256 gave the lowest loss of every run (1.75 val loss). The model went from 0.80M to 3.16M parameters, and each step took over twice as long (about 42ms vs 18ms). The gap between train and val loss also got bigger (0.20 vs 0.12), which could be an early sign of overfitting.

**eval_iters doesn't change how the model trains.** It only controls how many batches get averaged when the loss is checked. A higher number gives a more reliable loss reading, but each check is slower (about 940ms vs 210ms). The small difference from the baseline comes from randomness, not from the setting itself.

**Val loss is always a little higher than train loss.** That makes sense because the val data is text the model never trained on.

## Takeaway

On this dataset the model size (embeddings) and training time (iterations) made the biggest difference. Adding layers without adding training time didn't help. Bigger models cost more time per step, so there's a tradeoff between how good the model gets and how long it takes.
