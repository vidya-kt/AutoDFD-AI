# AutoDFD AI

AutoDFD AI is an AI-powered web application that automatically generates professional Data Flow Diagrams (DFDs) from natural language system descriptions. The application leverages Large Language Models (LLMs) through the Groq API to convert textual requirements into valid Mermaid.js diagrams with automatic DFD level detection.

---

## Features

- AI-powered Data Flow Diagram generation
- Automatic DFD level detection
  - Level 0 (Context Diagram)
  - Level 1 (Major Process DFD)
  - Level 2 (Detailed Process DFD)
- Mermaid.js diagram rendering
- Mermaid syntax generation
- PNG export
- PDF export
- Mermaid code copy functionality
- Input validation
- Ambiguous prompt detection
- Mermaid syntax cleaning and validation
- Responsive user interface

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Mermaid.js
- html2canvas
- jsPDF

### Backend
- Python
- Flask
- Groq API
- Llama 3.1 8B Instant
- Requests
- python-dotenv

---

## Project Structure

```
AutoDFD-AI/
│
├── app.py                     # Flask application entry point
├── config.py                  # Application configuration
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
├── .gitignore                 # Files and folders ignored by Git
├── .env                       # Environment variables (not included in repository)
│
├── routes/
│   ├── __init__.py
│   └── dfd_routes.py          # API routes for DFD generation
│
├── services/
│   ├── __init__.py
│   └── groq_service.py        # AI prompt generation and Groq API integration
│
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Input validation, Mermaid cleaning, and utility functions
│
├── templates/
│   ├── base.html              # Base HTML template
│   ├── index.html             # Main application page
│   └── result.html            # Result page template
│
├── static/
│   ├── css/
│   │   └── style.css          # Application styling
│   │
│   └── js/
│       └── script.js          # Frontend logic and Mermaid rendering
│
├── __pycache__/               # Python cache files (ignored)
└── venv/                      # Virtual environment (ignored)
```
---

## Workflow

1. User enters a natural language system description.
2. Input validation checks for invalid or ambiguous descriptions.
3. AI classifies the DFD level.
4. A level-specific prompt is generated.
5. The prompt is sent to the Groq API.
6. The AI generates Mermaid.js DFD syntax.
7. Mermaid syntax is cleaned and validated.
8. Mermaid.js renders the diagram.
9. Users can:
   - View the generated DFD
   - Copy Mermaid syntax
   - Download PNG
   - Download PDF

---

## DFD Levels Supported

### Level 0
Context Diagram representing the complete system as a single process.

### Level 1
Shows major business processes and data stores.

### Level 2
Shows detailed process decomposition with multiple subprocesses.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AutoDFD-AI.git

cd AutoDFD-AI
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key

GROQ_API_KEY=your_groq_api_key
```

---

### Run Application

```bash
python app.py
```

The application runs at

```
http://127.0.0.1:5001
```

---

## Example Input

```
Customer places an order through an ecommerce system.
The system validates the order, processes payment,
updates inventory, stores order details,
and sends confirmation to the customer.
```

---

## Example Output

- Generated Mermaid syntax
- AI-detected DFD level
- Interactive Mermaid diagram
- PNG export
- PDF export

---

## Project Features

- AI-based DFD generation
- Automatic DFD level detection
- Prompt engineering
- Mermaid syntax validation
- Diagram rendering
- Responsive web interface
- PDF export
- PNG export
- Error handling
- Input validation

---

## Future Enhancements

- UML Diagram Generation
- Flowchart Generation
- Sequence Diagram Generation
- Use Case Diagram Generation
- PlantUML Export
- Mermaid Live Editor Integration
- User Authentication
- Diagram History
- Cloud Deployment
- Multi-language Support

---

## Screenshots

Add screenshots of:

- Home Page
- DFD Generator
- Generated Diagram
- PDF Export

---

## Author

Vidya K T

MCA Student

Bangalore Institute of Technology

---

## License

This project is developed for educational and academic purposes.