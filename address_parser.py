import re

def redact_addresses(text):
    # Define components of an Australian address
    street_types = r"(St|Street|Dv|Dve|Drive|Lane|Ln|Road|Rd|Court|Ct|Crescent|Cr|Cres|Highway|HWY|Hwy|Ave|Avenue|Boulevard|Way)"
    state_types = r"(ACT|Australian Capital Territory|NSW|New South Wales|NT|Northern Territory|QLD|Queensland|SA|South Australia|TAS|Tasmania|VIC|Victoria|WA|Western Australia)"
    # Match full addresses with unit numbers, street, city, state, and postal code
    address_pattern = fr"""
        \b                                  # Start at a word boundary
        (?:\d+/)?                           # Match optional unit numbers (e.g., 2/100)
        \d+[a-zA-Z]?                        # Match house/unit numbers (e.g., 2/100a)
        \s+\w+(?:\s\w+)*                    # Match street name (e.g., Nepean, Old Creek)
        \s{street_types}                    # Match street types (e.g., Road, St)
        (?:,?\s\w+(?:\s\w+)*)?               # Match optional suburb (e.g., Aspendale)
        (?:,?\s\d{{4}})?                     # Match optional postal code (e.g., 3290)
        (?:,?\s{state_types})?               # Match optional state/territory (e.g., Victoria)
        (?:,?\s\d{{4}})?                     # Match optional postal code (e.g., 3290)
        \b                                  # End at a word boundary
    """
    # Apply the regex with the IGNORECASE and VERBOSE flags
    redacted_text = re.sub(address_pattern, "[REDACTED ADDRESS]", text, flags=re.IGNORECASE | re.VERBOSE)
    return redacted_text

# Test the function
test_text = """
Please send the package to 5/100b Nepean Road 3195.
Is your address 3/100b Smith St, Collingwood, 3452, Victoria?
"""
redacted_result = redact_addresses(test_text)
print(redacted_result)
