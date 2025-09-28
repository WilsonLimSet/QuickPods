-- Add article_id column to group translations together
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS article_id UUID;

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_podcasts_article_id ON podcasts(article_id);

-- Step 1: For each unique md_slug in English, generate a UUID
-- This creates the "master" article_id for each unique article
UPDATE podcasts 
SET article_id = gen_random_uuid() 
WHERE locale = 'en' AND article_id IS NULL;

-- Step 2: Copy the article_id from English version to all translations
-- This links all language versions of the same article together
UPDATE podcasts p
SET article_id = en.article_id
FROM podcasts en
WHERE p.md_slug = en.md_slug 
  AND en.locale = 'en' 
  AND p.locale != 'en'
  AND p.article_id IS NULL;

-- Create a view to get total views across all languages
CREATE OR REPLACE VIEW podcast_views AS
SELECT 
  article_id,
  SUM(views) as total_views
FROM podcasts
WHERE article_id IS NOT NULL
GROUP BY article_id;

-- Verify the setup
SELECT 
  md_slug,
  locale,
  article_id,
  views
FROM podcasts
ORDER BY md_slug, locale;
