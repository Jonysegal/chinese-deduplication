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

# ===========================================
# Helpers
# ===========================================

CHINESE_CHAR_RE = re.compile(r'[\u4e00-\u9fff]')

def read_text(path: Path) -> str:
    """Read entire file as UTF-8, or return empty if missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def read_lines(path: Path) -> List[str]:
    """Read non-empty stripped lines."""
    text = read_text(path)
    return [line.strip() for line in text.splitlines() if line.strip()]

def extract_chinese_chars(text: str) -> List[str]:
    """Return a list of all Chinese characters in the input text."""
    return CHINESE_CHAR_RE.findall(text)

def chinese_chars_from_lines(lines: List[str]) -> Set[str]:
    """Return a set of Chinese characters across all lines."""
    chars: Set[str] = set()
    for line in lines:
        chars.update(extract_chinese_chars(line))
    return chars

def normalize_unit(text: str) -> str:
    """
    Keep only Chinese characters in a 'unit' (word or phrase).
    This lets you have messy lines but still compare on pure Chinese.
    """
    return "".join(extract_chinese_chars(text))

# ===========================================
# Load all prior reference data
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

# Characters already known
baseline_characters: Set[str] = set()
baseline_characters.update(chinese_chars_from_lines(prior_anki_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_char_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_word_lines))
baseline_characters.update(chinese_chars_from_lines(prior_lesson_phrase_lines))

# Characters from new lesson dump + explicit new words + phrases files
new_chars: Set[str] = set()
new_chars.update(extract_chinese_chars(new_lesson_dump_text))
new_chars.update(chinese_chars_from_lines(new_lesson_word_lines))
new_chars.update(chinese_chars_from_lines(new_lesson_phrase_lines))

# Only characters not seen before
new_unique_chars = sorted(new_chars - baseline_characters)

# Write one character per line
OUTPUT_CHARACTERS.write_text("\n".join(new_unique_chars), encoding="utf-8")

# ===========================================
# 2) Identify NEW WORDS
# ===========================================

# Words already known from Anki and prior lessons
baseline_words: Set[str] = set()
for line in prior_anki_lines + prior_lesson_word_lines:
    w = normalize_unit(line)
    if w:
        baseline_words.add(w)

# Words from new lesson — deduped, normalized, compared
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

# Phrases already known from prior lessons
baseline_phrases: Set[str] = set()
for line in prior_lesson_phrase_lines:
    p = normalize_unit(line)
    if p:
        baseline_phrases.add(p)

# Phrases from new lesson — deduped, normalized, compared
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
# Console summary
# ===========================================

print("Done.")
print(f"- New characters written to: {OUTPUT_CHARACTERS} ({len(new_unique_chars)} chars)")
print(f"- New words written to: {OUTPUT_WORDS} ({len(new_unique_words)} words)")
print(f"- New phrases written to: {OUTPUT_PHRASES} ({len(new_unique_phrases)} phrases)")
