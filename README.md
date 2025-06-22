# IELTS Writing Task Evaluator

An AI-powered application that evaluates IELTS General Training writing tasks using OpenAI's GPT-4 or Ollama's Llama 3.2 models. The system provides detailed feedback based on official IELTS scoring criteria.

## Features

- **Multi-Model Support**: Choose between ChatGPT (GPT-4) or Llama 3.2 for evaluation
- **IELTS-Compliant Scoring**: Evaluates based on official IELTS criteria:
  - Task Achievement/Task Response
  - Coherence & Cohesion
  - Lexical Resource
  - Grammatical Range & Accuracy
- **Task Support**: Handles both Task 1 (Letter Writing) and Task 2 (Essay Writing)
- **User-Friendly GUI**: Simple Tkinter interface for easy interaction
- **RESTful API**: FastAPI backend for programmatic access
- **Detailed Feedback**: Comprehensive scoring with specific feedback for each criterion

## Architecture

- **Backend**: FastAPI server (`app.py`)
- **Frontend**: Tkinter GUI application (`ielts_tkinter_app.py`)
- **AI Models**: OpenAI GPT-4 and Ollama Llama 3.2 integration

## Prerequisites

### Required Software

1. **Python 3.8+**
2. **Ollama** (if using Llama 3.2)
   - Install from [https://ollama.ai](https://ollama.ai)
   - Pull the Llama 3.2 model: `ollama pull llama3.2`
3. **OpenAI API Key** (if using ChatGPT)

### API Keys

- **OpenAI API Key**: Set as environment variable `OPENAI_API_KEY`
  ```bash
  export OPENAI_API_KEY="your-openai-api-key-here"
  ```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd ielts-writing-evaluator
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install additional dependencies** (if not in requirements.txt):
   ```bash
   pip install openai ollama
   ```

4. **Set up Ollama** (if using Llama 3.2):
   ```bash
   # Install Ollama first, then:
   ollama pull llama3.2
   ```

## Running the Application

### Method 1: GUI Application (Recommended for End Users)

1. **Start the FastAPI backend**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`

2. **In a separate terminal, start the GUI**:
   ```bash
   python ielts_tkinter_app.py
   ```

### Method 2: API Only (For Developers)

1. **Start the FastAPI server**:
   ```bash
   python app.py
   ```

2. **Access the API documentation**:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

3. **Make API requests**:
   ```bash
   curl -X POST "http://localhost:8000/rate" \
   -H "Content-Type: application/json" \
   -d '{
     "task_type": "task1",
     "question": "Write a letter to your friend about your recent vacation.",
     "response": "Dear John, I hope you are doing well...",
     "model": "chatGPT"
   }'
   ```

## Usage

### Using the GUI

1. **Select AI Model**: Choose between "chatGPT" or "llama3.2"
2. **Select Task Type**: Choose "task1" (Letter Writing) or "task2" (Essay Writing)
3. **Enter Question**: Paste the IELTS writing task question
4. **Enter Response**: Write or paste the student's response
5. **Submit**: Click "Submit for Evaluation" to get detailed feedback

### API Endpoints

#### POST `/rate`

Evaluates an IELTS writing submission.

**Request Body**:
```json
{
  "task_type": "task1",
  "question": "Your writing task question here",
  "response": "Student's response here",
  "model": "chatGPT"
}
```

**Response**:
```json
{
  "rating": {
    "task_achievement": {
      "score": 7.0,
      "feedback": "The response adequately addresses the task..."
    },
    "coherence_cohesion": {
      "score": 6.5,
      "feedback": "The response shows good organization..."
    },
    "lexical_resource": {
      "score": 7.0,
      "feedback": "Good range of vocabulary used..."
    },
    "grammatical_range": {
      "score": 6.0,
      "feedback": "Some grammatical errors present..."
    },
    "overall_score": 6.5,
    "overall_feedback": "Overall, this is a competent response..."
  }
}
```

## Scoring Criteria

The application evaluates writing tasks based on official IELTS criteria:

- **Task Achievement** (Task 1) / **Task Response** (Task 2): How well the response addresses the task requirements
- **Coherence & Cohesion**: Logical organization, paragraphing, and linking
- **Lexical Resource**: Vocabulary range, accuracy, and appropriateness
- **Grammatical Range & Accuracy**: Sentence variety and grammatical correctness
- **Overall Score**: Final band score (0-9 scale, 0.5 increments)

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required for ChatGPT model)
- `OLLAMA_API_URL`: Ollama API URL (default: `http://localhost:11434/api/`)

### Model Configuration

- **ChatGPT**: Uses GPT-4 model with temperature 0.2 for consistent scoring
- **Llama 3.2**: Uses local Ollama installation

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY environment variable is not set"**
   - Set your OpenAI API key as an environment variable
   - Verify the key is correctly set: `echo $OPENAI_API_KEY`

2. **"Connection refused" when using Llama 3.2**
   - Ensure Ollama is running: `ollama serve`
   - Check if Llama 3.2 model is installed: `ollama list`

3. **"Failed to get feedback" in GUI**
   - Ensure the FastAPI backend is running on port 8000
   - Check the terminal for error messages

4. **Import errors**
   - Install missing dependencies: `pip install -r requirements.txt`
   - For Ollama: `pip install ollama`
   - For OpenAI: `pip install openai`

### Debug Mode

Enable debug mode to see detailed error information:
```bash
curl -X POST "http://localhost:8000/rate?debug_mode=true" \
# ... rest of request
```

## Development

### Project Structure

```
├── app.py                    # FastAPI backend server
├── ielts_tkinter_app.py     # Tkinter GUI application
├── requirements.txt         # Python dependencies
└── README.md               # This file
---

**Note**: This application is designed for learning purposes and your feedback may vary with the prompt
