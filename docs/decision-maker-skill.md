# Decision Maker Skill Integration

This project now includes a backend implementation of the downloaded `decision-maker.skill.md` workflow and the Claude Code website pipeline PDF.

It is also saved as an always-on project memory in:

- `docs/project-memory.md`
- `backend/app/design_skill/memory.py`

## What It Does

The skill guides a user through:

1. Six decisions:
   - feeling
   - audience
   - anti-audience
   - hero object
   - job
   - three-second memory
2. Three reference buckets:
   - feeling
   - structure
   - detail
3. Three style logics:
   - color
   - typography
   - spatial
4. Final outputs:
   - copywriter prompt
   - visual/3D prompt
   - design prompt
   - developer prompt
   - GitHub/Vercel launch guide

## API Endpoints

Start the guided skill:

```http
GET /api/design-skill/start
```

Advance the skill:

```http
POST /api/design-skill/answer
```

Body:

```json
{
  "state": {
    "current_step": "project"
  },
  "answer": "Agentic AI Workflow\nA multi-agent workflow platform for builders."
}
```

Read the Claude Code website pipeline:

```http
GET /api/design-skill/pipeline
```

Read the saved project memory:

```http
GET /api/design-skill/memory
```

## Pipeline Implemented From PDF

The pipeline has 11 steps:

1. Brief and copywriting
2. Find a section reference
3. Strip background into clean UI reference
4. Recreate layout in Claude Code / Next.js
5. Typography
6. Color palettes
7. 3D models
8. Image and video generation
9. Animation references
10. Asset compression
11. Deploy

## Frontend Use Later

When we build the real frontend, this can become a guided wizard:

- left panel: current question
- center: user answer box
- right panel: locked brief summary
- final screen: copyable AI prompts and launch guide
