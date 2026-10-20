import html
import random
import re

INPUT_FILE = "corrupt_movie_corpus.txt"
SAMPLE_FILE = "sample_10_lines.txt"
OUTPUT_FILE = "clean_movie_corpus.txt"

TAG_PATTERN = re.compile(r"</?(b|i|u|span|pre)>", re.IGNORECASE)

DELIMITER_PATTERN = re.compile(r"\+\+\+\$\+\+\+")

NOISE_PATTERN = re.compile(r"(?<!\S)(\^\^|[@$%])(?!\S)")

SPACES_PATTERN = re.compile(r"\s+")


def explore(lines):
    print(f"Total lines: {len(lines):,}")
    print(f"Total characters: {sum(len(line) for line in lines):,}")
    print("\nFirst 5 lines:")
    for line in lines[:5]:
        print("  ", line.rstrip())


def make_sample(lines, n=10):
    random.seed(42)
    sample = random.sample(lines, n)
    with open(SAMPLE_FILE, "w", encoding="utf-8") as f:
        f.writelines(sample)
    return sample


def clean_line(line):
    line = html.unescape(line)
    line = TAG_PATTERN.sub(" ", line)
    line = DELIMITER_PATTERN.sub(" ", line)
    line = NOISE_PATTERN.sub(" ", line)
    line = re.sub(r"<(\w+)>", r"\1", line)
    line = SPACES_PATTERN.sub(" ", line)
    return line.strip()


def clean_lines(lines):
    cleaned = []
    for line in lines:
        result = clean_line(line)
        if result:
            cleaned.append(result)
    return cleaned


def main():
    with open(INPUT_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    explore(lines)

    sample = make_sample(lines)
    print(f"\nSample saved to {SAMPLE_FILE}. Before and after:")
    for line in sample:
        print("  BEFORE:", line.rstrip())
        print("  AFTER: ", clean_line(line))
        print()

    cleaned = clean_lines(lines)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned) + "\n")

    print(f"Cleaned {len(lines):,} lines down to {len(cleaned):,}")
    print(f"Removed {len(lines) - len(cleaned):,} lines that were only noise")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
