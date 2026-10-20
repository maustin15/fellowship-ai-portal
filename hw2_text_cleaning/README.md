# HW2: Cleaning a Corrupt Movie Corpus

Python script that cleans a corrupted corpus of movie script dialogue.

## Files

| File | What it is |
| --- | --- |
| `corrupt_movie_corpus.txt` | Dirty input (304,713 lines, about 20 MB) |
| `sample_10_lines.txt` | 10 random lines used to test the cleaning before running it on the full file |
| `clean.py` | Cleaning code |
| `clean_movie_corpus.txt` | Cleaned output (304,713 lines, about 17 MB) |

## Run it

```
uv run clean.py
```

No extra packages needed. It only uses Python's built-in `re`, `html`, and `random` modules.

## Issues I found

- **HTML tags** thrown into the text: `<b>`, `</b>`, `<i>`, `</span>` (about 114,000 each), plus some `<u>` and `<PRE>`
- **Random symbols** standing alone between words: `@`, `$`, `%`, `^^` (about 114,000 each)
- **HTML entities** like `&quot;`, `&amp;`, `&lt;`, `&gt;`
- **Leftover dataset delimiter** `+++$+++` (267 times)
- **Extra spaces** left behind between words
- **OCR typos** from the scanned scripts, like `CoghilL`, `ft` instead of `It`, `I'11` instead of `I'll`, and stray page numbers at the end of some lines

## What the script does

1. Converts HTML entities back to normal characters (`&quot;` becomes `"`)
2. Removes HTML tags with regex
3. Removes the `+++$+++` delimiter
4. Removes `@`, `$`, `%`, and `^^` only when they stand alone. That way real values like `$500` and `100%` stay.
5. Collapses extra spaces into one and trims each line
6. Drops any line that ends up empty

## Choices I made

- **Kept capitalization, punctuation, and stop words.** This project builds toward text generation, so the model needs natural sentences.
- **Left the OCR typos alone.** Fixing them would need a spell checker, and that could also "fix" real names like Coghill and Durnford.
- **Kept duplicate lines.** Short lines like "Yes." show up a lot in real dialogue.
