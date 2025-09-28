-- Add locale column to podcasts table
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS locale TEXT DEFAULT 'en';

-- Update all existing rows to have 'en' locale
UPDATE podcasts SET locale = 'en' WHERE locale IS NULL;

-- Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_podcasts_locale ON podcasts(locale);
CREATE INDEX IF NOT EXISTS idx_podcasts_slug_locale ON podcasts(md_slug, locale);
