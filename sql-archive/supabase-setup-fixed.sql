-- QuickPods Database Setup (Fixed for older PostgreSQL versions)
-- Run this in your Supabase SQL Editor

-- 1. Drop existing policies if they exist (safe to run multiple times)
DROP POLICY IF EXISTS "Enable read access for all users" ON podcasts;
DROP POLICY IF EXISTS "Enable insert for all users" ON podcasts;
DROP POLICY IF EXISTS "Enable update for all users" ON podcasts;
DROP POLICY IF EXISTS "Enable insert for newsletter" ON newsletter_subscribers;
DROP POLICY IF EXISTS "Enable read for newsletter" ON newsletter_subscribers;

-- 2. Create Podcasts table
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

-- 3. Create Newsletter subscribers table
CREATE TABLE IF NOT EXISTS newsletter_subscribers (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  subscribed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_podcasts_slug ON podcasts(md_slug);
CREATE INDEX IF NOT EXISTS idx_podcasts_date ON podcasts(publish_date DESC);
CREATE INDEX IF NOT EXISTS idx_podcasts_views ON podcasts(views DESC);
CREATE INDEX IF NOT EXISTS idx_newsletter_email ON newsletter_subscribers(email);

-- 5. Enable Row Level Security (RLS)
ALTER TABLE podcasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;

-- 6. Create policies for public read access (without IF NOT EXISTS)
CREATE POLICY "Enable read access for all users"
ON podcasts FOR SELECT
USING (true);

CREATE POLICY "Enable insert for all users"
ON podcasts FOR INSERT
WITH CHECK (true);

CREATE POLICY "Enable update for all users"
ON podcasts FOR UPDATE
USING (true);

-- 7. Newsletter policies
CREATE POLICY "Enable insert for newsletter"
ON newsletter_subscribers FOR INSERT
WITH CHECK (true);

CREATE POLICY "Enable read for newsletter"
ON newsletter_subscribers FOR SELECT
USING (true);

-- Setup complete!