-- Add interviewee_title column to podcasts table
ALTER TABLE podcasts ADD COLUMN IF NOT EXISTS interviewee_title TEXT;

-- Update existing records to have empty string instead of NULL
UPDATE podcasts SET interviewee_title = '' WHERE interviewee_title IS NULL;