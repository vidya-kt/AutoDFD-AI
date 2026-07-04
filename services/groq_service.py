import os
import requests

from dotenv import load_dotenv

from utils.helpers import (
    clean_mermaid_response,
    validate_mermaid_syntax
)

load_dotenv()

# API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq API URL
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def generate_dfd(user_description):

    level = classify_description(user_description)

    #print("Detected Level:", level)


    if level == "INVALID":

        raise Exception(
            "Please enter a meaningful system description."
        )

    if level == "AMBIGUOUS":

        raise Exception(
            "Description is too vague. Please describe the workflow and actors."
        )

    # Dynamic Layout Selection
    layout = "graph TD"

    # Use Left-to-Right for complex prompts
    if len(user_description.split()) > 30:
        layout = "graph LR"
    else:
        layout = "graph TD"


    BASE_RULES = f"""
CRITICAL OUTPUT RULES
- Output ONLY Mermaid.js code.
- Do NOT provide explanations.
- Do NOT provide notes.
- Do NOT provide descriptions.
- Do NOT provide markdown.
- Do NOT provide bullet points.
- Do NOT provide comments.
- The response must start with:
    graph TD
or
    graph LR
- The response must end with the last Mermaid connection.
- Any text outside Mermaid syntax is INVALID.

CRITICAL:

Every node must have:
Identifier[Label]
or
Identifier((Label))
or
Identifier[(Label)]

Examples:

P[Patient]
D[Doctor]
DB[(Hospital Database)]
RP((Registration Process))

Never use:

Patient[E]
Registration Process[P]
Hospital Database[DB]

1. Start with {layout}
2. Generate ONLY valid Mermaid.js syntax.
3. Generate clean, readable, academic-style Data Flow Diagrams (DFDs).
4. Use simple and balanced layouts.
5. Use only one-directional arrows (A --> B).
6. Avoid reverse arrows, bidirectional arrows, loops, and duplicate connections.
7. Avoid unnecessary nodes, processes, and arrows.
8. Keep related components grouped logically.
9. Prioritize readability over completeness.

MERMAID SYNTAX RULES

10. Define every node before using it in a connection.
11. Every connection must use previously defined node identifiers.
12. All node identifiers must be unique.
13. Never place raw text or floating labels outside connections.
14. Node definitions and connections must be on separate lines.
15. Define all nodes first, then generate connections.

Correct:

D[Doctor]
RP((Record Management Process))

D --> RP

Wrong:

Doctor[D --> RP
Patient[P --> Registration

NODE SHAPES (MANDATORY)

16. External Entities:

    P[Patient]
    D[Doctor]
    A[Administrator]

Examples:

    Customer[Customer]
    Doctor[Doctor]
    Administrator[Administrator]

17. Processes:

    RP((Registration Process))
    VP((Validation Process))
    BP((Billing Process))

Examples:

    RP((Registration Process))
    VP((Validation Process))
    BP((Billing Process))

Invalid:

    RP[Registration Process]
    RP(Registration Process)

18. Databases:

    DB[(Database)]

Examples:

    DB[(Hospital Database)]
    DB[(Order Database)]

Invalid:

    DB[Hospital Database]
    [(Hospital Database)]

DFD STRUCTURE RULES

19. External entities must interact through processes.
20. External entities must NEVER connect directly to:
        - Other external entities
        - Databases

21. Databases should connect only to processes.
22. Direct entity-to-database connections should be avoided.
23. Use databases only when explicitly mentioned or clearly implied.
24. Use one representative flow between a process and a database.
25. Avoid showing separate read and write arrows for the same relationship.

WORKFLOW RULES

26. Separate independent workflows into distinct branches.
27. Do not merge unrelated workflows unless an explicit dependency exists.

Correct:

Patient --> Registration Process --> Validation Process

Billing Department --> Billing Process --> Database

Administrator --> Report Generation Process --> Database

Wrong:

Notification Process --> Patient --> Registration Process

28. If a user action is described, represent it using a process when appropriate.
29. Preserve system names mentioned in the description whenever appropriate.
30. Do not invent actors, databases, or business processes that are not mentioned or clearly implied.
31. Prefer process-centric DFD structures.
32. Keep databases primarily as storage targets.
33. Any diagram violating these rules is invalid.
34. Node identifiers must not contain spaces.

Correct:

RP((Registration Process))
DB[(Hospital Database)]
D[Doctor]

Wrong:

Registration Process[P]
Hospital Database[DB]
Billing Department[E]
"""

    if level == "LEVEL_0":
        LEVEL_RULES = """
Generate a TRUE Context Diagram (Level-0 DFD).

A Context Diagram represents the ENTIRE SYSTEM as ONE process.

STRICT RULES:

1. Use EXACTLY one central process.
2. The central process must represent the complete system.
3. Show ONLY external entities interacting with the system.
4. Do NOT create internal modules.
5. Do NOT create subprocesses.
6. Do NOT create databases.
7. Do NOT create records, schedules, reports, notifications, validations, registrations, payments, billing modules, management modules, or any internal component.
8. Maximum 4 external entities.
9. Maximum 5 total nodes.
10. Use only simple arrows.
11. Use syntax A --> B only.
12. All external entities must connect directly to the central process.
13. Every arrow must start or end at the central process.
14. External entities must NEVER connect to each other.
15. The diagram must contain:
    - External Entities
    - One Central Process
    - Data Flows
16. If multiple processes are identified, merge them into the single system process.
17. The central system process must be the only process node.
18. If activities such as registration, validation, scheduling, payments, notifications, reports, or records are mentioned, treat them as internal behavior of the system and DO NOT create separate nodes.
19. If more than one process node is created, the answer is incorrect.
20. If a system name is mentioned,
    use that system name as the central process.
21. The central system MUST be represented using circular process notation.
22. External entities MUST send data to the central system process.

Correct:

Patient --> Hospital System
Doctor --> Hospital System
Administrator --> Hospital System

Wrong:

Hospital System --> Patient
Hospital System --> Doctor
Hospital System --> Administrator

Correct:

S((Hospital System))
S((Ecommerce System))

Wrong:

S[Hospital System]
S[Hospital Database]

Example:

Patients use a hospital system.

Correct:

Hospital System

Wrong:

Admission Process
Treatment Process
Management Process

OUTPUT STRUCTURE EXAMPLE:

graph TD

A[Customer]
B[Admin]

C((Ecommerce System))

A --> C
B --> C

IMPORTANT:
If the description mentions appointments, records, payments, reports, notifications, schedules, validation, registration, etc., treat them as activities of the central system and DO NOT create separate nodes for them.

Output ONLY Mermaid syntax.
"""

    elif level == "LEVEL_1":
        LEVEL_RULES = """
Generate a Level-1 DFD.

A Level-1 DFD shows the major business processes of the system.

Additional Rules:

1. Decompose the system into major modules only.
2. Show key business processes.
3. Maximum 8 nodes.
4. Avoid excessive decomposition.
5. Show databases only when explicitly mentioned.
6. Use 2 to 5 major processes.
7. External entities must interact with processes.
8. External entities must NEVER connect directly to databases.
9. Databases must connect only to processes.
10. Do not model information, records, reports, or payments as databases unless an actual database is mentioned.
11. If the description explicitly mentions a system, create a central process representing that system.
12. External entities must NEVER connect directly to other external entities.
13. Do not infer new actors.
14. Do not infer new databases.
15. Do not infer new processes unless clearly implied.
16. Keep the flow simple and academic.
17. Avoid unnecessary arrows.
18. Use one central business flow.

Example Input:

Patient registers through hospital system.
Doctor updates patient records.
Billing department processes payments and stores data in hospital database.

Expected Output:

graph TD

P[Patient]
H((Hospital System))
D[Doctor]
B[Billing Department]
DB[(Hospital Database)]

P -->|Registration| H
H -->|Patient Data| DB
D -->|Update Records| DB
B -->|Payment Data| DB

STRICT MERMAID RULES:

1. Use ONLY:
   A --> B

2. Labels:
   A -->|Label| B

3. Never generate:
   A -> B

4. Never generate:
   A ==> B

5. Never generate:
   A -->|Label|> B

DATABASE RULES:

1. Every database must have an identifier.

Correct:

DB[(Hospital Database)]

Wrong:

[(Hospital Database)]

2. Define databases before connections.

3. Never create anonymous databases.
"""

    elif level == "LEVEL_2":
        LEVEL_RULES = """
Generate a Level-2 DFD.

A Level-2 DFD represents a detailed decomposition of system functionality into multiple interconnected subprocesses.

LEVEL-2 STRUCTURE RULES:

1. Generate detailed process decomposition.
2. Show major subprocesses explicitly mentioned in the description.
3. Maximum 12 nodes.
4. Maintain readability and academic DFD conventions.
5. Every major action described in the workflow should be represented as a process node.
6. External entities must interact with processes, not directly with databases.
7. Databases should primarily connect to processes.
8. Avoid direct external entity to database connections.
9. If a role performs an action, include that role as an external entity and create a corresponding process when appropriate.
10. Avoid unnecessary process-to-process loops.
11. Prefer one-directional data flow.
12. Notification processes should send outputs to external entities.
13. Reporting processes should read data from databases and provide reports to administrators.
14. Record management activities should be represented as processes.
15. Result uploads should be represented as processes.
16. Billing activities should be represented as billing processes.
17. Validation activities should be represented as validation processes.
18. Registration and validation must be represented as separate processes when both are described.
19. Doctor activities should be represented through a Record Management Process.
20. Laboratory activities should be represented through a Result Upload Process.
21. Administrator reporting activities should be represented through a Report Generation Process.

Examples:

Patient registers
→ Registration Process

System validates details
→ Validation Process

Doctor retrieves and updates records
→ Record Management Process

Laboratory uploads test results
→ Result Upload Process

Billing department generates invoices and processes payments
→ Billing Process

Administrator generates reports
→ Report Generation Process

Notification service sends confirmations
→ Notification Process

EXPECTED STRUCTURE EXAMPLE:

Patient --> Registration Process
Registration Process --> Validation Process
Validation Process --> Hospital Database

Doctor --> Record Management Process
Record Management Process --> Hospital Database

Laboratory --> Result Upload Process
Result Upload Process --> Hospital Database

Billing Department --> Billing Process
Billing Process --> Hospital Database

Billing Process --> Notification Process
Notification Process --> Patient

Administrator --> Report Generation Process
Report Generation Process --> Hospital Database

STRICT MERMAID RULES:

1. Use ONLY:
   A --> B

2. Labels:
   A -->|Label| B

3. Never generate:
   A -> B

4. Never generate:
   A ==> B

5. Never generate:
   A -->|Label|> B

DATABASE RULES:

DB[(Database)]

NODE SHAPES:

External Entity:
E[Entity]

Process:
P((Process))

Database:
DB[(Database)]
"""

    else:
        raise Exception(
            f"Unknown level returned by classifier: {level}"
        )

    # Dynamic Prompt
    dynamic_prompt = f"""
You are an expert software system analyst.

Generate ONLY valid Mermaid.js Data Flow Diagram syntax.

{BASE_RULES}

{LEVEL_RULES}
"""
    #print("Prompt Used:")
    
    #print(dynamic_prompt)

    # Headers
    headers = {

        "Authorization":
            f"Bearer {GROQ_API_KEY}",

        "Content-Type":
            "application/json"
    }

    # API Payload
    payload = {

        "model": "llama-3.1-8b-instant",

        "messages": [

            {
                "role": "system",
                "content": dynamic_prompt
            },

            {
                "role": "user",
                "content": user_description
            }
        ],

        "temperature": 0,

        "max_tokens": 1024
    }

    # API Request
    response = requests.post(

        GROQ_URL,

        headers=headers,

        json=payload
    )

    # Error Handling
    if response.status_code != 200:

        raise Exception(
            f"Groq API request failed: {response.text}"
        )

    # Response JSON
    data = response.json()

    # Extract AI Output
    raw_output = \
        data["choices"][0]["message"]["content"]

    # Clean Mermaid Response
    cleaned_output = \
        clean_mermaid_response(raw_output)
    
    #print(cleaned_output)

    print("Detected Level:", level)

    # Validate Mermaid Syntax
    if not validate_mermaid_syntax(cleaned_output):

        raise Exception(
            "Invalid Mermaid syntax generated"
        )

    return {
        "mermaid": cleaned_output,
        "level": level
    }

