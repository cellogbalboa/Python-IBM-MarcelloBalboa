-- Table: hello_world

-- DROP TABLE hello_world;



CREATE TABLE hello_world
(
    id serial NOT NULL,
    message_text text NOT NULL,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE hello_world
    OWNER to "ibm-cloud-base-user";