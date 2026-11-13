# Corpus inventory

Source: uploaded `corpus(4).json`, copied byte-for-byte to `data/corpus.json`.

## Top-level structure

| Section | Count / type |
|---|---:|
| `meta` | 6 |
| `vocabulary` | 250 |
| `phrases` | 100 |
| `stories_or_proverbs` | 25 |
| `quizzes` | 50 |
| `dialogues` | 10 |
| `riddles` | 19 |
| `grammar_rules` | 10 |

## Record counts

| Section | Records |
|---|---:|
| `vocabulary` | 250 |
| `phrases` | 100 |
| `stories_or_proverbs` | 25 |
| `quizzes` | 50 |
| `dialogues` | 10 |
| `riddles` | 19 |
| `grammar_rules` | 10 |

## Language field presence

Counts indicate records with a non-empty direct language field; nested multilingual fields may exist in other sections.

### `vocabulary`
| Language | Non-empty direct fields |
|---|---:|
| irula | 250 |
| english | 250 |
| tamil | 250 |
| telugu | 250 |
| hindi | 250 |

### `phrases`
| Language | Non-empty direct fields |
|---|---:|
| irula | 100 |
| english | 100 |
| tamil | 100 |
| telugu | 100 |
| hindi | 100 |

### `stories_or_proverbs`
| Language | Non-empty direct fields |
|---|---:|
| irula | 25 |
| english | 25 |
| tamil | 25 |
| telugu | 25 |
| hindi | 25 |

### `quizzes`
| Language | Non-empty direct fields |
|---|---:|
| irula | 0 |
| english | 0 |
| tamil | 0 |
| telugu | 0 |
| hindi | 0 |

### `dialogues`
| Language | Non-empty direct fields |
|---|---:|
| irula | 0 |
| english | 0 |
| tamil | 0 |
| telugu | 0 |
| hindi | 0 |

### `riddles`
| Language | Non-empty direct fields |
|---|---:|
| irula | 0 |
| english | 0 |
| tamil | 0 |
| telugu | 0 |
| hindi | 0 |

### `grammar_rules`
| Language | Non-empty direct fields |
|---|---:|
| irula | 0 |
| english | 0 |
| tamil | 0 |
| telugu | 0 |
| hindi | 0 |

## Validation notes

- Duplicate IDs within a section: 0.
- Records without an `id` field: 0 (counted by section occurrence).
- JSON parsing succeeded when this report was generated.
- Linguistic accuracy and native-speaker verification were not independently established by this structural check.
- Some records may use nested objects for translations or different field names; the app handles common shapes, but UI coverage may need refinement after manual testing.