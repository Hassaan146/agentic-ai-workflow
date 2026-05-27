# Environment And API Key Guide

Use this guide after the local dev skeleton is working.

## Local Dev Mode

For local development without external services, use:

```env
APP_ENV=dev
ALLOW_DEV_AUTH=true
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
NEXT_PUBLIC_AUTH_MODE=dev
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

This makes the frontend send `dev-token` to the backend. The backend accepts `dev-token` as a local development user.

## Clerk

Used for:

- Login
- Signup
- User sessions
- Protected frontend access
- Protected backend access

Where to place keys:

- Frontend: `frontend/.env.local`
- Backend: `backend/.env`

Frontend:

```env
NEXT_PUBLIC_AUTH_MODE=clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
```

Backend:

```env
CLERK_JWKS_URL=https://your-clerk-domain/.well-known/jwks.json
```

You do not need to put a Clerk secret key in the frontend. The current backend verifies Clerk JWTs through `CLERK_JWKS_URL`, so the required Clerk values are:

- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`: Vercel/frontend only. This is the `pk_test_...` or `pk_live_...` key.
- `CLERK_JWKS_URL`: Render/backend only. In Clerk, copy the JWKS URL from the JWT/session verification settings, or use the domain form shown above.

Keep `CLERK_SECRET_KEY` backend-only if you later add Clerk server SDK actions. It is not required for the current MVP auth verification path.

## Supabase

Used for:

- User profiles
- Workflow runs
- Node traces
- Final outputs
- Usage logs

Where to place keys:

- Backend only: `backend/.env`

Backend:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
```

Important:

- Never put `SUPABASE_SERVICE_ROLE_KEY` in the frontend.
- Run `supabase/schema.sql` in the Supabase SQL editor before using the hosted database.

## Groq

Used for:

- Fast model calls
- Request structuring
- Routing-style tasks

Where to place key:

- Backend only: `backend/.env`

```env
GROQ_API_KEY=your_groq_api_key
DEFAULT_FAST_MODEL=llama-3.1-8b-instant
```

## Google AI Studio / Gemini

Used for:

- Reasoning
- Synthesis
- Final answer generation

Where to place key:

- Backend only: `backend/.env`

```env
GOOGLE_API_KEY=your_google_ai_studio_key
DEFAULT_REASONING_MODEL=gemini-1.5-flash
```

## Search Provider

Used for controlled research sources.

Backend only:

```env
SEARCH_PROVIDER=mock
```

Use `mock` for local testing and portfolio demos without network dependency. Use `duckduckgo` when you want the MVP to fetch real public search-style results without adding another paid key.

## Frontend API URL

Local:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Production:

```env
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend.onrender.com
```

## Render Backend Environment Variables

Set these in Render:

```env
APP_ENV=production
ALLOW_DEV_AUTH=false
BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app
CLERK_JWKS_URL=https://your-clerk-domain/.well-known/jwks.json
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_ai_studio_key
SEARCH_PROVIDER=mock
DEFAULT_FAST_MODEL=llama-3.1-8b-instant
DEFAULT_REASONING_MODEL=gemini-1.5-flash
```

## Vercel Frontend Environment Variables

Set these in Vercel:

```env
NEXT_PUBLIC_AUTH_MODE=clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_or_live_key
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend.onrender.com
```

## Secret Placement Checklist

- Vercel: only `NEXT_PUBLIC_*` values.
- Render: backend secrets, model keys, Supabase service role key, Clerk JWKS URL.
- Supabase: run the SQL schema, then copy URL and service role key into Render.
- Clerk: copy publishable key into Vercel and JWKS URL into Render.
- Groq: copy API key into Render as `GROQ_API_KEY`.
- Google AI Studio: copy API key into Render as `GOOGLE_API_KEY`.
