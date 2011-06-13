--  Migration file to add token_id column to add_credit job table
--  Ivan Willig

ALTER TABLE addcredit ADD COLUMN token_id integer;
