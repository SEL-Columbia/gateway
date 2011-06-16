--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE account (
    id integer NOT NULL,
    pin character varying,
    name character varying,
    phone character varying,
    lang character varying
);


ALTER TABLE public.account OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_id_seq OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE account_id_seq OWNED BY account.id;


--
-- Name: addcredit; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE addcredit (
    id integer NOT NULL,
    credit integer,
    token_id integer
);


ALTER TABLE public.addcredit OWNER TO postgres;

--
-- Name: airtel_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE airtel_interface (
    id integer NOT NULL,
    host character varying
);


ALTER TABLE public.airtel_interface OWNER TO postgres;

--
-- Name: alert; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE alert (
    id integer NOT NULL,
    date timestamp without time zone,
    text character varying,
    message_id integer,
    circuit_id integer
);


ALTER TABLE public.alert OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE alert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_id_seq OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE alert_id_seq OWNED BY alert.id;


--
-- Name: circuit; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE circuit (
    id integer NOT NULL,
    uuid character varying,
    date timestamp without time zone,
    pin character varying,
    meter integer,
    energy_max double precision,
    power_max double precision,
    status integer,
    ip_address character varying,
    credit double precision,
    account_id integer
);


ALTER TABLE public.circuit OWNER TO postgres;

--
-- Name: circuit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE circuit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.circuit_id_seq OWNER TO postgres;

--
-- Name: circuit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE circuit_id_seq OWNED BY circuit.id;


--
-- Name: communication_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE communication_interface (
    type character varying,
    id integer NOT NULL,
    name character varying,
    provider character varying,
    location character varying,
    phone character varying
);


ALTER TABLE public.communication_interface OWNER TO postgres;

--
-- Name: communication_interface_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE communication_interface_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.communication_interface_id_seq OWNER TO postgres;

--
-- Name: communication_interface_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE communication_interface_id_seq OWNED BY communication_interface.id;


--
-- Name: cping; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE cping (
    id integer NOT NULL
);


