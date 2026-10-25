import re

def validate_pattern(pattern: str) -> str | None:
    if not pattern: return None
    try:
        re.compile(pattern)
        return None
    except re.error as e: return str(e)

def get_highlighted_segments(pattern: str, text: str) -> list[tuple[str, bool]]:
    if not pattern or not text: return [(text, False)]
    
    segments = []
    last_index = 0
    for match in re.finditer(pattern, text):
        start, end = match.span()
        if start > last_index:
            segments.append((text[last_index:start], False))
        segments.append((text[start:end], True))
        last_index = end
        
    if last_index < len(text):
        segments.append((text[last_index:], False))
        
    return segments