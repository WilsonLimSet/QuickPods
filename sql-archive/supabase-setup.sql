-- QuickPods Database Setup
-- Run this in your Supabase SQL Editor: https://supabase.com/dashboard/project/ifbaqecltzlpuootdyfw/sql

-- 1. Create Podcasts table (if not exists)
CREATE TABLE IF NOT EXISTS podcasts (
  id SERIAL PRIMARY KEY,
  interviewer TEXT,
  interviewee TEXT,
  insights TEXT[],
  thumbnail_url TEXT,
  publish_date DATE,
  tag TEXT,
  md_slug TEXT UNIQUE,
  blog_content TEXT,
  views INTEGER DEFAULT 0,
  youtube_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create Newsletter subscribers table (if not exists)
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_podcasts_slug ON podcasts(md_slug);
CREATE INDEX IF NOT EXISTS idx_podcasts_date ON podcasts(publish_date DESC);
CREATE INDEX IF NOT EXISTS idx_podcasts_views ON podcasts(views DESC);
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter_subscribers(email);

-- 4. Enable Row Level Security (RLS)
ALTER TABLE podcasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;

-- 5. Create policies for public read access
CREATE POLICY IF NOT EXISTS "Enable read access for all users"
ON podcasts FOR SELECT
USING (true);

CREATE POLICY IF NOT EXISTS "Enable insert for all users"
ON podcasts FOR INSERT
WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "Enable update for all users"
ON podcasts FOR UPDATE
USING (true);

-- 6. Newsletter policies
CREATE POLICY IF NOT EXISTS "Enable insert for newsletter"
ON newsletter_subscribers FOR INSERT
WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "Enable read for newsletter"
ON newsletter_subscribers FOR SELECT
USING (true);

-- 7. Grant permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON podcasts TO anon, authenticated;
GRANT ALL ON newsletter_subscribers TO anon, authenticated;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

-- Setup complete!
-- You can now test the connection by running: pnpm dev