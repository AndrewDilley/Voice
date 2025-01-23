import re

# Regex pattern
name_pattern = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*|[A-Z](?:\.|[a-z]+)?(?:\s[A-Z](?:\.|[a-z]+)?)*\s[A-Z][a-z]+)\b"

# Test cases
test_text = """
Andrew
Andrew Dilley
Andrew J Dilley
Andrew J. Dilley
AJ Dilley
A Dilley
A. J. Dilley
AJ. Dilley

Mr Andrew Dilley and Mrs Anthea Roberts

Mr Andrew Dilley & Mrs Anthea Roberts

Mr. Andrew Dilley and Mrs Anthea Roberts

Mr. Andrew Dilley and Mrs. Anthea Roberts

Andrew and Anthea

Mr. Dilley and Mrs. Roberts


"""

matches = re.findall(name_pattern, test_text)
for match in matches:
    print(match)



#text = re.sub(fr"\b(?:\d+/)?\d+[a-zA-Z]?\s+\w+(?:\s\w+)*\s{street_types}(?:,?\s\w+(?:\s\w+)*)?(?:,?\s\d{{4}})?(?:,?\s{state_types})?(?:,?\s\d{{4}})?\b", "[REDACTED ADDRESS]", text, flags=re.IGNORECASE)
 
    #names

    #text = re.sub(fr"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*|[A-Z](?:\.|[a-z]+)?(?:\s[A-Z](?:\.|[a-z]+)?)*\s[A-Z][a-z]+)\b", "[REDACTED PERSONS NAME]", text, flags=re.IGNORECASE)
