import os
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import docx
from dotenv import load_dotenv
import re
import json

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Set OpenAI API key
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


# Load glossary from JSON
with open("glossary.json", "r", encoding="utf-8") as f:
    glossary = json.load(f)


# Function to replace glossary terms in text
def apply_glossary(text):
    words = text.split()
    
    for key, value in glossary.items():
        key_variants = [k.strip().lower() for k in re.split(r"[/,]", key)]
        value_variants = [v.strip() for v in re.split(r"[/,]", value)]

        for key_variant in key_variants:
            pattern = r"\b" + re.escape(key_variant) + r"\b"
            if re.search(pattern, text, re.IGNORECASE):
                best_replacement = value_variants[0]  # Default first word
                if len(value_variants) > 1:
                    best_replacement = choose_best_replacement(text, value_variants)
                text = re.sub(pattern, best_replacement, text, flags=re.IGNORECASE)

    return text

# Function to choose the best word from multiple replacements
def choose_best_replacement(text, options):
    prompt = f"""
    Given the following sentence:
    "{text}"
    Choose the most appropriate word from this list: {', '.join(options)}
    Respond with only the single best word.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()



# Function to redact PII from the text
def redact_pii(text):
    import re
    # Redact email addresses
#    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "[REDACTED EMAIL]", text)
    # Redact phone numbers
 #   text = re.sub(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{1,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b", "[REDACTED PHONE]", text)
    # Redact credit card numbers
    text = re.sub(r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b", "[REDACTED CREDIT CARD]", text)


  # 2️⃣ Redact all phone numbers EXCEPT 1300 926 666
    text = re.sub(r"\b(?!1300\s?926\s?666)(\+?\d{1,4}[-.\s]?)?(\(?\d{1,4}\)?[-.\s]?)?\d{3,4}[-.\s]?\d{3,4}\b", "[REDACTED PHONE]", text)

    # 3️⃣ Redact all emails EXCEPT info@wannonwater.com.au
    text = re.sub(r"\b(?!info@wannonwater\.com\.au)([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b", "[REDACTED EMAIL]", text, flags=re.IGNORECASE)

    
    # Redact addresses
    #street_types = r"(St|Street|Dv|Dve|Drive|Lane|Ln|Road|Rd|Court|Ct|Crescent|Cr|Cres|Highway|HWY|Hwy|Ave|Avenue|Boulevard|Way)"
   
    # Define state and territory names
    #state_types = r"(ACT|Australian Capital Territory|NSW|New South Wales|NT|Northern Territory|QLD|Queensland|SA|South Australia|TAS|Tasmania|VIC|Victoria|WA|Western Australia)"
    
    #address_pattern = fr"\b(?:\d+/)?\d+[a-zA-Z]?\s+\w+(?:\s\w+)*\s{street_types}(?:,?\s\w+(?:\s\w+)*)?(?:,?\s\d{{4}})?(?:,?\s{state_types})?(?:,?\s\d{{4}})?\b"
    #text = re.sub(address_pattern, "[REDACTED ADDRESS]", text, flags=re.IGNORECASE)

    # name_pattern = r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)*|[A-Z](?:\.|[a-z]+)?(?:\s[A-Z](?:\.|[a-z]+)?)*\s[A-Z][a-z]+)\b"
    # text = re.sub(name_pattern, "[REDACTED NAME]", text)


    # Redact names (add known names as needed)
    # names = ["Wannon Water", "WW", "Wannon Region Water Corporation"]
    # for name in names:
    #     text = text.replace(name, "[REDACTED NAME]")


    # Redact personal names but keep addresses unchanged

    # Redact full names appearing on separate lines
    text = re.sub(r"(?m)^(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Madam|Mx)?\.?\s*[A-Z][a-z]+(?:\s[A-Z][a-z]+)*$", "[REDACTED NAME]", text, flags=re.IGNORECASE)
    # Redact names appearing within sentences (e.g., "Dear Mr. Dilley")
    text = re.sub(r"\b(?:Mr|Mrs|Ms|Miss|Dr|Prof|Sir|Madam|Mx)\.?\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", "[REDACTED NAME]", text, flags=re.IGNORECASE)
  
    return text




# Function to rewrite text using GPT-4o Mini
def rewrite_text(input_text):
    prompt = f"""
    You are an expert copy editor for Wannon Water. Rewrite the provided text to align with the "Our Voice Guide - January 2023" following these rules:
    - Informative: Clear and concise, avoiding jargon. Explain technical terms simply.
    - Neighborly: Warm and inclusive language. Avoid overly formal expressions.
    - Local Leader: Active voice and short, dynamic sentences.
    Example Rewrite:
    Input: "The community will be informed of a water outage."
    Output: "We'll let the community know about a water outage."

    

    # Start Version 2 changes - 18/2/25
    Use Australian English spelling and conventions.
    Maintain conversational tone, keeping contractions (e.g., "we'll" instead of "we will").
    Use fewer subheadings to maintain a smooth flow without unnecessary segmentation.
    # End Version 2 changes

    Ensure capitalization follows these rules:
    - Seasons like "summer" and "winter" should always be lowercase unless part of a title or proper noun.
    - Proper nouns like "Wannon Water" should always be capitalized.
    - Job titles, departments, and organizational names (e.g., "Operations Manager," "Digital Services Department") should be capitalized.

    Example Rewrite:
    Input: "Winter is coming, and the operations manager is ready to manage the seasonal changes."
    Output: "winter is coming, and the Operations Manager is ready to manage the seasonal changes."

    Ensure that all dates are formatted as "date month year" (e.g., 10 March 1996). Avoid using "10th of March, 1996" or formats like "03/10/1996."

    Example Rewrite:
    Input: "The project began on the 10th of March, 1996, and ended on 1996-03-15."
    Output: "The project began on 10 March 1996 and ended on 15 March 1996."

    Ensure that all times are formatted as follows:
    - Use lowercase "am" or "pm."
    - Do not include a space between the number and "am" or "pm" (e.g., "4pm" instead of "4 pm").
    - For times on the hour, do not include ":00" (e.g., "4pm" instead of "4:00pm").

    Example Rewrite:
    Input: "The meeting is scheduled for 4:00 PM and will end at 6:30 PM."
    Output: "The meeting is scheduled for 4pm and will end at 6:30pm."

    Ensure numbers 0–9 are written as numerals (e.g., 3).
    Write numbers 10 and above in words, except for measurements (e.g., length, money, temperature). For measurements, retain numerals (e.g., 12 km, $45 million, 25°C).

    Inclusive language principles:
    - Avoid gendered terms unless specifically required. Use gender-neutral alternatives (e.g., "they/them" instead of "he/she").
    - Use respectful terminology for groups or communities (e.g., "person with disability" instead of "disabled person").
    - Avoid terms with negative connotations (e.g., "victim" should be replaced with "survivor").
    - Use simple, clear terms to accommodate readers with varying literacy levels.
    - Avoid referring to someone's age unless it is relevant to the context.
    - Use culturally appropriate terms and avoid stereotypes (e.g., "First Nations Australians," or "Aboriginal and Torres Strait Islander peoples" are appropriate).
    - Use gender-neutral terms like "chairperson" instead of "chairman" or "chairwoman."
    - Avoid asking for Christian name; use "first name" instead.
    - Avoid asking for surname; use "last name" instead.
    - Avoid using "maiden name"; use "birth name" instead.
    - Avoid using "husband" or "wife"; use "spouse" instead.
    - Avoid using "mankind"; use "humanity" instead.
    - Avoid using "manpower"; use "workforce" instead.
    - Avoid using "ladies and gentlemen"; use "everyone" instead.

    Examples of inclusive rewriting:
    - Input: "Each employee should submit his timesheet."
      Output: "All employees should submit their timesheets."
    - Input: "The disabled will benefit from this project."
      Output: "People with disabilities will benefit from this project."

    Ensure the text includes subheadings where appropriate to break the content into logical sections. Subheadings should:
    - Be concise and descriptive.
    - Use sentence case (capitalize only the first word and proper nouns).
    - Provide a clear structure to the content.

    Example Rewrite:
    Input:
    "Our project involves several phases. First, we will upgrade the main pipeline. Then, we will expand the water treatment plant capacity. Lastly, we will implement new monitoring systems."

    Output:
    "Our project involves several phases:

    Upgrading the main pipeline
    We will start by upgrading the main pipeline to improve water flow and reliability.

    Expanding water treatment capacity
    Next, we will expand the water treatment plant capacity to meet future demand.

    Implementing new monitoring systems
    Lastly, we will implement advanced monitoring systems to ensure ongoing operational efficiency."

    Rewrite this: {input_text}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        text = request.form.get('text')
        if text:
            # Redact PII before sending to the LLM
            redacted_text = redact_pii(text)  # Step 1: Redact PII
            glossary_applied_text = apply_glossary(redacted_text)  # Step 2: Replace glossary words
            final_translation = rewrite_text(glossary_applied_text)  # Step 3: GPT refinement
           # final_translation = apply_glossary(final_translation)  # Step 4: Final glossary check
            return jsonify({"translated": final_translation})
        return jsonify({"error": "No text provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
