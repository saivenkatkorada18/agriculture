# Database & Row Level Security (RLS) Rules

## Database Target: Supabase PostgreSQL + SQLite local fallback

## Schema Conventions
1. All table names in lowercase snake_case (`profiles`, `analyses`, `recommendations`, `chat_sessions`, `chat_messages`).
2. Primary keys use `UUID` default `gen_random_uuid()` (or integer autoincrement for SQLite fallback).
3. Foreign keys must specify `ON DELETE CASCADE` where child records (e.g. recommendations, chat messages) belong to a parent record.
4. Timestamps use `TIMESTAMPTZ` default `NOW()`.

## Row Level Security (RLS) Policy
- `ENABLE ROW LEVEL SECURITY` on all user-facing tables.
- Standard policy: `CREATE POLICY "Users can only access own records" ON analyses FOR ALL USING (auth.uid() = user_id);`
- Service role keys must NEVER be bundled in the client bundle. Only `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` can be exposed to frontend.
