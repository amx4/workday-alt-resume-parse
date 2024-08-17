# Alternative to Workday : AI-Powered Resume Parser

This Flask application uses Google's Generative AI (Gemini Pro) to parse and extract structured information from PDF resumes.

## Features

- Upload PDF resumes through a web interface
- Parse resumes using advanced AI technology
- Extract key information such as personal details, work experience, education, skills, and more
- Download parsed resume data as JSON

## Prerequisites

- Python 3.12
- Flask
- langchain
- google-generativeai
- python-dotenv
- PyPDF2

## Setup

1. Clone the repository
2. Install dependencies:
```python3 pip install -r requirements.txt```


3. Set up your Google API key:
- Create a `.env` file in the project root
- Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`

## Usage

1. Run the application:
```python3 main.py```

2. Open a web browser and navigate to `http://localhost:5000`
3. Upload a PDF resume
4. View the parsed information and download the JSON file

## API Endpoint

The application provides an API endpoint for programmatic access:

- POST `/api/parse_resume`
- Upload a PDF file with the key 'resume'
- Returns parsed resume data as JSON

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
