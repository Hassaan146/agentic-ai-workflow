# Environment And API Key Guide

Use this guide after the local dev skeleton is working.

## Local Dev Mode

```env
APP_ENV=dev
ALLOW_DEV_AUTH=true
BACKEND_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Local dev still accepts `dev-token`, but the frontend login/signup screens now use the FastAPI auth endpoints.

## FastAPI Auth

Used for:

- Signup
- Login
- JWT sessions
- Protected backend access

Backend only:

```env
JWT_SECRET=your_long_random_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
```

Generate `JWT_SECRET` with a long random value and keep it backend-only. Do not put it in the frontend or GitHub.

## Supabase

Used for:

- User profiles and password hashes
- Workflow runs
- Node traces
- Final outputs
- Usage logs

Backend only:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_or_secret_key
```

Important:

- Never put `SUPABASE_SERVICE_ROLE_KEY` in the frontend.
- Run `supabase/schema.sql` in the Supabase SQL editor before using the hosted database.

## Groq

Backend only:

```env
GROQ_API_KEY=your_fast_groq_api_key
GROQ_REASONING_API_KEY=your_reasoning_groq_api_key
DEFAULT_FAST_MODEL=llama-3.1-8b-instant
DEFAULT_REASONING_MODEL=llama-3.3-70b-versatile
```

## Google AI Studio / Gemini

Optional. Leave this empty if you want Groq only.

```env
GOOGLE_API_KEY=
```

## Search Provider

Backend only:

```env
SEARCH_PROVIDER=duckduckgo
```

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

```env
APP_ENV=production
ALLOW_DEV_AUTH=false
BACKEND_CORS_ORIGINS=https://your-vercel-app.vercel.app
JWT_SECRET=your_long_random_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_or_secret_key
GROQ_API_KEY=your_fast_groq_api_key
GROQ_REASONING_API_KEY=your_reasoning_groq_api_key
GOOGLE_API_KEY=
SEARCH_PROVIDER=duckduckgo
DEFAULT_FAST_MODEL=llama-3.1-8b-instant
DEFAULT_REASONING_MODEL=llama-3.3-70b-versatile
```

## Vercel Frontend Environment Variables

```env
NEXT_PUBLIC_API_BASE_URL=https://your-render-backend.onrender.com
```

## Secret Placement Checklist

- Vercel: only `NEXT_PUBLIC_*` values.
- Render: backend secrets, model keys, Supabase service role/secret key, JWT secret.
- Supabase: run the SQL schema, then copy URL and service role/secret key into Render.
- Groq: copy keys into Render as `GROQ_API_KEY` and optionally `GROQ_REASONING_API_KEY`.
