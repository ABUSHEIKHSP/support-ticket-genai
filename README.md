# 🧠 Support Ticket Classifier — GenAI Powered Automation

This project automates the classification, tagging, priority assignment, ETA estimation, and response generation for support tickets using a lightweight LLM served locally through [Ollama](https://ollama.com/).

We built this as a **real-world GenAI application**, ideal for customer support teams that need structured triage and faster ticket processing.

---

## 🚀 Features

- Classify tickets into:
  - `Technical issues`
  - `Hardware issues`
  - `Data recovery`
- Extract 1–3 relevant **tags**
- Assign a **priority** (`High`, `Medium`, or `Low`)
- Assign a **response ETA** (`Immediate`, `24 hours`, `2-3 business days`)
- Auto-generate a **brief human-like reply**
- Outputs a fully structured **JSON response**
- All results stored using **pandas DataFrame**

---

## 🧩 Tech Stack

- **LLM**: `llama3:3.2b` pulled from [Ollama](https://ollama.com/library/llama3)
- **LangChain**: for prompt templating and chaining
- **Pandas**: for structured data processing
- **Python 3.10+**
- **No GPU required** (Runs fully on CPU via Ollama)

---

## ⚙️ Setup Instructions

1. **Install Ollama**

   [🔗 Ollama Installation Guide](https://ollama.com/download)

2. **Pull the LLM model**

   ```bash
   ollama pull llama3:3.2b
   
3. **Create a virtual environment and install dependencies**
   
   ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

5. **Run the script**
   
   ```bash
   python main.py

## 📥 Input Example

  ```text
  "My laptop won't start and I have a client meeting in 2 hours. Urgent help needed!"
  ```

## 📤 Output Format

  ```json
  {
  "category": "Hardware issues",
  "tags": ["laptop", "won't start", "urgent"],
  "priority": "High",
  "eta": "Immediate",
  "response": "Please connect your laptop to power, hold the power button for 10 seconds, and if it doesn’t boot, visit our nearest support center for immediate diagnosis."
  }
  ```

## 📂 File Structure

  ```bash
  support-ticket-classifier/
  ├── main.py                # Final implementation
  ├── requirements.txt       # All dependencies
  ├── README.md              # Project guide (this file)
  ```

## 📌 Notes

  - This repo includes only the .py file for clean usage.
  - All logic is built to work on your CPU with a local model using Ollama — no OpenAI key or cloud cost required.

## 🔮 Future Additions

  - ✅ Streamlit or Gradio UI for live input
  - ✅ Larger dataset integration
  - ✅ Custom training & finetuning via LoRA
  - ✅ Dataset export (for future ML pipelines)

## 👨‍💻 Author

Built with ❤️ to demonstrate hands-on GenAI skills using LangChain, Ollama, and lightweight LLMs. Perfect for real-world applications.
    



  
