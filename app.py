import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from openai import OpenAI
import docx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'

# Set OpenAI API key

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

# Function to rewrite text using GPT-4o Mini

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

     Inclusive language principles:
    - Avoid gendered terms unless specifically required. Use gender-neutral alternatives (e.g., "they/them" instead of "he/she").
    - Use respectful terminology for groups or communities (e.g., "person with disability" instead of "disabled person").
    - Avoid terms with negative connotations (e.g., "victim" should be replaced with "survivor").
    - Use simple, clear terms to accommodate readers with varying literacy levels.
    - Avoid referring to soneone's age unless it is relevant to the context.
    - Use culturally appropriate terms and avoid stereotypes (eg "First Nations Australians", or "Aboriginal and Torres Straight Islander peoples" are appropriate).
    - Use gender neutal terms like "chairperson" instead of "chairman" or "chairwoman".
    - Avoid asking for Christian name, use "first name" instead.
    - Avoid asking for surname, use "last name" instead.
    - avoid using "maiden name" use "birth name" instead.
    - Avoid using "husband" or "wife" use "spouse" instead.
    - Avoid using "mankind" use "humanity" instead.
    - avoid using "manpower" use "workforce" instead.
    - avoid using 'ladies and gentlemen' use 'everyone' instead.

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
        model="gpt-4o-mini",  # Ensure you have access to the GPT-4o Mini model
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
        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith('.docx'):
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filepath)
                doc = docx.Document(filepath)
                text = "\n".join([para.text for para in doc.paragraphs])
            else:
                return jsonify({"error": "Unsupported file format"}), 400
        else:
            text = request.form.get('text')
        if text:
            translated_text = rewrite_text(text)
            return jsonify({"translated": translated_text})
        return jsonify({"error": "No text provided"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)