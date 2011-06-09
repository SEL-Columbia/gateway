-- Converts the type of start and end columsn to dates
-- Ivan, 6 9 2011

--  Add the temp columns to store the dates as strings
ALTER TABLE jobs ADD COLUMN start_tmp timestamp without time zone ;

-- Move the info to the temp columns
UPDATE jobs SET start_tmp = to_timestamp(start, 'YYYY-MM-DD HH24:MI:SS') ; 

-- Remove the old start and end columns
ALTER TABLE jobs DROP COLUMN start; 

-- Adds the columns back with the correct type
ALTER TABLE jobs ADD COLUMN start timestamp without time zone; 

-- Add the info back to the start column
UPDATE jobs SET start = start_tmp ; 

-- remove the tmp column
ALTER TABLE jobs DROP COLUMN start_tmp;
