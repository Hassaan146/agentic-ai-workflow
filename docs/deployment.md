# Deployment Notes

## Frontend: Vercel

- Root directory: `frontend`
- Build command: `npm run build`
- Environment variables:
  - `NEXT_PUBLIC_AUTH_MODE=clerk`
  - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
  - `NEXT_PUBLIC_API_BASE_URL`

## Backend: Render

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables:
  - `APP_ENV=production`
  - `ALLOW_DEV_AUTH=false`
  - `BACKEND_CORS_ORIGINS`
  - `CLERK_JWKS_URL`
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `GROQ_API_KEY`
  - `GOOGLE_API_KEY`
  - `SEARCH_PROVIDER`
  - `DEFAULT_FAST_MODEL`
  - `DEFAULT_REASONING_MODEL`

## Database: Supabase

- Run `supabase/schema.sql` in the Supabase SQL editor.
- Keep the service role key on the backend only.
- Store Clerk user IDs in `clerk_user_id`.