def classify_description(user_description):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Analyze the following user description.

CRITICAL:

Your response must contain EXACTLY ONE WORD.

Valid responses:

LEVEL_0
LEVEL_1
LEVEL_2
AMBIGUOUS
INVALID

Do NOT provide explanations.
Do NOT provide reasoning.
Do NOT provide additional text.

Definitions:

INVALID:
- Random text
- Numbers only
- Meaningless input

AMBIGUOUS:
- System name only
- Insufficient workflow details

LEVEL_0:
- Statements such as:
  "Users use the system"
  "Doctors access information"
  "Administrators monitor operations"
  "Customers interact with the system"

  MUST remain LEVEL_0 if no internal workflow steps are described.

- Accessing information alone does NOT imply a database.

- Monitoring operations alone does NOT imply a monitoring process.

- Never infer internal modules from generic actor actions.

LEVEL_0 Example:

Patients use a hospital system.
Doctors access patient information.
Administrators monitor hospital operations.

Output:
LEVEL_0

LEVEL_1:
- Major business processes are described.
- Limited decomposition.
- May contain databases.
- Does not contain detailed workflow steps.

LEVEL_1 Example:

Patient registers through hospital system.
Doctor updates patient records.
Billing department processes payments and stores data in hospital database.

Output:
LEVEL_1

LEVEL_2:

LEVEL_2:
- Detailed workflow with sequential or dependent process steps.
- Multiple subprocesses are described.
- Validation, notifications, approvals, reports, etc.
- Data flows through multiple stages.

LEVEL_2 Example:

Patient registers through the hospital system.
System validates patient details.
Doctor updates records.
Billing generates invoice.
Notification service sends confirmation.

Output:
LEVEL_2

Description:
{user_description}
"""

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    response = requests.post(
        GROQ_URL,
        headers=headers,
        json=payload
    )

    result = response.json()

    response_text = (
        result["choices"][0]["message"]["content"]
        .strip()
        .upper()
    )

    if "LEVEL_0" in response_text:
        return "LEVEL_0"

    if "LEVEL_1" in response_text:
        return "LEVEL_1"

    if "LEVEL_2" in response_text:
        return "LEVEL_2"

    if "AMBIGUOUS" in response_text:
        return "AMBIGUOUS"

    if "INVALID" in response_text:
        return "INVALID"

    return "AMBIGUOUS"