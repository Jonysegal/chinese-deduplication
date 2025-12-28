import re
from pathlib import Path
from typing import List, Set

# ===========================================
# CONFIG: Input and Output Filenames
# ===========================================
PRIOR_ANKI_CHARACTERS = Path("prior_anki_characters.txt")
PRIOR_LESSON_CHARACTERS = Path("prior_lesson_characters.txt")
PRIOR_LESSON_WORDS = Path("prior_lesson_words.txt")
PRIOR_LESSON_PHRASES = Path("prior_lesson_phrases.txt")

NEW_LESSON_WORDS = Path("new_lesson_words.txt")
NEW_LESSON_PHRASES = Path("new_lesson_phrases.txt")
NEW_LESSON_DUMP = Path("new_lesson_dump.txt")

OUTPUT_CHARACTERS = Path("output_characters.txt")
OUTPUT_WORDS = Path("output_words.txt")
OUTPUT_PHRASES = Path("output_phrases.txt")

DEBUG_BASELINE_CHARACTERS = Path("debug_baseline_characters.txt")

# ===========================================
# Helpers
# ===========================================

CHINESE_CHAR_RE = re.compile(r'[\u4e00-\u9fff]')

def require_file(path: Path) -> None:
    """Fail fast if a required input file is missing."""
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path} (resolved to: {path.resolve()})\n"
            f"Tip: Run this script from the folder containing your .txt files."
        )

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def read_lines(path: Path) -> List[str]:
    text = read_text(path)
    return [line.strip() for line in text.splitlines() if line.strip()]

def extract_chinese_chars(text: str) -> List[str]:
    return CHINESE_CHAR_RE.findall(text)

def chinese_chars_from_lines(lines: List[str]) -> Set[str]:
    chars: Set[str] = set()
    for line in lines:
        chars.update(extract_chinese_chars(line))
    return chars

def normalize_unit(text: str) -> str:
    return "".join(extract_chinese_chars(text))

# ===========================================
# Require input files (fail fast)
# ===========================================
for p in [
    PRIOR_ANKI_CHARACTERS,
    PRIOR_LESSON_CHARACTERS,
    PRIOR_LESSON_WORDS,
    PRIOR_LESSON_PHRASES,
    NEW_LESSON_WORDS,
    NEW_LESSON_PHRASES,
    NEW_LESSON_DUMP,
]:
    require_file(p)

print("Reading files from:")
for p in [
    PRIOR_ANKI_CHARACTERS,
    PRIOR_LESSON_CHARACTERS,
    PRIOR_LESSON_WORDS,
    PRIOR_LESSON_PHRASES,
    NEW_LESSON_WORDS,
    NEW_LESSON_PHRASES,
    NEW_LESSON_DUMP,
]:
    print(f"  - {p} -> {p.resolve()}")

# ===========================================
# Load all data
# ===========================================
prior_anki_lines = read_lines(PRIOR_ANKI_CHARACTERS)
prior_lesson_char_lines = read_lines(PRIOR_LESSON_CHARACTERS)
prior_lesson_word_lines = read_lines(PRIOR_LESSON_WORDS)
prior_lesson_phrase_lines = read_lines(PRIOR_LESSON_PHRASES)

new_lesson_word_lines = read_lines(NEW_LESSON_WORDS)
new_lesson_phrase_lines = read_lines(NEW_LESSON_PHRASES)
new_lesson_dump_text = read_text(NEW_LESSON_DUMP)

# ===========================================
# 1) Identify NEW CHARACTERS
# ===========================================
baseline_characters: Set[str] = set()
baseline_characters.update(chinese_chars_from_lines(prior_anki_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_char_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_word_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_phrase_lines))

new_chars: Set[str] = set()
new_chars.update(extract_chinese_chars(new_lesson_dump_text))
new_chars.update(chinese_chars_from_lines(new_lesson_word_lines))
new_chars.update(chinese_chars_from_lines(new_lesson_phrase_lines))

new_unique_chars = sorted(new_chars - baseline_characters)

OUTPUT_CHARACTERS.write_text("\n".join(new_unique_chars), encoding="utf-8")

# Write debug baseline so you can verify what the script thinks you already know
DEBUG_BASELINE_CHARACTERS.write_text("\n".join(sorted(baseline_characters)), encoding="utf-8")

# ===========================================
# 2) Identify NEW WORDS
# ===========================================
baseline_words: Set[str] = set()
for line in prior_anki_lines + prior_lesson_word_lines:
    w = normalize_unit(line)
    if w:
        baseline_words.add(w)

seen_new_words: Set[str] = set()
new_unique_words: List[str] = []

for line in new_lesson_word_lines:
    w = normalize_unit(line)
    if not w:
        continue
    if w in baseline_words:
        continue
    if w in seen_new_words:
        continue
    seen_new_words.add(w)
    new_unique_words.append(w)

OUTPUT_WORDS.write_text("\n".join(new_unique_words), encoding="utf-8")

# ===========================================
# 3) Identify NEW PHRASES
# ===========================================
baseline_phrases: Set[str] = set()
for line in prior_lesson_phrase_lines:
    p = normalize_unit(line)
    if p:
        baseline_phrases.add(p)

seen_new_phrases: Set[str] = set()
new_unique_phrases: List[str] = []

for line in new_lesson_phrase_lines:
    p = normalize_unit(line)
    if not p:
        continue
    if p in baseline_phrases:
        continue
    if p in seen_new_phrases:
        continue
    seen_new_phrases.add(p)
    new_unique_phrases.append(p)

OUTPUT_PHRASES.write_text("\n".join(new_unique_phrases), encoding="utf-8")

# ===========================================
# Console summary + sanity checks
# ===========================================
print("Done.")
print(f"- Baseline characters: {len(baseline_characters)} (debug written to {DEBUG_BASELINE_CHARACTERS})")
print(f"- New characters written to: {OUTPUT_CHARACTERS} ({len(new_unique_chars)} chars)")
print(f"- New words written to: {OUTPUT_WORDS} ({len(new_unique_words)} words)")
print(f"- New phrases written to: {OUTPUT_PHRASES} ({len(new_unique_phrases)} phrases)")

if new_unique_chars:
    print(f"- Sample new chars (first 30): {''.join(new_unique_chars[:30])}")
