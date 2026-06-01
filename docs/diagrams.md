# Agentic AI Workflow Diagrams

These diagrams are designed for README documentation and LinkedIn PDF carousel posts. Each section is kept to one export page so the rendered PDF does not cut diagrams in half.

Internal agent handoffs use TOON (Token-Oriented Object Notation) to reduce prompt tokens while preserving traceability.

## Main Product Workflow

```mermaid
flowchart TD
    A["User prompt"] --> B["Structure request"]
    B --> C["Plan tasks"]
    C --> D["Check prerequisites"]
    D --> E["Route agents"]
    E --> F["Run specialist agents"]
    F --> G["Encode TOON handoff"]
    G --> H["Verify result"]
    H --> I{"Accepted?"}
    I -->|No| E
    I -->|Yes| J["Final response"]
    J --> K["Format for user"]
    K --> L["Output + trace"]
```

<div style="page-break-after: always;"></div>

## Agent Routing Layer

```mermaid
flowchart TD
    A["LangGraph Orchestrator"] --> B["Search Agent"]
    A --> C["Reasoning Agent"]
    A --> D["Comparison Agent"]
    A --> E["Extraction Agent"]
    A --> F["Writing Agent"]
    B --> G["TOON handoff"]
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H["Verifier"]
```

<div style="page-break-after: always;"></div>

## LangGraph State Graph

```mermaid
stateDiagram-v2
    [*] --> StructureRequest
    StructureRequest --> DecomposeTasks
    DecomposeTasks --> AnalyzePrerequisites
    AnalyzePrerequisites --> RouteTasks
    RouteTasks --> ExecuteAgents
    ExecuteAgents --> EncodeToonHandoff
    EncodeToonHandoff --> VerifyOutput
    VerifyOutput --> RouteTasks : improve
    VerifyOutput --> FinalResponse : accepted
    FinalResponse --> FormatForUser
    FormatForUser --> [*]
```

<div style="page-break-after: always;"></div>

## Agent Responsibility Map

```mermaid
flowchart TD
    A["Structuring"] --> A1["Convert prompt into intent"]
    B["Planning"] --> B1["Split into tasks"]
    C["Prerequisites"] --> C1["Order dependencies"]
    D["Orchestrator"] --> D1["Choose next agent"]
    E["Specialists"] --> E1["Search, reason, compare, extract, write"]
    F["TOON Encoder"] --> F1["Compress handoffs"]
    G["Verifier"] --> G1["Check completeness"]
    H["Formatter"] --> H1["Match user response style"]
```

<div style="page-break-after: always;"></div>

## TOON Agent Handoff Flow

```mermaid
flowchart LR
    A["Agent output"] --> B["TOON encoder"]
    B --> C["Compact payload"]
    C --> D["Next agent prompt"]
    D --> E["Better context"]
```

<div style="page-break-after: always;"></div>

## TOON Payload Shape

```mermaid
flowchart TD
    A["Agent output"] --> B["task_id"]
    A --> C["agent"]
    A --> D["summary"]
    A --> E["sources"]
    B --> F["TOON handoff"]
    C --> F
    D --> F
    E --> F
    F --> G["Next agent"]
```

<div style="page-break-after: always;"></div>

## User-Preferred Response Layer

```mermaid
flowchart TD
    A["Verified result"] --> B["Final TOON handoff"]
    C["User preference"] --> D["Response formatter"]
    B --> D
    D --> E{"Output type"}
    E -->|Brief| F["Summary"]
    E -->|Deep dive| G["Report"]
    E -->|Action| H["Checklist"]
    E -->|Social| I["LinkedIn post"]
    E -->|Data| J["Table"]
    F --> K["Useful final answer"]
    G --> K
    H --> K
    I --> K
    J --> K
```

<div style="page-break-after: always;"></div>

## Response Quality Loop

```mermaid
flowchart LR
    A["User feedback"] --> B["Preference research"]
    B --> C["Format library"]
    C --> D["Formatter agent"]
    D --> E["Better responses"]
    E --> A
```

<div style="page-break-after: always;"></div>

## Tech Architecture

```mermaid
flowchart TD
    A["Next.js frontend"] --> B["FastAPI backend"]
    B --> C["Auth"]
    B --> D["Supabase"]
    B --> E["LangGraph"]
    E --> F["LangChain tools"]
    F --> G["Groq models"]
    F --> H["Gemini optional"]
    F --> I["Web search"]
    E --> J["TOON handoffs"]
    E --> K["Response formatter"]
    D --> L["Runs + traces"]
```

<div style="page-break-after: always;"></div>

## Example Flow

```mermaid
flowchart TD
    A["Custom user prompt"] --> B["Structure intent"]
    B --> C["Encode intent as TOON"]
    C --> D["Plan dependencies"]
    D --> E["Find source evidence"]
    E --> F["TOON evidence handoff"]
    F --> G["Compare or reason"]
    G --> H["Verify"]
    H --> I{"Ready?"}
    I -->|No| D
    I -->|Yes| J["Final TOON handoff"]
    J --> K["User format"]
    K --> L["Final answer"]
```
