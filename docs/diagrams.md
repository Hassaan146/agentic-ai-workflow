# Agentic AI Workflow Diagrams

These diagrams are designed for README documentation and LinkedIn posts. Internal agent handoffs use TOON (Token-Oriented Object Notation) to reduce prompt tokens while preserving traceability.

## Main Product Workflow

```mermaid
flowchart TD
    A["User Request"] --> B["Request Structuring Agent"]
    subgraph S1["Structured Planning Layer"]
        direction TD
        B --> C["Task Decomposition Agent"]
        C --> D["Prerequisite Analyzer"]
        D --> E["LangGraph Orchestrator"]
    end
    subgraph S2["Specialized Agent Layer"]
        direction LR
        E --> F["Search Agent"]
        E --> G["Reasoning Agent"]
        E --> H["Comparison Agent"]
        E --> I["Extraction Agent"]
        E --> J["Writing Agent"]
    end
    subgraph S3["TOON Handoff Layer"]
        direction TD
        F --> K["TOON Agent Handoff"]
        G --> K
        H --> K
        I --> K
        J --> K
    end
    K --> L["Verifier Agent"]
    L --> M{"Complete and Consistent?"}
    M -->|No| E
    M -->|Yes| N["Final Response Agent"]
    N --> P["Response Preference Formatter"]
    P --> O["User Output + Execution Trace"]

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef soft fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    classDef decision fill:#ffffff,stroke:#1d4ed8,color:#0f172a,stroke-width:2px;
    classDef group fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:1.5px,stroke-dasharray: 6 4;
    class A,O primary;
    class B,C,D,E,F,G,H,I,J,L,N,P soft;
    class K toon;
    class M decision;
    class S1,S2,S3 group;
```

## LangGraph State Graph

```mermaid
stateDiagram-v2
    [*] --> StructureRequest
    state "Planning Layer" as Planning {
        StructureRequest --> DecomposeTasks
        DecomposeTasks --> AnalyzePrerequisites
        AnalyzePrerequisites --> RouteTasks
    }
    state "Agent Execution Layer" as Agents {
        RouteTasks --> ExecuteSearch : needs research
        RouteTasks --> ExecuteReasoning : needs reasoning
        RouteTasks --> ExecuteComparison : needs comparison
        RouteTasks --> ExecuteExtraction : needs extraction
    }
    state "Verification and Formatting Layer" as Response {
        ExecuteSearch --> VerifyOutput
        ExecuteReasoning --> VerifyOutput
        ExecuteComparison --> VerifyOutput
        ExecuteExtraction --> VerifyOutput
    }
    VerifyOutput --> RouteTasks : missing or weak output
    VerifyOutput --> FinalResponse : output accepted
    FinalResponse --> FormatForUser
    FormatForUser --> [*]

    classDef royal fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef light fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    classDef dotted fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:1.5px,stroke-dasharray: 6 4;
    class StructureRequest,DecomposeTasks,AnalyzePrerequisites,RouteTasks,ExecuteSearch,ExecuteReasoning,ExecuteComparison,ExecuteExtraction,VerifyOutput,FinalResponse,FormatForUser light;
    class Planning,Agents,Response dotted;
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
    K["Response Preference Formatter"] --> K1["Shapes answer into the user's desired format"]

    classDef agent fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef responsibility fill:#ffffff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    class A,B,C,D,E,F,G,H,I,J,K agent;
    class A1,B1,C1,D1,E1,F1,G1,H1,I1,J1,K1 responsibility;
```


## TOON Agent Handoff Flow

```mermaid
flowchart LR
    A["Agent 1 Output"] --> B["TOON Encoder"]
    B --> C["Compact TOON Payload"]
    C --> D["Next Agent Prompt"]
    D --> E["Agent 2 Uses Prior Evidence"]
    E --> F["Lower-token Internal Context"]

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    class A,D,E,F primary;
    class B,C toon;
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

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef field fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    class A,G primary;
    class B,C,D,E field;
    class F toon;
```

## User-Preferred Response Layer

```mermaid
flowchart TD
    A["Verified Agent Result"] --> B["Final TOON Handoff"]
    C["User Response Preference"] --> D["Response Formatter"]
    B --> D
    D --> E{"Desired Output Type"}
    E -->|Brief| F["Concise Executive Summary"]
    E -->|Deep Dive| G["Detailed Report"]
    E -->|Action| H["Checklist or Plan"]
    E -->|Social| I["LinkedIn-ready Post"]
    E -->|Data| J["Table or Structured Output"]
    F --> K["Valid, Useful Final Answer"]
    G --> K
    H --> K
    I --> K
    J --> K

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    classDef format fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    class A,C,K primary;
    class B toon;
    class D,E,F,G,H,I,J format;
```

## Response Quality Loop

```mermaid
flowchart LR
    A["User Feedback"] --> B["Preference Research"]
    B --> C["Response Format Library"]
    C --> D["Formatter Agent"]
    D --> E["Better User-fit Responses"]
    E --> A

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef soft fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    class A,E primary;
    class B,C,D soft;
```

## Tech Architecture

```mermaid
flowchart LR
    subgraph Client["Client Layer"]
        A["Next.js Frontend on Vercel"]
    end
    subgraph Backend["Backend Layer"]
        B["FastAPI Backend on Render"]
        C["Clerk Auth Verification"]
        D["Supabase Postgres"]
        E["LangGraph Orchestrator"]
    end
    subgraph Intelligence["Model and Tool Layer"]
        F["LangChain Model and Tool Layer"]
        G["Groq Models"]
        H["Google AI Studio / Gemini"]
        I["Controlled Web Search"]
        K["TOON Internal Handoffs"]
        L["Response Preference Formatter"]
    end
    A --> B
    B --> C
    B --> D
    B --> E
    E --> F
    F --> G
    F --> H
    F --> I
    E --> K
    K --> F
    E --> L
    D --> J["Runs, Traces, Outputs, Usage Logs"]

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef soft fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    classDef group fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:1.5px,stroke-dasharray: 6 4;
    class A,B,E primary;
    class C,D,F,G,H,I,J,L soft;
    class K toon;
    class Client,Backend,Intelligence group;
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
    Q -->|Yes| S["Final TOON Handoff"]
    S --> T["Format For User Preference"]
    T --> U["Final Suggestions With Sources"]

    classDef primary fill:#1d4ed8,stroke:#0f2f8f,color:#ffffff,stroke-width:2px;
    classDef soft fill:#eff6ff,stroke:#1d4ed8,color:#0f172a,stroke-width:1.5px;
    classDef toon fill:#ffffff,stroke:#1d4ed8,color:#1d4ed8,stroke-width:2px;
    classDef decision fill:#ffffff,stroke:#1d4ed8,color:#0f172a,stroke-width:2px;
    class A,U primary;
    class B,D,E,F,H,I,R,T soft;
    class C,G,S toon;
    class Q decision;
```
