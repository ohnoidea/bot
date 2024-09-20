import re
from datetime import datetime, time


def time_from_text(text: str) -> time:
    result = re.search(r'(\d+)[., :-](\d+)', text)
    if not result:
        return None

    try:
        t = datetime.strptime(' '.join(result.group(1, 2)), '%H %M').time()
    except:
        return None

    return t
