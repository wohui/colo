SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;


CREATE EXTENSION IF NOT EXISTS timescaledb WITH SCHEMA public;



COMMENT ON EXTENSION timescaledb IS 'Enables scalable inserts and complex queries for time-series data';


CREATE EXTENSION IF NOT EXISTS tablefunc WITH SCHEMA public;



COMMENT ON EXTENSION tablefunc IS 'functions that manipulate whole tables, including crosstab';


SET default_tablespace = '';

SET default_with_oids = false;


CREATE TABLE public.request (
    "time" timestamp with time zone NOT NULL,
    run_id timestamp with time zone NOT NULL,
    exception text,
    greenlet_id integer NOT NULL,
    loadgen text NOT NULL,
    name text NOT NULL,
    request_type text NOT NULL,
    response_length integer,
    response_time double precision,
    success smallint NOT NULL,
    testplan character varying(255) NOT NULL,
    pid integer,
    context jsonb,
    url character varying(255)
);


ALTER TABLE public.request OWNER TO postgres;

CREATE TABLE public.testrun (
    id timestamp with time zone NOT NULL,
    testplan text NOT NULL,
    profile_name text,
    num_clients integer NOT NULL,
    rps double precision,
    description text,
    end_time timestamp with time zone,
    env character varying(10) NOT NULL,
    username character varying(64),
    gitrepo character varying(120),
    rps_avg numeric,
    resp_time_avg numeric,
    changeset_guid character varying(36),
    fail_ratio double precision,
    requests integer,
    arguments text,
    exit_code integer
);


ALTER TABLE public.testrun OWNER TO postgres;


CREATE TABLE public.user_count (
    testplan character varying(255) NOT NULL,
    user_count integer NOT NULL,
    "time" timestamp with time zone NOT NULL,
    run_id timestamp with time zone
);


ALTER TABLE public.user_count OWNER TO postgres;


CREATE TABLE public.events (
    "time" timestamp with time zone NOT NULL,
    text text NOT NULL
);


ALTER TABLE public.events OWNER TO postgres;


ALTER TABLE ONLY public.testrun
    ADD CONSTRAINT testrun_pkey PRIMARY KEY (id);


CREATE INDEX request_time_idx ON public.request USING btree ("time" DESC);



CREATE INDEX run_id_idx ON public.request USING btree (run_id);


CREATE INDEX testrun_id_idx ON public.testrun USING btree (id DESC);

CREATE INDEX user_count_time_idx ON public.user_count USING btree ("time" DESC);
