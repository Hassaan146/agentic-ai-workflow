# LinkedIn Build Journey Plan

## Post 1: Project Announcement

Theme: Why this project exists.

Key message:

Normal chatbots answer complex tasks in one hidden step. Agentic AI Workflow turns a messy request into a structured, dependency-aware workflow and routes it through specialized agents.

Visual:

Use the main product workflow diagram.

## Post 2: Product Design Thinking

Theme: How the system understands a user request.

Key message:

The first agent does not answer the user. It restructures the request so the rest of the system can reason over clean tasks, constraints, and expected output.

Visual:

Use the request structure and task decomposition section from the state graph.

## Post 3: State Graph Architecture

Theme: Why LangGraph matters.

Key message:

This project uses a state graph because the workflow is not linear. Some agents run only when needed, and the verifier can route work back if the answer is incomplete.

Visual:

Use the LangGraph state graph diagram.

## Post 4: Tech Stack

Theme: Tool selection and product architecture.

Key message:

Each tool has one clear responsibility: Next.js for the interface, FastAPI for APIs, LangGraph for orchestration, LangChain for models/tools, FastAPI JWT auth, Supabase for storage, Vercel and Render for deployment.

Visual:

Use the tech architecture diagram.

## Post 5: First Working MVP

Theme: From design to execution.

Key message:

The first MVP will support login, a dashboard, one general workflow, live agent execution trace, saved runs, and final output with sources.

Visual:

Use a screenshot of the dashboard or run page after implementation.

## Post 6: Testing And Deployment

Theme: Production mindset.

Key message:

The project is tested at every layer: backend endpoints, auth, Supabase, LangGraph routing, agent outputs, frontend states, and deployed workflow execution.

Visual:

Use a simple testing pyramid or deployment checklist.
