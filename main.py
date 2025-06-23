import pandas as pd
import json
from yaspin import yaspin
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM


# 1. Load model from Ollama
llm = OllamaLLM(model="gemma3:1b", temperature=0) # temperature=0 for consistent output

# 2. Prompt template
template = """
You are a support ticket analyst. Analyze the ticket and respond ONLY with a JSON object, no explanation.

Instructions:

1. **category**: One of:
   - Technical issues
   - Hardware issues
   - Data recovery

2. **tags**: Extract 1 to 3 key tags.

3. **priority**: Choose based on real urgency:
   - High: Only if user mentions deadline, system crash, or urgent need.
   - Medium: If it's disruptive but not urgent.
   - Low: If it's a minor issue, information request, or not time-sensitive.

4. **eta**: Must depend on the priority:
   - High → Immediate
   - Medium → 24 hours
   - Low → 2-3 business days

5. **response**: Provide a clear, calm instruction to the user in 1 sentence.

Output the following data as JSON only, but do not include any code block markers:

{{
  "category": "your_category_prediction",
  "tags": ["tag1", "tag2"],
  "priority": "your_priority_prediction",
  "eta": "your_eta_prediction",
  "response": "your_brief_instruction_to_user"
}}


--- Examples ---

Example 1:
Ticket: "My laptop won't turn on and I have a presentation in 2 hours."
Output:
{{
  "category": "Hardware issues",
  "tags": ["laptop", "won't turn on", "presentation"],
  "priority": "High"
}}

Example 2:
Ticket: "Having trouble installing the software. Need to get it working today."
Output:
{{
  "category": "Technical issues",
  "tags": ["installation", "software", "troubleshooting"],
  "priority": "Medium"
}}

Example 3:
Ticket: "Files from a previous backup seem corrupted but I have time to reupload."
Output:
{{
  "category": "Data recovery",
  "tags": ["backup", "corrupted files"],
  "priority": "Low"
}}

Example 4:
Ticket: "My email isn't syncing, but I can still use webmail for now."
Output:
{{
  "category": "Technical issues",
  "tags": ["email", "sync issue", "webmail"],
  "priority": "Low"
}}

Example 5:
Ticket: "My computer fan is making loud noises and I'm worried it may fail soon."
Output:
{{
  "category": "Hardware issues",
  "tags": ["fan noise", "possible failure", "hardware"],
  "priority": "Medium"
}}

Analyze the following ticket and respond:
Ticket: "{ticket}"
Output:
"""


prompt = PromptTemplate.from_template(template)

# 3. Chain
chain = prompt | llm

# 4. Example data (replace with your own)
# tickets = [
#     "Urgent help! My laptop won't turn on and I have a deadline today.",
#     "Lost all my project files after a system crash. Need recovery.",
#     "Just need assistance updating my app. Nothing critical."
# ]

tickets = [
    "Urgent help! My laptop won't turn on and I have a deadline today.",
]

# 5. Classify + clean output
def classify_ticket(text: str) -> dict:
    with yaspin(text="Classifying...", color="cyan") as spinner:
        result = chain.invoke({"ticket": text})
        spinner.ok("✅")

    # Remove ```json code blockers, if our output has it
    result = result.replace("```json", "").replace("```", "").strip()

    if not result.strip().startswith("{"):
        result = "{" + result
    if not result.strip().endswith("}"):
        result = result + "}"

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON response:", result)
        return {}

 

# 6. Run on all tickets
df = pd.DataFrame(tickets, columns=["ticket"])
df["result"] = df["ticket"].apply(classify_ticket)

# 7. Expand structured fields
df["category"] = df["result"].apply(lambda x: x.get("category", ""))
df["tags"] = df["result"].apply(lambda x: x.get("tags", []))
df["priority"] = df["result"].apply(lambda x: x.get("priority", ""))
df["eta"] = df["result"].apply(lambda x: x.get("eta", ""))
df["response"] = df["result"].apply(lambda x: x.get("response", ""))

# 8. Show result
print(df[["ticket", "category", "tags", "priority", "eta", "response"]])

