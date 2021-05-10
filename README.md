# Notion Linter

This Python script helps you lint your Article in Notion:

- Fix Typo based on your dict
- Insert spaces between English, Chinese and Number

## Installation

```bash
    pip install -r requirements.txt
```

Follow the [guide](https://github.com/jamalex/notion-py), to set `token_v2 in` `linter.py L93` and `URL` in `linter.py L97`.
Notice that the notion passage cannot be a subpage.

## Roadmap

- Insert space between emojis and other texts
- Fix English and Chines punctuations(全角，半角符号)
- Add more to the dict
- Uppercase English word
