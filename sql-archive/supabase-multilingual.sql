-- Add multilingual support to podcasts table
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS locale TEXT DEFAULT 'en';

-- Create index for fast locale + slug lookups
CREATE INDEX IF NOT EXISTS idx_podcasts_locale_slug ON podcasts(locale, md_slug);

-- Create index for locale filtering
CREATE INDEX IF NOT EXISTS idx_podcasts_locale ON podcasts(locale);

-- Migrate existing posts to English locale (if not already set)
UPDATE podcasts SET locale = 'en' WHERE locale IS NULL OR locale = '';

-- Create unique constraint for slug + locale combination to prevent duplicates
-- (This will fail if you already have duplicate slugs, which is expected for now)
-- ALTER TABLE podcasts ADD CONSTRAINT unique_slug_locale UNIQUE (md_slug, locale);