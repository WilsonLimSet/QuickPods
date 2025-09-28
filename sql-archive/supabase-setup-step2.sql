-- QuickPods Database Setup - Step 2: Security Policies
-- Run this AFTER step 1

-- 1. Enable Row Level Security (RLS)
ALTER TABLE podcasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE newsletter_subscribers ENABLE ROW LEVEL SECURITY;

-- 2. Create policies for podcasts (public access)
CREATE POLICY "Enable read access for all users"
ON podcasts FOR SELECT
USING (true);

CREATE POLICY "Enable insert for all users"
ON podcasts FOR INSERT
WITH CHECK (true);

CREATE POLICY "Enable update for all users"
ON podcasts FOR UPDATE
USING (true);

-- 3. Create policies for newsletter
CREATE POLICY "Enable insert for newsletter"
ON newsletter_subscribers FOR INSERT
WITH CHECK (true);

CREATE POLICY "Enable read for newsletter"
ON newsletter_subscribers FOR SELECT
USING (true);

-- Setup complete! You can now run: pnpm dev