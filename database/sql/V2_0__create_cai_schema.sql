-- SCHEMA: cai

-- DROP SCHEMA cai ;

-- Creation will actually be handled automatically by Flyway
--CREATE SCHEMA cai
--    AUTHORIZATION "ibm-cloud-base-user";

COMMENT ON SCHEMA cai
    IS 'cai challenge application schema';

GRANT ALL ON SCHEMA cai TO "ibm-cloud-base-user";

GRANT ALL ON SCHEMA cai TO PUBLIC;