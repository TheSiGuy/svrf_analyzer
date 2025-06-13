import re

def parse_svrf_rules(file_path):
    """
    Parses an SVRF file to extract rule names and their comments.

    Consecutive comment lines (@) at each rule block are combined into a single string separated by a single space

    Args:
        file_path (str): Path to the source file.

    Returns:
        List[dict]: A list of dictionaries with 'check name' and 'comment' keys.

    Example:
        Input file content:
            L.S.1 {
                @ This is a comment
                @ Continuation of the comment
                @ Continuation of the comment
                EXT L < 0.1
            }

        Output:
            [
                {
                    'check name': 'L.S.1',
                    'comment': 'This is a comment Continuation of the comment Continuation of the comment'
                }
            ]

    """
    with open(file_path, 'r') as f:
        text = f.read()

    # Match rule blocks: identifier followed by { ... }
    blocks = re.findall(r'([A-Za-z0-9_.]+)\s*\{([^}]*)\}', text, re.DOTALL)

    rules = []

    for name, content in blocks:
        lines = content.strip().splitlines()
        comment_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith('@'):
                comment_lines.append(stripped[1:].strip())  # Remove '@' and extra spaces
            else:
                break

        if comment_lines:
            comment = ' '.join(comment_lines)
            rules.append({
                'check name': name,
                'comment': comment
            })

    return rules
