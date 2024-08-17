from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify, send_file
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import json
from datetime import datetime

app = Flask(__name__)

load_dotenv()

# Configure Google AI
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Prompt template for resume parsing
RESUME_PARSE_PROMPT = """
Use {current_date} as the current date for your reference.

Resume content:
{resume_content}
You are a NER Extraction expert.
Parse the given resume and extract information in this format:
OUTPUT SCHEMAA :
{{
  "full_name": "",
  "skillset": [],
  "profile_summary": "",
  "mobile": "",
  "email": "",
  "linkedin": "",
  "alternate_number": "",
  "preferred_location": "",
  "current_location": "",
  "total_experience": "",
  "language_skills": [],
  "programming_languages": [],
  "experience": [
    {{
      "title": "",
      "company": "",
      "duration_from": "",
      "duration_to": "",
      "projects": [
        {{
          "name": "",
          "details": ""
        }}
      ]
    }}
  ],
  "education": [
    {{
      "institution": "",
      "degree": "",
      "passing_year": "",
      "grade": ""
    }}
  ]
}}

[INST]
0. Think in a step by step manner. eg To calculate total experience:
THOUGHT: I need to calculate total experience. The oldest date Mentioned in resume is ABC Month - YYYY Year and Newest Experience date is LatestExpDate. so the total experience is 
TotalExperience = LatestExpDate - OldestExpDate 
1. If the resume does not contain the information, leave the field blank.
2. Return only the JSON object without any additional text or explanation. Ensure that the output is valid JSON format.
3. Most importantly, be faithful to the resume text. Do not add any other text or explanation. All the information should be factually correct and as per the resume only.
[END_INST]
"""

@app.route('/', methods=['GET'])
def upload_ui():
    return render_template('upload.html')

@app.route('/api/upload_resume', methods=['POST'])
def api_upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        # Save the file temporarily
        temp_path = ".temp/temp_resume.pdf"
        file.save(temp_path)

        # Load and parse the PDF
        loader = PyPDFLoader(temp_path)
        pages = loader.load_and_split()

        # Combine all pages into a single text
        text_splitter = CharacterTextSplitter()
        texts = text_splitter.split_documents(pages)
        resume_content = " ".join([t.page_content for t in texts])

        # Get the current date
        current_date = datetime.now().strftime('%Y-%m-%d')
        prompt = RESUME_PARSE_PROMPT.format(resume_content=resume_content, current_date=current_date)
        
        try:
            response = model.generate_content(prompt)
            parsed_resume = json.loads(response.text.replace("```json", "").replace("```", ""))
        except Exception as e:
            return jsonify({"error": f"Error generating content: {str(e)}"}), 500
        finally:
            # Clean up the temporary file
            os.remove(temp_path)

        # Render the result in an HTML page
        return render_template('result.html', parsed_resume=parsed_resume)
    else:
        return jsonify({"error": "Unsupported file type. Please upload a PDF file."}), 400

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)
@app.route('/api/save_resume', methods=['POST'])
def save_resume():
    # Extract data from the form
    data = request.form.to_dict(flat=False)
    
    # Process and save the data as needed
    # For example, you might save it to a database or a file
    # Here we just print it to the console
    print(data)
    
    # Respond with a confirmation message or redirect as needed
    return jsonify({"status": "success", "message": "Resume updated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
