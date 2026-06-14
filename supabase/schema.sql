create table if not exists public.user_profiles (
    id uuid primary key default gen_random_uuid(),
    clerk_user_id text not null unique,
    email text,
    full_name text,
    password_hash text,
    auth_provider text not null default 'local',
    is_admin boolean not null default false,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.workflow_runs (
    id uuid primary key default gen_random_uuid(),
    clerk_user_id text not null,
    template_key text not null default 'general',
    user_request text not null,
    status text not null default 'queued',
    final_output jsonb,
    error_message text,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists public.node_traces (
    id uuid primary key default gen_random_uuid(),
    run_id uuid not null references public.workflow_runs(id) on delete cascade,
    node_key text not null,
    agent_name text not null,
    status text not null,
    input_payload jsonb,
    output_payload jsonb,
    error_message text,
    started_at timestamptz not null default now(),
    completed_at timestamptz
);

create table if not exists public.usage_logs (
    id uuid primary key default gen_random_uuid(),
    run_id uuid references public.workflow_runs(id) on delete cascade,
    provider text not null,
    model text not null,
    purpose text not null,
    prompt_tokens integer not null default 0,
    completion_tokens integer not null default 0,
    estimated_cost numeric(12, 6) not null default 0,
    created_at timestamptz not null default now()
);


alter table public.user_profiles
    add column if not exists password_hash text;

alter table public.user_profiles
    add column if not exists auth_provider text not null default 'local';


alter table public.user_profiles
    add column if not exists is_admin boolean not null default false;
