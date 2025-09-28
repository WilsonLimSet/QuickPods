-- Add article_id to group translations together
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS article_id UUID;
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS total_views INTEGER DEFAULT 0;

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_podcasts_article_id ON podcasts(article_id);

-- Step 1: Generate article_id for English articles (the "master" version)
UPDATE podcasts 
SET article_id = gen_random_uuid() 
WHERE locale = 'en' AND article_id IS NULL;

-- Step 2: Copy article_id to all translations
UPDATE podcasts p
SET article_id = en.article_id
FROM podcasts en
WHERE p.md_slug = en.md_slug 
  AND en.locale = 'en' 
  AND p.locale != 'en'
  AND p.article_id IS NULL;

-- Step 3: Initialize total_views across all translations
UPDATE podcasts p
SET total_views = (
  SELECT COALESCE(SUM(views), 0)
  FROM podcasts
  WHERE article_id = p.article_id
)
WHERE article_id IS NOT NULL;

-- Step 4: Create trigger to keep total_views in sync automatically
CREATE OR REPLACE FUNCTION update_total_views()
RETURNS TRIGGER AS $$
BEGIN
  -- Update all rows with same article_id
  UPDATE podcasts
  SET total_views = (
    SELECT COALESCE(SUM(views), 0)
    FROM podcasts
    WHERE article_id = NEW.article_id
  )
  WHERE article_id = NEW.article_id;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_total_views ON podcasts;
CREATE TRIGGER trigger_update_total_views
AFTER UPDATE OF views ON podcasts
FOR EACH ROW
EXECUTE FUNCTION update_total_views();

-- Verify the setup
SELECT 
  md_slug,
  locale,
  article_id,
  views,
  total_views
FROM podcasts
ORDER BY md_slug, locale;
