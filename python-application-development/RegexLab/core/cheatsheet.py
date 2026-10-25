CHEATSHEET_DATA = {
    "Special Characters": {
        "\\": "escape special characters",
        ".": "matches any character\n(newlines only if DOTALL)",
        "^": "matches beginning of string",
        "$": "matches end of string",
        "[5b-d]": "matches '5', 'b', 'c' or 'd'",
        "[^a-c6]": "matches any char\nexcept 'a', 'b', 'c' or '6'",
        "R|S": "matches regex R or S",
        "()": "creates a capture group"
    },

    "Quantifiers": {
        "*": "0 or more",
        "+": "1 or more",
        "?": "0 or 1",
        "{m}": "exactly m occurrences",
        "{m,n}": "from m to n",
        "{m,n}?": "from m to n,\nas few as possible",
        "*?": "non-greedy"
    },

    "Special Sequences": {
        "\\A": "start of string",
        "\\b": "word boundary",
        "\\B": "not word boundary",
        "\\d": "digit",
        "\\D": "non-digit",
        "\\s": "whitespace",
        "\\S": "non-whitespace",
        "\\w": "alphanumeric",
        "\\W": "non-alphanumeric",
        "\\Z": "end of string"
    },

    "Groups & Lookarounds": {
        "(?i)(?m)(?s)(?x)": "sets re.X flags",
        "(?:...)": "non-capturing group",
        "(?P<n>...)": "named group",
        "(?#...)": "a comment",
        "(?=...)": "lookahead assertion",
        "(?!...)": "negative lookahead",
        "(?<=...)": "lookbehind assertion",
        "(?<!...)": "negative lookbehind",
        "(?(id)y|n)": "conditional match"
    }
}
