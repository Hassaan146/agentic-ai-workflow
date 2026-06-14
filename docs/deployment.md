# Deployment Notes

## Frontend: Vercel

- Root directory: `frontend`
- Build command: `npm run build`
- Environment variables:
  - `NEXT_PUBLIC_API_BASE_URL`

## Backend: Render

- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables:
  - `APP_ENV=production`
  - `ALLOW_DEV_AUTH=false`
  - `BACKEND_CORS_ORIGINS`
  - `JWT_SECRET`
  - `JWT_ALGORITHM=HS256`
  - `JWT_EXPIRE_MINUTES=10080`
  - `ADMIN_EMAILS`
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `GROQ_API_KEY`
  - `GROQ_REASONING_API_KEY`
  - `GOOGLE_API_KEY`
  - `SEARCH_PROVIDER=duckduckgo`
  - `DEFAULT_FAST_MODEL`
  - `DEFAULT_REASONING_MODEL`

## Database: Supabase

- Run `supabase/schema.sql` in the Supabase SQL editor.
- Keep the JWT-style service role key on the backend only.
- Local FastAPI auth stores password hashes in `user_profiles.password_hash`.
- The existing `clerk_user_id` column is reused as a local user id for backward compatibility.

## Admin Access

- Set `ADMIN_EMAILS` to the email you will use for the admin signup.
- Sign up with that email, then open `/admin` after login.
- If the account already exists, set `user_profiles.is_admin = true` for that email in Supabase.
- Use the JWT-style Supabase service role key on Render; keep it backend-only.
