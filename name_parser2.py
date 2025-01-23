import probablepeople as pp
import re

def redact_names(text):
    try:
        # Parse the text to find names
        result, _ = pp.parse(text)
        # Loop through each part of the parsed text
        for part, label in result:
            if label in ["GivenName", "Surname", "MiddleInitial", "MiddleName", "Prefix", "Suffix"]:
                # Replace each part of the name with [REDACTED NAME]
                text = re.sub(rf"\b{re.escape(part)}\b", "[REDACTED NAME]", text, flags=re.IGNORECASE)
    except pp.RepeatedLabelError:
        pass  # Handle cases where probablepeople is unsure
    return text

# Test the function
test_text = "Andrew J. Dilley went to the store. He met with Dr. Jane Smith there."
redacted_result = redact_names(test_text)
print(redacted_result)
