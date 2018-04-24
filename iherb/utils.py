def parse_html_text_btw(text: str, left: str, right: str) -> str:
    text = text[text.find(left) + len(left):]
    return text[:text.find(right)]