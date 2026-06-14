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

## Admin Panel

Admins are controlled by email. Put the email address you will use to sign up in the backend environment:

```env
ADMIN_EMAILS=your_admin_email@example.com
```

You can add multiple admins with commas:

```env
ADMIN_EMAILS=you@example.com,teammate@example.com
```

Set this before registering your admin account. If you already registered first, update the user in Supabase:

```sql
update public.user_profiles set is_admin = true where email = 'your_admin_email@example.com';
```

After login, open `/admin` to see users, runs, traces, usage logs, and token estimates.

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
SUPABASE_SERVICE_ROLE_KEY=your_jwt_service_role_key
```

Important:

- Never put `SUPABASE_SERVICE_ROLE_KEY` in the frontend.
- Use the JWT-style Supabase `service_role` key for this backend SDK. Do not use the public/publishable key, and do not use a key format that starts with `sb_secret_` unless you also replace the Supabase client implementation.
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
ADMIN_EMAILS=your_admin_email@example.com
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_jwt_service_role_key
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
- Render: backend secrets, model keys, Supabase service role key, JWT secret, and `ADMIN_EMAILS`.
- Supabase: run the SQL schema, then copy URL and JWT-style service role key into Render.
- Groq: copy keys into Render as `GROQ_API_KEY` and optionally `GROQ_REASONING_API_KEY`.
