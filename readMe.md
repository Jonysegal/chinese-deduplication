# Lesson Processing Script

## Overview

This project provides a Python script (`process_lessons.py`) that identifies **new Chinese characters**, **new Chinese words**, and **new Chinese phrases** from each new lesson.

It compares the content in your upcoming lesson against everything you have already learned and outputs only the new items, ready to paste into Google Sheets or feed into Anki.

---

## Input Files

Place the following `.txt` files in the same directory as `process_lessons.py`.  
All files must be UTF-8 text.

### `prior_anki_characters.txt`

Characters or words extracted from your Anki deck (one item per line).

### `prior_lesson_characters.txt`

Characters collected from prior lessons (one character per line).

### `prior_lesson_words.txt`

Words from previous lessons (one word per line).

### `prior_lesson_phrases.txt`

Phrases from previous lessons (one phrase per line).  
These are typically multi-character expressions you are tracking separately from single words.

### `new_lesson_words.txt`

Words you manually extract from the upcoming lesson (one word per line).

### `new_lesson_phrases.txt`

Phrases you extract from the upcoming lesson (one phrase per line).  
A convenient way to generate this file is:

1. Take the contents of `new_lesson_dump.txt`.
2. Paste it into an AI assistant.
3. Ask it to extract **useful Chinese phrases** (e.g., collocations, common sentence chunks, multi-character expressions) and return them as a **newline-delimited list**.
4. Paste that list into `new_lesson_phrases.txt`.

### `new_lesson_dump.txt`

Raw pasted text from the upcoming lesson.  
This can contain English, punctuation, numbers, etc. — the script automatically filters to only Chinese characters where appropriate.

---

## Output Files

The script generates three output files:

### `output_characters.txt`

All Chinese characters found in the new lesson that do **not** appear in any prior files  
(`prior_anki_characters`, `prior_lesson_characters`, `prior_lesson_words`, `prior_lesson_phrases`).  
One character per line.

### `output_words.txt`

All new Chinese words found in `new_lesson_words.txt` that are not already present in:

- `prior_anki_characters.txt` (if it contains words as well)
- `prior_lesson_words.txt`

One word per line.

### `output_phrases.txt`

All new Chinese phrases found in `new_lesson_phrases.txt` that are not already present in:

- `prior_lesson_phrases.txt`

One phrase per line.

All three outputs are formatted to be easy to copy into Google Sheets.

---

## How to Run

### 1. Ensure Python 3 is installed

Check with:

```bash
python3 --version
```

or on Windows:

```bash
python --version
```

### 2. Place all `.txt` files and `process_lessons.py` in the same directory

Example layout:

```text
process_lessons.py
prior_anki_characters.txt
prior_lesson_characters.txt
prior_lesson_words.txt
prior_lesson_phrases.txt
new_lesson_words.txt
new_lesson_phrases.txt
new_lesson_dump.txt
```

### 3. Run the script

Mac/Linux:

```bash
python3 process_lessons.py
```

Windows:

```bash
python process_lessons.py
```

### 4. Check the output files

```text
output_characters.txt
output_words.txt
output_phrases.txt
```

These contain the new characters, words, and phrases for this lesson.

5. **Use the outputs**

   - Copy `output_characters.txt`, `output_words.txt`, and `output_phrases.txt` into your Google Sheets。 Leave a comment at the start of the block for which lesson number the block comes from.

6. **Copy into Anki and add Audio**

   - Export the sheets as .tsv's and bring them into Anki. Because the decks are split between visual and audio you'll have to move the visual cards from the audio deck to the visual deck. Once all the cards are situated, add audio to them with the Anki extension.