ALTER TABLE public.cping OWNER TO postgres;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groups (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groups_id_seq OWNED BY groups.id;


--
-- Name: incoming_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE incoming_message (
    id integer NOT NULL,
    text character varying,
    communication_interface_id integer
);


ALTER TABLE public.incoming_message OWNER TO postgres;

--
-- Name: job_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE job_message (
    id integer NOT NULL,
    job_id integer,
    incoming character varying(100),
    text character varying(100)
);


ALTER TABLE public.job_message OWNER TO postgres;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE jobs (
    id integer NOT NULL,
    type character varying(50),
    uuid character varying,
    state boolean,
    circuit_id integer,
    start timestamp without time zone,
    "end" timestamp without time zone
);


ALTER TABLE public.jobs OWNER TO postgres;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_id_seq OWNER TO postgres;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE jobs_id_seq OWNED BY jobs.id;


--
-- Name: kannel_incoming__message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_incoming__message (
    id integer NOT NULL,
    text character varying
);


ALTER TABLE public.kannel_incoming__message OWNER TO postgres;

--
-- Name: kannel_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_interface (
    id integer NOT NULL,
    host character varying,
    port integer,
    username character varying,
    password character varying
);


ALTER TABLE public.kannel_interface OWNER TO postgres;

--
-- Name: kannel_job_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_job_message (
    id integer NOT NULL,
    job_id integer,
    incoming character varying,
    text character varying
);


ALTER TABLE public.kannel_job_message OWNER TO postgres;

--
-- Name: kannel_outgoing_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_outgoing_message (
    id integer NOT NULL,
    text character varying,
    incoming character varying
);


ALTER TABLE public.kannel_outgoing_message OWNER TO postgres;

--
-- Name: log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE log (
    id integer NOT NULL,
    date timestamp without time zone,
    uuid character varying,
    type character varying(50),
    circuit_id integer
);


ALTER TABLE public.log OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.log_id_seq OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE message (
    type character varying(50),
    id integer NOT NULL,
    date timestamp without time zone,
    sent boolean,
    number character varying,
    uuid character varying
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE message_id_seq OWNED BY message.id;


--
-- Name: meter; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meter (
    id integer NOT NULL,
    uuid character varying,
    phone character varying,
    name character varying,
    location character varying,
    status boolean,
    date timestamp without time zone,
    battery integer,
    panel_capacity integer,
    communication character varying,
    slug character varying(100),
    communication_interface_id integer,
    geometry text
);


ALTER TABLE public.meter OWNER TO postgres;

--
-- Name: meter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_id_seq OWNER TO postgres;

--
-- Name: meter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meter_id_seq OWNED BY meter.id;


--
-- Name: meter_messages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meter_messages (
    id integer NOT NULL,
    message_id integer,
    meter_id integer
);


ALTER TABLE public.meter_messages OWNER TO postgres;

--
-- Name: meter_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meter_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_messages_id_seq OWNER TO postgres;

--
-- Name: meter_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meter_messages_id_seq OWNED BY meter_messages.id;


--
-- Name: meterchangeset; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meterchangeset (
    id integer NOT NULL,
    date timestamp without time zone,
    meter integer,
    meterconfigkey integer,
    value character varying
);


ALTER TABLE public.meterchangeset OWNER TO postgres;

--
-- Name: meterchangeset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meterchangeset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meterchangeset_id_seq OWNER TO postgres;

--
-- Name: meterchangeset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meterchangeset_id_seq OWNED BY meterchangeset.id;


--
-- Name: meterconfigkey; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meterconfigkey (
    id integer NOT NULL,
    key character varying
);


ALTER TABLE public.meterconfigkey OWNER TO postgres;

--
-- Name: meterconfigkey_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meterconfigkey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meterconfigkey_id_seq OWNER TO postgres;

--
-- Name: meterconfigkey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meterconfigkey_id_seq OWNED BY meterconfigkey.id;


--
-- Name: mping; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mping (
    id integer NOT NULL
);


ALTER TABLE public.mping OWNER TO postgres;

--
-- Name: netbook_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE netbook_interface (
    id integer NOT NULL
);


ALTER TABLE public.netbook_interface OWNER TO postgres;

--
-- Name: outgoing_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE outgoing_message (
    id integer NOT NULL,
    text character varying,
    incoming character varying
);


ALTER TABLE public.outgoing_message OWNER TO postgres;

--
-- Name: primary_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE primary_log (
    id integer NOT NULL,
    watthours double precision,
    use_time double precision,
    created timestamp without time zone,
    credit double precision,
    status integer
);


ALTER TABLE public.primary_log OWNER TO postgres;

--
-- Name: system_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE system_log (
    id integer NOT NULL,
    uuid character varying,
    text character varying,
    created character varying
);


ALTER TABLE public.system_log OWNER TO postgres;

--
-- Name: system_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE system_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.system_log_id_seq OWNER TO postgres;

--
-- Name: system_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE system_log_id_seq OWNED BY system_log.id;


--
-- Name: test_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_message (
    id integer NOT NULL,
    date timestamp without time zone,
    text character varying
);


ALTER TABLE public.test_message OWNER TO postgres;

--
-- Name: test_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE test_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_message_id_seq OWNER TO postgres;

--
-- Name: test_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE test_message_id_seq OWNED BY test_message.id;


--
-- Name: token; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE token (
    id integer NOT NULL,
    created timestamp without time zone,
    token numeric,
    value numeric,
    state character varying,
    batch_id integer
);


ALTER TABLE public.token OWNER TO postgres;

--
-- Name: token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_id_seq OWNER TO postgres;

--
-- Name: token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE token_id_seq OWNED BY token.id;


--
-- Name: tokenbatch; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tokenbatch (
    id integer NOT NULL,
    uuid character varying,
    created timestamp without time zone
);


ALTER TABLE public.tokenbatch OWNER TO postgres;

--
-- Name: tokenbatch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tokenbatch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tokenbatch_id_seq OWNER TO postgres;

--
-- Name: tokenbatch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tokenbatch_id_seq OWNED BY tokenbatch.id;


--
-- Name: turnoff; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE turnoff (
    id integer NOT NULL
);


ALTER TABLE public.turnoff OWNER TO postgres;

--
-- Name: turnon; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE turnon (
    id integer NOT NULL
);


ALTER TABLE public.turnon OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    name character varying(100),
    password character varying(100),
    email character varying(100),
    group_id integer,
    notify boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE account ALTER COLUMN id SET DEFAULT nextval('account_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE alert ALTER COLUMN id SET DEFAULT nextval('alert_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE circuit ALTER COLUMN id SET DEFAULT nextval('circuit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE communication_interface ALTER COLUMN id SET DEFAULT nextval('communication_interface_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE groups ALTER COLUMN id SET DEFAULT nextval('groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE jobs ALTER COLUMN id SET DEFAULT nextval('jobs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE message ALTER COLUMN id SET DEFAULT nextval('message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meter ALTER COLUMN id SET DEFAULT nextval('meter_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meter_messages ALTER COLUMN id SET DEFAULT nextval('meter_messages_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meterchangeset ALTER COLUMN id SET DEFAULT nextval('meterchangeset_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meterconfigkey ALTER COLUMN id SET DEFAULT nextval('meterconfigkey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE system_log ALTER COLUMN id SET DEFAULT nextval('system_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE test_message ALTER COLUMN id SET DEFAULT nextval('test_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE token ALTER COLUMN id SET DEFAULT nextval('token_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE tokenbatch ALTER COLUMN id SET DEFAULT nextval('tokenbatch_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: addcredit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY addcredit
    ADD CONSTRAINT addcredit_pkey PRIMARY KEY (id);


--
-- Name: airtel_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY airtel_interface
    ADD CONSTRAINT airtel_interface_pkey PRIMARY KEY (id);


--
-- Name: alert_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_pkey PRIMARY KEY (id);


--
-- Name: circuit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_pkey PRIMARY KEY (id);


--
-- Name: communication_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY communication_interface
    ADD CONSTRAINT communication_interface_pkey PRIMARY KEY (id);


--
-- Name: cping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY cping
    ADD CONSTRAINT cping_pkey PRIMARY KEY (id);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: incoming_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY incoming_message
    ADD CONSTRAINT incoming_message_pkey PRIMARY KEY (id);


--
-- Name: job_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_pkey PRIMARY KEY (id);


--
-- Name: jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: kannel_incoming__message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_incoming__message
    ADD CONSTRAINT kannel_incoming__message_pkey PRIMARY KEY (id);


--
-- Name: kannel_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_interface
    ADD CONSTRAINT kannel_interface_pkey PRIMARY KEY (id);


--
-- Name: kannel_job_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_pkey PRIMARY KEY (id);


--
-- Name: kannel_outgoing_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_outgoing_message
    ADD CONSTRAINT kannel_outgoing_message_pkey PRIMARY KEY (id);


--
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: meter_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_pkey PRIMARY KEY (id);


--
-- Name: meter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meter
    ADD CONSTRAINT meter_pkey PRIMARY KEY (id);


--
-- Name: meterchangeset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_pkey PRIMARY KEY (id);


--
-- Name: meterconfigkey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meterconfigkey
    ADD CONSTRAINT meterconfigkey_pkey PRIMARY KEY (id);


--
-- Name: mping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mping
    ADD CONSTRAINT mping_pkey PRIMARY KEY (id);


--
-- Name: netbook_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY netbook_interface
    ADD CONSTRAINT netbook_interface_pkey PRIMARY KEY (id);


--
-- Name: outgoing_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY outgoing_message
    ADD CONSTRAINT outgoing_message_pkey PRIMARY KEY (id);


--
-- Name: primary_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY primary_log
    ADD CONSTRAINT primary_log_pkey PRIMARY KEY (id);


--
-- Name: system_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY system_log
    ADD CONSTRAINT system_log_pkey PRIMARY KEY (id);


--
-- Name: test_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_message
    ADD CONSTRAINT test_message_pkey PRIMARY KEY (id);


--
-- Name: token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: tokenbatch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tokenbatch
    ADD CONSTRAINT tokenbatch_pkey PRIMARY KEY (id);


--
-- Name: turnoff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY turnoff
    ADD CONSTRAINT turnoff_pkey PRIMARY KEY (id);


--
-- Name: turnon_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY turnon
    ADD CONSTRAINT turnon_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: addcredit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY addcredit
    ADD CONSTRAINT addcredit_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: airtel_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY airtel_interface
    ADD CONSTRAINT airtel_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: alert_circuit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_circuit_id_fkey FOREIGN KEY (circuit_id) REFERENCES circuit(id);


--
-- Name: alert_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_message_id_fkey FOREIGN KEY (message_id) REFERENCES message(id);


--
-- Name: circuit_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_account_id_fkey FOREIGN KEY (account_id) REFERENCES account(id);


--
-- Name: circuit_meter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_meter_fkey FOREIGN KEY (meter) REFERENCES meter(id);


--
-- Name: cping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cping
    ADD CONSTRAINT cping_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: incoming_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY incoming_message
    ADD CONSTRAINT incoming_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: job_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: job_message_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(id);


--
-- Name: kannel_incoming__message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_incoming__message
    ADD CONSTRAINT kannel_incoming__message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: kannel_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_interface
    ADD CONSTRAINT kannel_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: kannel_job_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: kannel_job_message_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(id);


--
-- Name: kannel_outgoing_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_outgoing_message
    ADD CONSTRAINT kannel_outgoing_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: meter_messages_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_message_id_fkey FOREIGN KEY (message_id) REFERENCES message(id);


--
-- Name: meter_messages_meter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_meter_id_fkey FOREIGN KEY (meter_id) REFERENCES meter(id);


--
-- Name: meterchangeset_meter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_meter_fkey FOREIGN KEY (meter) REFERENCES meter(id);


--
-- Name: meterchangeset_meterconfigkey_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_meterconfigkey_fkey FOREIGN KEY (meterconfigkey) REFERENCES meterconfigkey(id);


--
-- Name: mping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mping
    ADD CONSTRAINT mping_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: netbook_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY netbook_interface
    ADD CONSTRAINT netbook_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: outgoing_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY outgoing_message
    ADD CONSTRAINT outgoing_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: primary_log_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY primary_log
    ADD CONSTRAINT primary_log_id_fkey FOREIGN KEY (id) REFERENCES log(id);


--
-- Name: token_batch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES tokenbatch(id);


--
-- Name: turnoff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY turnoff
    ADD CONSTRAINT turnoff_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: turnon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY turnon
    ADD CONSTRAINT turnon_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: users_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE OR REPLACE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: account; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE account (
    id integer NOT NULL,
    pin character varying,
    name character varying,
    phone character varying,
    lang character varying
);


ALTER TABLE public.account OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE account_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.account_id_seq OWNER TO postgres;

--
-- Name: account_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE account_id_seq OWNED BY account.id;


--
-- Name: addcredit; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE addcredit (
    id integer NOT NULL,
    credit integer,
    token_id integer
);


ALTER TABLE public.addcredit OWNER TO postgres;

--
-- Name: airtel_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE airtel_interface (
    id integer NOT NULL,
    host character varying
);


ALTER TABLE public.airtel_interface OWNER TO postgres;

--
-- Name: alert; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE alert (
    id integer NOT NULL,
    date timestamp without time zone,
    text character varying,
    message_id integer,
    circuit_id integer
);


ALTER TABLE public.alert OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE alert_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.alert_id_seq OWNER TO postgres;

--
-- Name: alert_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE alert_id_seq OWNED BY alert.id;


--
-- Name: circuit; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE circuit (
    id integer NOT NULL,
    uuid character varying,
    date timestamp without time zone,
    pin character varying,
    meter integer,
    energy_max double precision,
    power_max double precision,
    status integer,
    ip_address character varying,
    credit double precision,
    account_id integer
);


ALTER TABLE public.circuit OWNER TO postgres;

--
-- Name: circuit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE circuit_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.circuit_id_seq OWNER TO postgres;

--
-- Name: circuit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE circuit_id_seq OWNED BY circuit.id;


--
-- Name: communication_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE communication_interface (
    type character varying,
    id integer NOT NULL,
    name character varying,
    provider character varying,
    location character varying,
    phone character varying
);


ALTER TABLE public.communication_interface OWNER TO postgres;

--
-- Name: communication_interface_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE communication_interface_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.communication_interface_id_seq OWNER TO postgres;

--
-- Name: communication_interface_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE communication_interface_id_seq OWNED BY communication_interface.id;


--
-- Name: cping; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE cping (
    id integer NOT NULL
);


ALTER TABLE public.cping OWNER TO postgres;

--
-- Name: groups; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE groups (
    id integer NOT NULL,
    name character varying(100)
);


ALTER TABLE public.groups OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.groups_id_seq OWNER TO postgres;

--
-- Name: groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE groups_id_seq OWNED BY groups.id;


--
-- Name: incoming_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE incoming_message (
    id integer NOT NULL,
    text character varying,
    communication_interface_id integer
);


ALTER TABLE public.incoming_message OWNER TO postgres;

--
-- Name: job_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE job_message (
    id integer NOT NULL,
    job_id integer,
    incoming character varying(100),
    text character varying(100)
);


ALTER TABLE public.job_message OWNER TO postgres;

--
-- Name: jobs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE jobs (
    id integer NOT NULL,
    type character varying(50),
    uuid character varying,
    state boolean,
    circuit_id integer,
    start timestamp without time zone,
    "end" timestamp without time zone
);


ALTER TABLE public.jobs OWNER TO postgres;

--
-- Name: jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.jobs_id_seq OWNER TO postgres;

--
-- Name: jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE jobs_id_seq OWNED BY jobs.id;


--
-- Name: kannel_incoming__message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_incoming__message (
    id integer NOT NULL,
    text character varying
);


ALTER TABLE public.kannel_incoming__message OWNER TO postgres;

--
-- Name: kannel_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_interface (
    id integer NOT NULL,
    host character varying,
    port integer,
    username character varying,
    password character varying
);


ALTER TABLE public.kannel_interface OWNER TO postgres;

--
-- Name: kannel_job_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_job_message (
    id integer NOT NULL,
    job_id integer,
    incoming character varying,
    text character varying
);


ALTER TABLE public.kannel_job_message OWNER TO postgres;

--
-- Name: kannel_outgoing_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE kannel_outgoing_message (
    id integer NOT NULL,
    text character varying,
    incoming character varying
);


ALTER TABLE public.kannel_outgoing_message OWNER TO postgres;

--
-- Name: log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE log (
    id integer NOT NULL,
    date timestamp without time zone,
    uuid character varying,
    type character varying(50),
    circuit_id integer
);


ALTER TABLE public.log OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.log_id_seq OWNER TO postgres;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE log_id_seq OWNED BY log.id;


--
-- Name: message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE message (
    type character varying(50),
    id integer NOT NULL,
    date timestamp without time zone,
    sent boolean,
    number character varying,
    uuid character varying
);


ALTER TABLE public.message OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.message_id_seq OWNER TO postgres;

--
-- Name: message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE message_id_seq OWNED BY message.id;


--
-- Name: meter; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meter (
    id integer NOT NULL,
    uuid character varying,
    phone character varying,
    name character varying,
    location character varying,
    status boolean,
    date timestamp without time zone,
    battery integer,
    panel_capacity integer,
    communication character varying,
    slug character varying(100),
    communication_interface_id integer,
    geometry text
);


ALTER TABLE public.meter OWNER TO postgres;

--
-- Name: meter_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_id_seq OWNER TO postgres;

--
-- Name: meter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meter_id_seq OWNED BY meter.id;


--
-- Name: meter_messages; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meter_messages (
    id integer NOT NULL,
    message_id integer,
    meter_id integer
);


ALTER TABLE public.meter_messages OWNER TO postgres;

--
-- Name: meter_messages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meter_messages_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meter_messages_id_seq OWNER TO postgres;

--
-- Name: meter_messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meter_messages_id_seq OWNED BY meter_messages.id;


--
-- Name: meterchangeset; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meterchangeset (
    id integer NOT NULL,
    date timestamp without time zone,
    meter integer,
    meterconfigkey integer,
    value character varying
);


ALTER TABLE public.meterchangeset OWNER TO postgres;

--
-- Name: meterchangeset_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meterchangeset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meterchangeset_id_seq OWNER TO postgres;

--
-- Name: meterchangeset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meterchangeset_id_seq OWNED BY meterchangeset.id;


--
-- Name: meterconfigkey; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE meterconfigkey (
    id integer NOT NULL,
    key character varying
);


ALTER TABLE public.meterconfigkey OWNER TO postgres;

--
-- Name: meterconfigkey_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE meterconfigkey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.meterconfigkey_id_seq OWNER TO postgres;

--
-- Name: meterconfigkey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE meterconfigkey_id_seq OWNED BY meterconfigkey.id;


--
-- Name: mping; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE mping (
    id integer NOT NULL
);


ALTER TABLE public.mping OWNER TO postgres;

--
-- Name: netbook_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE netbook_interface (
    id integer NOT NULL
);


ALTER TABLE public.netbook_interface OWNER TO postgres;

--
-- Name: outgoing_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE outgoing_message (
    id integer NOT NULL,
    text character varying,
    incoming character varying
);


ALTER TABLE public.outgoing_message OWNER TO postgres;

--
-- Name: primary_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE primary_log (
    id integer NOT NULL,
    watthours double precision,
    use_time double precision,
    created timestamp without time zone,
    credit double precision,
    status integer
);


ALTER TABLE public.primary_log OWNER TO postgres;

--
-- Name: system_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE system_log (
    id integer NOT NULL,
    uuid character varying,
    text character varying,
    created character varying
);


ALTER TABLE public.system_log OWNER TO postgres;

--
-- Name: system_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE system_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.system_log_id_seq OWNER TO postgres;

--
-- Name: system_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE system_log_id_seq OWNED BY system_log.id;


--
-- Name: test_message; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_message (
    id integer NOT NULL,
    date timestamp without time zone,
    text character varying
);


ALTER TABLE public.test_message OWNER TO postgres;

--
-- Name: test_message_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE test_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_message_id_seq OWNER TO postgres;

--
-- Name: test_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE test_message_id_seq OWNED BY test_message.id;


--
-- Name: token; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE token (
    id integer NOT NULL,
    created timestamp without time zone,
    token numeric,
    value numeric,
    state character varying,
    batch_id integer
);


ALTER TABLE public.token OWNER TO postgres;

--
-- Name: token_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE token_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.token_id_seq OWNER TO postgres;

--
-- Name: token_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE token_id_seq OWNED BY token.id;


--
-- Name: tokenbatch; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tokenbatch (
    id integer NOT NULL,
    uuid character varying,
    created timestamp without time zone
);


ALTER TABLE public.tokenbatch OWNER TO postgres;

--
-- Name: tokenbatch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tokenbatch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tokenbatch_id_seq OWNER TO postgres;

--
-- Name: tokenbatch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tokenbatch_id_seq OWNED BY tokenbatch.id;


--
-- Name: turnoff; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE turnoff (
    id integer NOT NULL
);


ALTER TABLE public.turnoff OWNER TO postgres;

--
-- Name: turnon; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE turnon (
    id integer NOT NULL
);


ALTER TABLE public.turnon OWNER TO postgres;

--
-- Name: twilio_interface; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE twilio_interface (
    id integer NOT NULL,
    host character varying,
    account_id character varying,
    token character varying,
    api_version character varying
);


ALTER TABLE public.twilio_interface OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    name character varying(100),
    password character varying(100),
    email character varying(100),
    group_id integer,
    notify boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE account ALTER COLUMN id SET DEFAULT nextval('account_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE alert ALTER COLUMN id SET DEFAULT nextval('alert_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE circuit ALTER COLUMN id SET DEFAULT nextval('circuit_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE communication_interface ALTER COLUMN id SET DEFAULT nextval('communication_interface_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE groups ALTER COLUMN id SET DEFAULT nextval('groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE jobs ALTER COLUMN id SET DEFAULT nextval('jobs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE message ALTER COLUMN id SET DEFAULT nextval('message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meter ALTER COLUMN id SET DEFAULT nextval('meter_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meter_messages ALTER COLUMN id SET DEFAULT nextval('meter_messages_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meterchangeset ALTER COLUMN id SET DEFAULT nextval('meterchangeset_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE meterconfigkey ALTER COLUMN id SET DEFAULT nextval('meterconfigkey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE system_log ALTER COLUMN id SET DEFAULT nextval('system_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE test_message ALTER COLUMN id SET DEFAULT nextval('test_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE token ALTER COLUMN id SET DEFAULT nextval('token_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE tokenbatch ALTER COLUMN id SET DEFAULT nextval('tokenbatch_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: account_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY account
    ADD CONSTRAINT account_pkey PRIMARY KEY (id);


--
-- Name: addcredit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY addcredit
    ADD CONSTRAINT addcredit_pkey PRIMARY KEY (id);


--
-- Name: airtel_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY airtel_interface
    ADD CONSTRAINT airtel_interface_pkey PRIMARY KEY (id);


--
-- Name: alert_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_pkey PRIMARY KEY (id);


--
-- Name: circuit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_pkey PRIMARY KEY (id);


--
-- Name: communication_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY communication_interface
    ADD CONSTRAINT communication_interface_pkey PRIMARY KEY (id);


--
-- Name: cping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY cping
    ADD CONSTRAINT cping_pkey PRIMARY KEY (id);


--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: incoming_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY incoming_message
    ADD CONSTRAINT incoming_message_pkey PRIMARY KEY (id);


--
-- Name: job_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_pkey PRIMARY KEY (id);


--
-- Name: jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY jobs
    ADD CONSTRAINT jobs_pkey PRIMARY KEY (id);


--
-- Name: kannel_incoming__message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_incoming__message
    ADD CONSTRAINT kannel_incoming__message_pkey PRIMARY KEY (id);


--
-- Name: kannel_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_interface
    ADD CONSTRAINT kannel_interface_pkey PRIMARY KEY (id);


--
-- Name: kannel_job_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_pkey PRIMARY KEY (id);


--
-- Name: kannel_outgoing_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY kannel_outgoing_message
    ADD CONSTRAINT kannel_outgoing_message_pkey PRIMARY KEY (id);


--
-- Name: log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY message
    ADD CONSTRAINT message_pkey PRIMARY KEY (id);


--
-- Name: meter_messages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_pkey PRIMARY KEY (id);


--
-- Name: meter_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meter
    ADD CONSTRAINT meter_pkey PRIMARY KEY (id);


--
-- Name: meterchangeset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_pkey PRIMARY KEY (id);


--
-- Name: meterconfigkey_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY meterconfigkey
    ADD CONSTRAINT meterconfigkey_pkey PRIMARY KEY (id);


--
-- Name: mping_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY mping
    ADD CONSTRAINT mping_pkey PRIMARY KEY (id);


--
-- Name: netbook_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY netbook_interface
    ADD CONSTRAINT netbook_interface_pkey PRIMARY KEY (id);


--
-- Name: outgoing_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY outgoing_message
    ADD CONSTRAINT outgoing_message_pkey PRIMARY KEY (id);


--
-- Name: primary_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY primary_log
    ADD CONSTRAINT primary_log_pkey PRIMARY KEY (id);


--
-- Name: system_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY system_log
    ADD CONSTRAINT system_log_pkey PRIMARY KEY (id);


--
-- Name: test_message_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_message
    ADD CONSTRAINT test_message_pkey PRIMARY KEY (id);


--
-- Name: token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: tokenbatch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tokenbatch
    ADD CONSTRAINT tokenbatch_pkey PRIMARY KEY (id);


--
-- Name: turnoff_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY turnoff
    ADD CONSTRAINT turnoff_pkey PRIMARY KEY (id);


--
-- Name: turnon_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY turnon
    ADD CONSTRAINT turnon_pkey PRIMARY KEY (id);


--
-- Name: twilio_interface_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY twilio_interface
    ADD CONSTRAINT twilio_interface_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: addcredit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY addcredit
    ADD CONSTRAINT addcredit_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: airtel_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY airtel_interface
    ADD CONSTRAINT airtel_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: alert_circuit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_circuit_id_fkey FOREIGN KEY (circuit_id) REFERENCES circuit(id);


--
-- Name: alert_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY alert
    ADD CONSTRAINT alert_message_id_fkey FOREIGN KEY (message_id) REFERENCES message(id);


--
-- Name: circuit_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_account_id_fkey FOREIGN KEY (account_id) REFERENCES account(id);


--
-- Name: circuit_meter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY circuit
    ADD CONSTRAINT circuit_meter_fkey FOREIGN KEY (meter) REFERENCES meter(id);


--
-- Name: cping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY cping
    ADD CONSTRAINT cping_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: incoming_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY incoming_message
    ADD CONSTRAINT incoming_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: job_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: job_message_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY job_message
    ADD CONSTRAINT job_message_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(id);


--
-- Name: kannel_incoming__message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_incoming__message
    ADD CONSTRAINT kannel_incoming__message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: kannel_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_interface
    ADD CONSTRAINT kannel_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: kannel_job_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: kannel_job_message_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_job_message
    ADD CONSTRAINT kannel_job_message_job_id_fkey FOREIGN KEY (job_id) REFERENCES jobs(id);


--
-- Name: kannel_outgoing_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY kannel_outgoing_message
    ADD CONSTRAINT kannel_outgoing_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: meter_messages_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_message_id_fkey FOREIGN KEY (message_id) REFERENCES message(id);


--
-- Name: meter_messages_meter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meter_messages
    ADD CONSTRAINT meter_messages_meter_id_fkey FOREIGN KEY (meter_id) REFERENCES meter(id);


--
-- Name: meterchangeset_meter_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_meter_fkey FOREIGN KEY (meter) REFERENCES meter(id);


--
-- Name: meterchangeset_meterconfigkey_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY meterchangeset
    ADD CONSTRAINT meterchangeset_meterconfigkey_fkey FOREIGN KEY (meterconfigkey) REFERENCES meterconfigkey(id);


--
-- Name: mping_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mping
    ADD CONSTRAINT mping_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: netbook_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY netbook_interface
    ADD CONSTRAINT netbook_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: outgoing_message_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY outgoing_message
    ADD CONSTRAINT outgoing_message_id_fkey FOREIGN KEY (id) REFERENCES message(id);


--
-- Name: primary_log_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY primary_log
    ADD CONSTRAINT primary_log_id_fkey FOREIGN KEY (id) REFERENCES log(id);


--
-- Name: token_batch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES tokenbatch(id);


--
-- Name: turnoff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY turnoff
    ADD CONSTRAINT turnoff_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: turnon_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY turnon
    ADD CONSTRAINT turnon_id_fkey FOREIGN KEY (id) REFERENCES jobs(id);


--
-- Name: twilio_interface_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY twilio_interface
    ADD CONSTRAINT twilio_interface_id_fkey FOREIGN KEY (id) REFERENCES communication_interface(id);


--
-- Name: users_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_group_id_fkey FOREIGN KEY (group_id) REFERENCES groups(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

