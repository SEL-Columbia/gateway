-- Migration to move the circuit_id column to the primary log table from the log table.
-- 
-- 

-- Add a new column to the primary_log table
ALTER TABLE primary_log ADD COLUMN circuit_id integer;

-- Move the ids over.
UPDATE primary_log 
        SET circuit_id = log.circuit_id FROM log WHERE log.id = primary_log.id;

-- Make sure that all of the data moved correctly to the primary_log table
SELECT primary_log.id, log.id,
       primary_log.circuit_id, log.circuit_id FROM primary_log, log 
       WHERE primary_log.id = log.id AND primary_log.circuit_id != log.circuit_id; 

-- ALTER TABLE log DROP COLUMN circuit_id; 
ALTER TABLE log DROP COLUMN uuid;
 
