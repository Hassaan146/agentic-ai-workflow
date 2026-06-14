# Agentic AI Workflow Carousel

<style>
@page {
  size: 2160px 2700px;
  margin: 120px;
}

body {
  background: #070B10;
  color: #F9F9F9;
  font-family: Inter, Arial, sans-serif;
}

h1, h2, p {
  color: #F9F9F9;
}

h1 {
  font-size: 72px;
  line-height: 1.08;
  margin-bottom: 32px;
}

h2 {
  break-before: page;
  page-break-before: always;
  font-size: 58px;
  line-height: 1.12;
  margin-top: 0;
  margin-bottom: 36px;
}

h2:first-of-type {
  break-before: auto;
  page-break-before: auto;
}

p {
  font-size: 34px;
  line-height: 1.45;
}

.slide-note {
  color: #B7C0C8;
  max-width: 1450px;
}

.mermaid {
  break-inside: avoid;
  page-break-inside: avoid;
  margin-top: 40px;
}

.mermaid svg {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
}

.mermaid .node.gcf text,
.mermaid .node.gcf span,
.mermaid .node.gcf .label,
.mermaid .node.gcf foreignObject,
.mermaid .node.gcf foreignObject div,
.mermaid .node.decision text,
.mermaid .node.decision span,
.mermaid .node.decision .label,
.mermaid .node.decision foreignObject,
.mermaid .node.decision foreignObject div {
  fill: #101418 !important;
  color: #101418 !important;
}
</style>

## Agentic AI Workflow Orchestration

<p class="slide-note">
A multi-agent platform where one user prompt becomes a structured workflow, specialist agents execute the right steps, GCF keeps handoffs compact, and the final answer remains traceable.
</p>

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":70,"rankSpacing":95,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"28px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["User Prompt"] --> B["Structured Intent"]
    B --> C["Agent Routing"]
    C --> D["GCF Handoffs"]
    D --> E["Verified Final Output"]

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,E green;
    class B,C dark;
    class D gcf;
```

## Main Product Workflow

<p class="slide-note">
This version avoids crossing arrows by keeping the core workflow vertical and showing revision as a clean side loop.
</p>

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":80,"rankSpacing":90,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"26px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["User prompt"] --> B["Structure request"]
    B --> C["Plan tasks"]
    C --> D["Check prerequisites"]
    D --> E["Route agents"]
    E --> F["Run specialist agents"]
    F --> G["Encode GCF handoff"]
    G --> H["Verify result"]
    H --> I{"Accepted?"}
    I -->|Yes| J["Final response"]
    J --> K["Format for user"]
    K --> L["Output + trace"]
    I -->|Needs improvement| M["Revision route"]
    M --> E

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;
    classDef decision fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,L green;
    class B,C,D,E,F,H,J,K,M dark;
    class G gcf;
    class I decision;
```

## Agent Routing Layer

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":80,"rankSpacing":100,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"26px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
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

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,H green;
    class B,C,D,E,F dark;
    class G gcf;
```

## LangGraph State Graph

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"28px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","lineColor":"#D99A2B","textColor":"#F9F9F9","noteBkgColor":"#F9F9F9","noteTextColor":"#101418"}}}%%
stateDiagram-v2
    [*] --> StructureRequest
    StructureRequest --> DecomposeTasks
    DecomposeTasks --> AnalyzePrerequisites
    AnalyzePrerequisites --> RouteTasks
    RouteTasks --> ExecuteAgents
    ExecuteAgents --> EncodeGcfHandoff
    EncodeGcfHandoff --> VerifyOutput
    VerifyOutput --> FinalResponse : accepted
    VerifyOutput --> RouteTasks : improve
    FinalResponse --> FormatForUser
    FormatForUser --> [*]
```

## Agent Responsibility Map

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":70,"rankSpacing":85,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"25px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Structuring"] --> A1["Convert prompt into intent"]
    B["Planning"] --> B1["Split into tasks"]
    C["Prerequisites"] --> C1["Order dependencies"]
    D["Orchestrator"] --> D1["Choose next agent"]
    E["Specialists"] --> E1["Search, reason, compare, extract, write"]
    F["GCF Encoder"] --> F1["Compress handoffs"]
    G["Verifier"] --> G1["Check completeness"]
    H["Formatter"] --> H1["Match user response style"]

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,B,C,D,E,G,H green;
    class A1,B1,C1,D1,E1,F1,G1,H1 dark;
    class F gcf;
```

## GCF Agent Handoff Flow

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":80,"rankSpacing":100,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"27px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart LR
    A["Agent output"] --> B["GCF encoder"]
    B --> C["Compact payload"]
    C --> D["Next agent prompt"]
    D --> E["Better context"]

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,E green;
    class B,C gcf;
    class D dark;
```

## GCF Payload Shape

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":70,"rankSpacing":90,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"26px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
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

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,G green;
    class B,C,D,E dark;
    class F gcf;
```

## User-Preferred Response Layer

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":70,"rankSpacing":90,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"25px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Verified result"] --> B["Final GCF handoff"]
    C["User preference"] --> D["Response formatter"]
    B --> D
    D --> E["Output type"]
    E --> F["Summary"]
    E --> G["Report"]
    E --> H["Checklist"]
    E --> I["LinkedIn post"]
    E --> J["Table"]
    F --> K["Useful final answer"]
    G --> K
    H --> K
    I --> K
    J --> K

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,K green;
    class B gcf;
    class C,D,E,F,G,H,I,J dark;
```

## Tech Architecture

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":70,"rankSpacing":90,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"25px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
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

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,B,L green;
    class C,D,E,F,G,H,I,K dark;
    class J gcf;
```

## Example Flow

```mermaid
%%{init: {"theme":"base","flowchart":{"nodeSpacing":75,"rankSpacing":90,"curve":"basis","padding":30},"themeVariables":{"fontFamily":"Inter, Arial, sans-serif","fontSize":"25px","background":"#070B10","primaryColor":"#228B22","primaryTextColor":"#F9F9F9","primaryBorderColor":"#16651A","secondaryColor":"#F9F9F9","secondaryTextColor":"#101418","secondaryBorderColor":"#D99A2B","tertiaryColor":"#0B0F14","tertiaryTextColor":"#F9F9F9","tertiaryBorderColor":"#2A2F36","lineColor":"#D99A2B","textColor":"#F9F9F9","edgeLabelBackground":"#0B0F14"}}}%%
flowchart TD
    A["Custom user prompt"] --> B["Structure intent"]
    B --> C["Encode intent as GCF"]
    C --> D["Plan dependencies"]
    D --> E["Find source evidence"]
    E --> F["GCF evidence handoff"]
    F --> G["Compare or reason"]
    G --> H["Verify"]
    H --> I{"Ready?"}
    I -->|Yes| J["Final GCF handoff"]
    J --> K["User format"]
    K --> L["Final answer"]
    I -->|No| M["Improve plan"]
    M --> D

    classDef green fill:#228B22,stroke:#16651A,color:#F9F9F9,stroke-width:3px;
    classDef dark fill:#0B0F14,stroke:#2A2F36,color:#F9F9F9,stroke-width:2px;
    classDef gcf fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;
    classDef decision fill:#F9F9F9,stroke:#D99A2B,color:#101418,stroke-width:3px;

    class A,L green;
    class B,D,E,G,H,K,M dark;
    class C,F,J gcf;
    class I decision;
```
