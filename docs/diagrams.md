# Agentic AI Workflow Diagrams

These diagrams are designed for README documentation and LinkedIn posts. Internal agent handoffs use TOON (Token-Oriented Object Notation) to reduce prompt tokens while preserving traceability.

## Main Product Workflow

```mermaid
flowchart TD
    A["User Request"] --> B["Request Structuring Agent"]
    B --> C["Task Decomposition Agent"]
    C --> D["Prerequisite Analyzer"]
    D --> E["LangGraph Orchestrator"]
    E --> F["Search Agent"]
    E --> G["Reasoning Agent"]
    E --> H["Comparison Agent"]
    E --> I["Extraction Agent"]
    E --> J["Writing Agent"]
    F --> K["TOON Agent Handoff"]
    G --> K
    H --> K
    I --> K
    J --> K
    K --> L["Verifier Agent"]
    L --> M{"Complete and Consistent?"}
    M -->|No| E
    M -->|Yes| N["Final Response Agent"]
    N --> O["User Output + Execution Trace"]
```

## LangGraph State Graph

```mermaid
stateDiagram-v2
    [*] --> StructureRequest
    StructureRequest --> DecomposeTasks
    DecomposeTasks --> AnalyzePrerequisites
    AnalyzePrerequisites --> RouteTasks
    RouteTasks --> ExecuteSearch : needs research
    RouteTasks --> ExecuteReasoning : needs reasoning
    RouteTasks --> ExecuteComparison : needs comparison
    RouteTasks --> ExecuteExtraction : needs extraction
    ExecuteSearch --> VerifyOutput
    ExecuteReasoning --> VerifyOutput
    ExecuteComparison --> VerifyOutput
    ExecuteExtraction --> VerifyOutput
    VerifyOutput --> RouteTasks : missing or weak output
    VerifyOutput --> FinalResponse : output accepted
    FinalResponse --> [*]
```

## Agent Responsibility Map

```mermaid
flowchart LR
    A["Request Structuring Agent"] --> A1["Turns messy request into structured intent"]
    B["Task Decomposition Agent"] --> B1["Splits request into smaller tasks"]
    J["TOON Handoff Encoder"] --> J1["Compresses agent outputs before the next agent"]
    C["Prerequisite Analyzer"] --> C1["Finds task order and dependencies"]
    D["Orchestrator"] --> D1["Chooses which agent runs next"]
    E["Search Agent"] --> E1["Finds relevant external information"]
    F["Reasoning Agent"] --> F1["Analyzes constraints and tradeoffs"]
    G["Comparison Agent"] --> G1["Compares options against criteria"]
    H["Verifier Agent"] --> H1["Checks completeness and consistency"]
    I["Final Response Agent"] --> I1["Creates polished user answer"]
```


## TOON Agent Handoff Flow

```mermaid
flowchart LR
    A["Agent 1 Output"] --> B["TOON Encoder"]
    B --> C["Compact TOON Payload"]
    C --> D["Next Agent Prompt"]
    D --> E["Agent 2 Uses Prior Evidence"]
    E --> F["Lower-token Internal Context"]
```

## TOON Payload Shape

```mermaid
flowchart TD
    A["Agent Output"] --> B["task_id"]
    A --> C["agent"]
    A --> D["summary"]
    A --> E["sources as compact rows"]
    B --> F["TOON Handoff"]
    C --> F
    D --> F
    E --> F
    F --> G["Next Agent"]
```

## Tech Architecture

```mermaid
flowchart LR
    A["Next.js Frontend on Vercel"] --> B["FastAPI Backend on Render"]
    B --> C["Clerk Auth Verification"]
    B --> D["Supabase Postgres"]
    B --> E["LangGraph Orchestrator"]
    E --> F["LangChain Model and Tool Layer"]
    F --> G["Groq Models"]
    F --> H["Google AI Studio / Gemini"]
    F --> I["Controlled Web Search"]
    E --> K["TOON Internal Handoffs"]
    K --> F
    D --> J["Runs, Traces, Outputs, Usage Logs"]
```

## Example Flow: Compare AI Workflow Tools

```mermaid
flowchart TD
    A["User: Compare two AI workflow tools"] --> B["Structure Request"]
    B --> C["Encode Structured Intent as TOON"]
    C --> D["Analyze Prerequisites"]
    D --> E["Budget Filter Must Run Before Recommendation"]
    E --> F["Search Agent Finds Source Evidence"]
    F --> G["Search Output Encoded as TOON"]
    G --> H["Comparison Agent Reads TOON Handoff"]
    H --> I["Verifier Checks Completeness"]
    I --> Q{"Any valid result?"}
    Q -->|No| R["Return honest limitation and alternatives"]
    Q -->|Yes| S["Final Suggestions With Sources"]
```
