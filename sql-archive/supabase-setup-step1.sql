-- QuickPods Database Setup - Step 1: Create Tables
-- Run this FIRST

-- 1. Create Podcasts table
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

-- 2. Create Newsletter subscribers table
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

-- Tables created! Now run step 2.