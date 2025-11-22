-- Fix PM Temperature Control timing to open at 5pm instead of noon
-- PM checks should only be available from 5pm to midnight

UPDATE categories
SET opens_at = '17:00:00'
WHERE id = 128 AND name = 'Temperature Control (PM)';
