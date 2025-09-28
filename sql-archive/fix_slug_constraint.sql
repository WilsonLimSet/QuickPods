-- Drop the unique constraint on md_slug
ALTER TABLE podcasts DROP CONSTRAINT IF EXISTS podcasts_md_slug_key;

-- Add a composite unique constraint on (md_slug, locale)
ALTER TABLE podcasts ADD CONSTRAINT podcasts_md_slug_locale_key UNIQUE (md_slug, locale);
