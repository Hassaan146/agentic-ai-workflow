# Agentic AI Workflow Diagrams

<style>
@page {
  size: A4 landscape;
  margin: 12mm;
}

body {
  max-width: 100%;
  background: #070B10;
  color: #F9F9F9;
}

h1, h2, p {
  color: #F9F9F9;
}

h2 {
  break-before: page;
  page-break-before: always;
  margin-top: 0;
}

h2:first-of-type {
  break-before: auto;
  page-break-before: auto;
}

pre, svg, .mermaid {
  break-inside: avoid;
  page-break-inside: avoid;
  max-width: 100% !important;
  max-height: 165mm !important;
}

.mermaid svg {
  max-width: 100% !important;
  height: auto !important;
}
</style>

These diagrams are designed for README documentation and LinkedIn PDF carousel posts.

Internal agent handoffs use GCF (Graph Compact Format) to reduce prompt tokens while preserving traceability.

## Main Product Workflow

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["User prompt"] --> B["Structure request"]
    B --> C["Plan tasks"]
    C --> D["Check prerequisites"]
    D --> E["Route agents"]
    E --> F["Run specialist agents"]
    F --> G["Encode GCF handoff"]
    G --> H["Verify result"]
    H --> I{"Accepted?"}
    I -->|No| E
    I -->|Yes| J["Final response"]
    J --> K["Format for user"]
    K --> L["Output + trace"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;
    classDef decision fill:#F9F9F9,stroke:#D99A2B,color:#228B22,stroke-width:2px;

    class A,L primary;
    class B,C,D,E,F,H,J,K dark;
    class G gcf;
    class I decision;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## Agent Routing Layer

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["LangGraph Orchestrator"] --> B["Search Agent"]
    A --> C["Reasoning Agent"]
    A --> D["Comparison Agent"]
    A --> E["Extraction Agent"]
    A --> F["Writing Agent"]
    B --> G["GCF handoff"]
    C --> G
    D --> G
    E --> G
    F --> G
    G --> H["Verifier"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;

    class A,H primary;
    class B,C,D,E,F dark;
    class G gcf;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## LangGraph State Graph

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","lineColor":"#D99A2B","textColor":"#F9F9F9","noteBkgColor":"#F9F9F9","noteTextColor":"#101418"}}}%%
stateDiagram-v2
    [*] --> StructureRequest
    StructureRequest --> DecomposeTasks
    DecomposeTasks --> AnalyzePrerequisites
    AnalyzePrerequisites --> RouteTasks
    RouteTasks --> ExecuteAgents
    ExecuteAgents --> EncodeGcfHandoff
    EncodeGcfHandoff --> VerifyOutput
    VerifyOutput --> RouteTasks : improve
    VerifyOutput --> FinalResponse : accepted
    FinalResponse --> FormatForUser
    FormatForUser --> [*]
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## Agent Responsibility Map

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Structuring"] --> A1["Convert prompt into intent"]
    B["Planning"] --> B1["Split into tasks"]
    C["Prerequisites"] --> C1["Order dependencies"]
    D["Orchestrator"] --> D1["Choose next agent"]
    E["Specialists"] --> E1["Search, reason, compare, extract, write"]
    F["GCF Encoder"] --> F1["Compress handoffs"]
    G["Verifier"] --> G1["Check completeness"]
    H["Formatter"] --> H1["Match user response style"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;

    class A,B,C,D,E,G,H primary;
    class A1,B1,C1,D1,E1,G1,H1 dark;
    class F gcf;
    class F1 dark;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## GCF Agent Handoff Flow

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart LR
    A["Agent output"] --> B["GCF encoder"]
    B --> C["Compact payload"]
    C --> D["Next agent prompt"]
    D --> E["Better context"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;

    class A,E primary;
    class B,C gcf;
    class D dark;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## GCF Payload Shape

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Agent output"] --> B["task_id"]
    A --> C["agent"]
    A --> D["summary"]
    A --> E["sources"]
    B --> F["GCF handoff"]
    C --> F
    D --> F
    E --> F
    F --> G["Next agent"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;

    class A,G primary;
    class B,C,D,E dark;
    class F gcf;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## User-Preferred Response Layer

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Verified result"] --> B["Final GCF handoff"]
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

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;
    classDef decision fill:#F9F9F9,stroke:#D99A2B,color:#228B22,stroke-width:2px;

    class A,K primary;
    class B gcf;
    class C,D,F,G,H,I,J dark;
    class E decision;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## Response Quality Loop

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart LR
    A["User feedback"] --> B["Preference research"]
    B --> C["Format library"]
    C --> D["Formatter agent"]
    D --> E["Better responses"]
    E --> A

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;

    class A,E primary;
    class B,C,D dark;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## Tech Architecture

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Next.js frontend"] --> B["FastAPI backend"]
    B --> C["Auth"]
    B --> D["Supabase"]
    B --> E["LangGraph"]
    E --> F["LangChain tools"]
    F --> G["Groq models"]
    F --> H["Gemini optional"]
    F --> I["Web search"]
    E --> J["GCF handoffs"]
    E --> K["Response formatter"]
    D --> L["Runs + traces"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;

    class A,B,L primary;
    class C,D,E,F,G,H,I,K dark;
    class J gcf;
```

<div style="break-after: page; page-break-after: always;"></div>

<!-- pagebreak -->

## Example Flow

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":18,"rankSpacing":24,"curve":"linear"},"themeVariables":{"fontSize":"13px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Custom user prompt"] --> B["Structure intent"]
    B --> C["Encode intent as GCF"]
    C --> D["Plan dependencies"]
    D --> E["Find source evidence"]
    E --> F["GCF evidence handoff"]
    F --> G["Compare or reason"]
    G --> H["Verify"]
    H --> I{"Ready?"}
    I -->|No| D
    I -->|Yes| J["Final GCF handoff"]
    J --> K["User format"]
    K --> L["Final answer"]

    classDef primary fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:2px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:1.5px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:2px;
    classDef decision fill:#F9F9F9,stroke:#D99A2B,color:#228B22,stroke-width:2px;

    class A,L primary;
    class B,D,E,G,H,K dark;
    class C,F,J gcf;
    class I decision;
```