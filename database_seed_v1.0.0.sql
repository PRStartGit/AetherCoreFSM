--
-- PostgreSQL database dump
--

\restrict mvWt3qiycOLHTKf5iM78spRUZ3gGPTlWgLdmpNwoPhufn4scTcS4zgpoQKrBaii

-- Dumped from database version 16.11
-- Dumped by pg_dump version 16.11

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

ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_organization_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_sites DROP CONSTRAINT IF EXISTS user_sites_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.user_sites DROP CONSTRAINT IF EXISTS user_sites_site_id_fkey;
ALTER TABLE IF EXISTS ONLY public.tasks DROP CONSTRAINT IF EXISTS tasks_category_id_fkey;
ALTER TABLE IF EXISTS ONLY public.task_fields DROP CONSTRAINT IF EXISTS task_fields_task_id_fkey;
ALTER TABLE IF EXISTS ONLY public.task_field_responses DROP CONSTRAINT IF EXISTS task_field_responses_task_field_id_fkey;
ALTER TABLE IF EXISTS ONLY public.task_field_responses DROP CONSTRAINT IF EXISTS task_field_responses_completed_by_fkey;
ALTER TABLE IF EXISTS ONLY public.task_field_responses DROP CONSTRAINT IF EXISTS task_field_responses_checklist_item_id_fkey;
ALTER TABLE IF EXISTS ONLY public.task_field_responses DROP CONSTRAINT IF EXISTS task_field_responses_auto_defect_id_fkey;
ALTER TABLE IF EXISTS ONLY public.sites DROP CONSTRAINT IF EXISTS sites_organization_id_fkey;
ALTER TABLE IF EXISTS ONLY public.site_tasks DROP CONSTRAINT IF EXISTS site_tasks_task_id_fkey;
ALTER TABLE IF EXISTS ONLY public.site_tasks DROP CONSTRAINT IF EXISTS site_tasks_site_id_fkey;
ALTER TABLE IF EXISTS ONLY public.password_reset_tokens DROP CONSTRAINT IF EXISTS password_reset_tokens_user_id_fkey;
ALTER TABLE IF EXISTS ONLY public.organization_modules DROP CONSTRAINT IF EXISTS organization_modules_organization_id_fkey;
ALTER TABLE IF EXISTS ONLY public.defects DROP CONSTRAINT IF EXISTS defects_site_id_fkey;
ALTER TABLE IF EXISTS ONLY public.defects DROP CONSTRAINT IF EXISTS defects_reported_by_id_fkey;
ALTER TABLE IF EXISTS ONLY public.defects DROP CONSTRAINT IF EXISTS defects_closed_by_id_fkey;
ALTER TABLE IF EXISTS ONLY public.defects DROP CONSTRAINT IF EXISTS defects_checklist_item_id_fkey;
ALTER TABLE IF EXISTS ONLY public.checklists DROP CONSTRAINT IF EXISTS checklists_site_id_fkey;
ALTER TABLE IF EXISTS ONLY public.checklists DROP CONSTRAINT IF EXISTS checklists_completed_by_id_fkey;
ALTER TABLE IF EXISTS ONLY public.checklists DROP CONSTRAINT IF EXISTS checklists_category_id_fkey;
ALTER TABLE IF EXISTS ONLY public.checklist_items DROP CONSTRAINT IF EXISTS checklist_items_task_id_fkey;
ALTER TABLE IF EXISTS ONLY public.checklist_items DROP CONSTRAINT IF EXISTS checklist_items_checklist_id_fkey;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_organization_id_fkey;
DROP INDEX IF EXISTS public.ix_users_id;
DROP INDEX IF EXISTS public.ix_users_email;
DROP INDEX IF EXISTS public.ix_user_sites_id;
DROP INDEX IF EXISTS public.ix_tasks_id;
DROP INDEX IF EXISTS public.ix_task_fields_task_id;
DROP INDEX IF EXISTS public.ix_task_fields_id;
DROP INDEX IF EXISTS public.ix_task_field_responses_id;
DROP INDEX IF EXISTS public.ix_task_field_responses_checklist_item_id;
DROP INDEX IF EXISTS public.ix_sites_id;
DROP INDEX IF EXISTS public.ix_site_tasks_id;
DROP INDEX IF EXISTS public.ix_password_reset_tokens_token;
DROP INDEX IF EXISTS public.ix_password_reset_tokens_id;
DROP INDEX IF EXISTS public.ix_organizations_org_id;
DROP INDEX IF EXISTS public.ix_organizations_id;
DROP INDEX IF EXISTS public.ix_organization_modules_id;
DROP INDEX IF EXISTS public.ix_defects_id;
DROP INDEX IF EXISTS public.ix_checklists_id;
DROP INDEX IF EXISTS public.ix_checklist_items_id;
DROP INDEX IF EXISTS public.ix_categories_id;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS users_pkey;
ALTER TABLE IF EXISTS ONLY public.user_sites DROP CONSTRAINT IF EXISTS user_sites_pkey;
ALTER TABLE IF EXISTS ONLY public.tasks DROP CONSTRAINT IF EXISTS tasks_pkey;
ALTER TABLE IF EXISTS ONLY public.task_fields DROP CONSTRAINT IF EXISTS task_fields_pkey;
ALTER TABLE IF EXISTS ONLY public.task_field_responses DROP CONSTRAINT IF EXISTS task_field_responses_pkey;
ALTER TABLE IF EXISTS ONLY public.sites DROP CONSTRAINT IF EXISTS sites_pkey;
ALTER TABLE IF EXISTS ONLY public.site_tasks DROP CONSTRAINT IF EXISTS site_tasks_pkey;
ALTER TABLE IF EXISTS ONLY public.promotions DROP CONSTRAINT IF EXISTS promotions_pkey;
ALTER TABLE IF EXISTS ONLY public.password_reset_tokens DROP CONSTRAINT IF EXISTS password_reset_tokens_pkey;
ALTER TABLE IF EXISTS ONLY public.organizations DROP CONSTRAINT IF EXISTS organizations_pkey;
ALTER TABLE IF EXISTS ONLY public.organization_modules DROP CONSTRAINT IF EXISTS organization_modules_pkey;
ALTER TABLE IF EXISTS ONLY public.defects DROP CONSTRAINT IF EXISTS defects_pkey;
ALTER TABLE IF EXISTS ONLY public.checklists DROP CONSTRAINT IF EXISTS checklists_pkey;
ALTER TABLE IF EXISTS ONLY public.checklist_items DROP CONSTRAINT IF EXISTS checklist_items_pkey;
ALTER TABLE IF EXISTS ONLY public.categories DROP CONSTRAINT IF EXISTS categories_pkey;
ALTER TABLE IF EXISTS public.users ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.user_sites ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.tasks ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.task_fields ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.task_field_responses ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.sites ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.site_tasks ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.promotions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.password_reset_tokens ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organizations ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.organization_modules ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.defects ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.checklists ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.checklist_items ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.categories ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.users_id_seq;
DROP TABLE IF EXISTS public.users;
DROP SEQUENCE IF EXISTS public.user_sites_id_seq;
DROP TABLE IF EXISTS public.user_sites;
DROP SEQUENCE IF EXISTS public.tasks_id_seq;
DROP TABLE IF EXISTS public.tasks;
DROP SEQUENCE IF EXISTS public.task_fields_id_seq;
DROP TABLE IF EXISTS public.task_fields;
DROP SEQUENCE IF EXISTS public.task_field_responses_id_seq;
DROP TABLE IF EXISTS public.task_field_responses;
DROP SEQUENCE IF EXISTS public.sites_id_seq;
DROP TABLE IF EXISTS public.sites;
DROP SEQUENCE IF EXISTS public.site_tasks_id_seq;
DROP TABLE IF EXISTS public.site_tasks;
DROP SEQUENCE IF EXISTS public.promotions_id_seq;
DROP TABLE IF EXISTS public.promotions;
DROP SEQUENCE IF EXISTS public.password_reset_tokens_id_seq;
DROP TABLE IF EXISTS public.password_reset_tokens;
DROP SEQUENCE IF EXISTS public.organizations_id_seq;
DROP TABLE IF EXISTS public.organizations;
DROP SEQUENCE IF EXISTS public.organization_modules_id_seq;
DROP TABLE IF EXISTS public.organization_modules;
DROP SEQUENCE IF EXISTS public.defects_id_seq;
DROP TABLE IF EXISTS public.defects;
DROP SEQUENCE IF EXISTS public.checklists_id_seq;
DROP TABLE IF EXISTS public.checklists;
DROP SEQUENCE IF EXISTS public.checklist_items_id_seq;
DROP TABLE IF EXISTS public.checklist_items;
DROP SEQUENCE IF EXISTS public.categories_id_seq;
DROP TABLE IF EXISTS public.categories;
DROP TYPE IF EXISTS public.userrole;
DROP TYPE IF EXISTS public.jobtitle;
DROP TYPE IF EXISTS public.department;
DROP TYPE IF EXISTS public.defectstatus;
DROP TYPE IF EXISTS public.defectseverity;
DROP TYPE IF EXISTS public.checkliststatus;
DROP TYPE IF EXISTS public.checklistfrequency;
--
-- Name: checklistfrequency; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.checklistfrequency AS ENUM (
    'DAILY',
    'WEEKLY',
    'MONTHLY',
    'SIX_MONTHLY',
    'YEARLY',
    'quarterly',
    'every_2_hours',
    'per_batch',
    'per_delivery',
    'continuous',
    'as_needed',
    'QUARTERLY'
);


ALTER TYPE public.checklistfrequency OWNER TO postgres;

--
-- Name: checkliststatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.checkliststatus AS ENUM (
    'PENDING',
    'IN_PROGRESS',
    'COMPLETED',
    'OVERDUE'
);


ALTER TYPE public.checkliststatus OWNER TO postgres;

--
-- Name: defectseverity; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.defectseverity AS ENUM (
    'CRITICAL',
    'HIGH',
    'MEDIUM',
    'LOW'
);


ALTER TYPE public.defectseverity OWNER TO postgres;

--
-- Name: defectstatus; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.defectstatus AS ENUM (
    'OPEN',
    'CLOSED'
);


ALTER TYPE public.defectstatus OWNER TO postgres;

--
-- Name: department; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.department AS ENUM (
    'management',
    'boh',
    'foh'
);


ALTER TYPE public.department OWNER TO postgres;

--
-- Name: jobtitle; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.jobtitle AS ENUM (
    'general_manager',
    'assistant_manager',
    'head_chef',
    'sous_chef',
    'supervisor',
    'team_member'
);


ALTER TYPE public.jobtitle OWNER TO postgres;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.userrole AS ENUM (
    'SUPER_ADMIN',
    'ORG_ADMIN',
    'SITE_USER'
);


ALTER TYPE public.userrole OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying,
    is_active boolean,
    frequency public.checklistfrequency NOT NULL,
    closes_at time without time zone,
    is_global boolean,
    organization_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    icon character varying,
    opens_at time without time zone
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: checklist_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checklist_items (
    id integer NOT NULL,
    item_name character varying NOT NULL,
    is_completed boolean,
    notes text,
    item_data json,
    photo_url character varying,
    checklist_id integer NOT NULL,
    task_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.checklist_items OWNER TO postgres;

--
-- Name: checklist_items_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.checklist_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.checklist_items_id_seq OWNER TO postgres;

--
-- Name: checklist_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.checklist_items_id_seq OWNED BY public.checklist_items.id;


--
-- Name: checklists; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checklists (
    id integer NOT NULL,
    checklist_date date NOT NULL,
    status public.checkliststatus,
    category_id integer NOT NULL,
    site_id integer NOT NULL,
    completed_by_id integer,
    total_items integer,
    completed_items integer,
    completion_percentage integer,
    created_at timestamp with time zone DEFAULT now(),
    completed_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.checklists OWNER TO postgres;

--
-- Name: checklists_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.checklists_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.checklists_id_seq OWNER TO postgres;

--
-- Name: checklists_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.checklists_id_seq OWNED BY public.checklists.id;


--
-- Name: defects; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.defects (
    id integer NOT NULL,
    title character varying NOT NULL,
    description text,
    severity public.defectseverity NOT NULL,
    status public.defectstatus,
    photo_url character varying,
    site_id integer NOT NULL,
    checklist_item_id integer,
    reported_by_id integer NOT NULL,
    closed_by_id integer,
    created_at timestamp with time zone DEFAULT now(),
    closed_at timestamp with time zone,
    updated_at timestamp with time zone
);


ALTER TABLE public.defects OWNER TO postgres;

--
-- Name: defects_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.defects_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.defects_id_seq OWNER TO postgres;

--
-- Name: defects_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.defects_id_seq OWNED BY public.defects.id;


--
-- Name: organization_modules; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organization_modules (
    id integer NOT NULL,
    module_name character varying NOT NULL,
    is_enabled boolean,
    organization_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.organization_modules OWNER TO postgres;

--
-- Name: organization_modules_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organization_modules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organization_modules_id_seq OWNER TO postgres;

--
-- Name: organization_modules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organization_modules_id_seq OWNED BY public.organization_modules.id;


--
-- Name: organizations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.organizations (
    id integer NOT NULL,
    name character varying NOT NULL,
    org_id character varying NOT NULL,
    is_active boolean,
    contact_person character varying,
    contact_email character varying,
    contact_phone character varying,
    address text,
    subscription_tier character varying,
    custom_price_per_site double precision,
    subscription_start_date timestamp with time zone,
    subscription_end_date timestamp with time zone,
    is_trial boolean,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.organizations OWNER TO postgres;

--
-- Name: organizations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.organizations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.organizations_id_seq OWNER TO postgres;

--
-- Name: organizations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.organizations_id_seq OWNED BY public.organizations.id;


--
-- Name: password_reset_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.password_reset_tokens (
    id integer NOT NULL,
    token character varying NOT NULL,
    user_id integer NOT NULL,
    expires_at timestamp with time zone NOT NULL,
    used integer,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.password_reset_tokens OWNER TO postgres;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.password_reset_tokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.password_reset_tokens_id_seq OWNER TO postgres;

--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.password_reset_tokens_id_seq OWNED BY public.password_reset_tokens.id;


--
-- Name: promotions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.promotions (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    trial_days integer DEFAULT 30 NOT NULL,
    is_active boolean DEFAULT false,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone,
    start_date timestamp with time zone,
    end_date timestamp with time zone
);


ALTER TABLE public.promotions OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.promotions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.promotions_id_seq OWNER TO postgres;

--
-- Name: promotions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.promotions_id_seq OWNED BY public.promotions.id;


--
-- Name: site_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.site_tasks (
    id integer NOT NULL,
    site_id integer NOT NULL,
    task_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.site_tasks OWNER TO postgres;

--
-- Name: site_tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.site_tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.site_tasks_id_seq OWNER TO postgres;

--
-- Name: site_tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.site_tasks_id_seq OWNED BY public.site_tasks.id;


--
-- Name: sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sites (
    id integer NOT NULL,
    name character varying NOT NULL,
    site_code character varying,
    is_active boolean,
    address text,
    city character varying,
    postcode character varying,
    country character varying,
    organization_id integer NOT NULL,
    daily_report_enabled boolean,
    daily_report_time character varying,
    weekly_report_enabled boolean,
    weekly_report_day integer,
    weekly_report_time character varying,
    report_recipients text,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.sites OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sites_id_seq OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sites_id_seq OWNED BY public.sites.id;


--
-- Name: task_field_responses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_field_responses (
    id integer NOT NULL,
    checklist_item_id integer NOT NULL,
    task_field_id integer NOT NULL,
    text_value text,
    number_value double precision,
    boolean_value boolean,
    json_value json,
    file_url text,
    auto_defect_id integer,
    completed_at timestamp with time zone DEFAULT now(),
    completed_by integer
);


ALTER TABLE public.task_field_responses OWNER TO postgres;

--
-- Name: task_field_responses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_field_responses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_field_responses_id_seq OWNER TO postgres;

--
-- Name: task_field_responses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_field_responses_id_seq OWNED BY public.task_field_responses.id;


--
-- Name: task_fields; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_fields (
    id integer NOT NULL,
    task_id integer NOT NULL,
    field_type character varying(50) NOT NULL,
    field_label character varying(255) NOT NULL,
    field_order integer NOT NULL,
    is_required boolean,
    validation_rules json,
    options json,
    show_if json,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.task_fields OWNER TO postgres;

--
-- Name: task_fields_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_fields_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_fields_id_seq OWNER TO postgres;

--
-- Name: task_fields_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_fields_id_seq OWNED BY public.task_fields.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tasks (
    id integer NOT NULL,
    name character varying NOT NULL,
    description text,
    is_active boolean,
    order_index integer,
    form_config json,
    has_dynamic_form boolean,
    category_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    allocated_departments character varying[],
    priority character varying DEFAULT 'medium'::character varying
);


ALTER TABLE public.tasks OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tasks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tasks_id_seq OWNER TO postgres;

--
-- Name: tasks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tasks_id_seq OWNED BY public.tasks.id;


--
-- Name: user_sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sites (
    id integer NOT NULL,
    user_id integer NOT NULL,
    site_id integer NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.user_sites OWNER TO postgres;

--
-- Name: user_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_sites_id_seq OWNER TO postgres;

--
-- Name: user_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_sites_id_seq OWNED BY public.user_sites.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying NOT NULL,
    hashed_password character varying NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean,
    phone character varying,
    organization_id integer,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone,
    department public.department,
    job_title public.jobtitle,
    must_change_password boolean DEFAULT false
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Name: checklist_items id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklist_items ALTER COLUMN id SET DEFAULT nextval('public.checklist_items_id_seq'::regclass);


--
-- Name: checklists id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklists ALTER COLUMN id SET DEFAULT nextval('public.checklists_id_seq'::regclass);


--
-- Name: defects id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects ALTER COLUMN id SET DEFAULT nextval('public.defects_id_seq'::regclass);


--
-- Name: organization_modules id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_modules ALTER COLUMN id SET DEFAULT nextval('public.organization_modules_id_seq'::regclass);


--
-- Name: organizations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations ALTER COLUMN id SET DEFAULT nextval('public.organizations_id_seq'::regclass);


--
-- Name: password_reset_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens ALTER COLUMN id SET DEFAULT nextval('public.password_reset_tokens_id_seq'::regclass);


--
-- Name: promotions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions ALTER COLUMN id SET DEFAULT nextval('public.promotions_id_seq'::regclass);


--
-- Name: site_tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_tasks ALTER COLUMN id SET DEFAULT nextval('public.site_tasks_id_seq'::regclass);


--
-- Name: sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites ALTER COLUMN id SET DEFAULT nextval('public.sites_id_seq'::regclass);


--
-- Name: task_field_responses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses ALTER COLUMN id SET DEFAULT nextval('public.task_field_responses_id_seq'::regclass);


--
-- Name: task_fields id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_fields ALTER COLUMN id SET DEFAULT nextval('public.task_fields_id_seq'::regclass);


--
-- Name: tasks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks ALTER COLUMN id SET DEFAULT nextval('public.tasks_id_seq'::regclass);


--
-- Name: user_sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sites ALTER COLUMN id SET DEFAULT nextval('public.user_sites_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name, description, is_active, frequency, closes_at, is_global, organization_id, created_at, updated_at, icon, opens_at) FROM stdin;
4	Cleaning & Hygiene	Cleaning schedules and hygiene monitoring	t	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🧼	\N
5	Deliveries & Stock Checks	Supplier checks and stock rotation	t	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	\N	📦	\N
6	Pest Control	Pest monitoring and prevention	t	DAILY	09:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🐀	\N
7	Staff Hygiene & Training	Staff hygiene monitoring and training records	t	DAILY	09:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	👨‍🍳	\N
8	Cooking & Preparation	Food preparation and cooking controls	t	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🍳	\N
9	Equipment Maintenance	Equipment checks and servicing	t	WEEKLY	17:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🔧	\N
10	Licensing & Compliance	License checks and legal compliance	t	MONTHLY	17:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	📜	\N
11	Allergen Management	Allergen controls and documentation	t	DAILY	10:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	⚠️	\N
12	Waste Management	Waste disposal and recycling	t	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🗑️	\N
13	Fire Safety	Fire prevention and safety checks	t	DAILY	09:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	🔥	\N
14	Water Safety	Water temperature and legionella control	t	WEEKLY	17:00:00	t	\N	2025-11-17 20:24:29.66744+00	\N	💧	\N
1	Temperature Monitoring	Daily monitoring of fridge, freezer, and hot holding temperatures	f	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	2025-11-18 12:33:57.401993+00	🌡️	\N
2	Opening Checks	Daily opening procedures and safety checks	t	DAILY	12:00:00	t	\N	2025-11-17 20:24:29.66744+00	2025-11-18 12:33:57.41385+00	🔓	08:00:00
3	Closing Checks	End of day procedures and security	t	DAILY	23:59:00	t	\N	2025-11-17 20:24:29.66744+00	2025-11-18 12:33:57.41385+00	🔒	17:00:00
20	AM Temperature Monitoring	Morning temperature checks for fridges and freezers	t	DAILY	12:00:00	t	\N	2025-11-18 12:43:01.317348+00	\N	🌡️	08:00:00
21	PM Temperature Monitoring	Evening temperature checks for fridges	t	DAILY	23:59:00	t	\N	2025-11-18 12:43:01.317348+00	\N	🌡️	17:00:00
22	Opening Checks	Daily opening procedures and safety checks	t	DAILY	12:00:00	t	\N	2025-11-18 12:43:01.317348+00	\N	🔓	08:00:00
23	Closing Checks	End of day procedures and security	t	DAILY	23:59:00	t	\N	2025-11-18 12:43:01.317348+00	\N	🔒	17:00:00
15	AM Temperature Checks	Morning temperature monitoring (fridge & freezer)	f	DAILY	12:00:00	t	\N	2025-11-18 12:15:53.602299+00	2025-11-18 12:51:19.340179+00	🌡️	00:00:00
16	PM Temperature Checks	Evening temperature monitoring (fridge & freezer)	f	DAILY	23:59:00	t	\N	2025-11-18 12:15:53.602299+00	2025-11-18 12:51:19.340179+00	🌡️	17:00:00
17	Temperature Monitoring	Daily monitoring of fridge, freezer, and hot holding temperatures	f	DAILY	\N	t	\N	2025-11-18 12:33:57.41385+00	2025-11-18 12:51:19.340179+00	🌡️	\N
110	Food Safety Management System (HACCP)	HACCP-based food safety management procedures and documentation	t	MONTHLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
111	Temperature Control (AM)	Morning temperature checks for all refrigeration, freezer, and cooking equipment	t	DAILY	12:00:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	08:00:00
113	Personal Hygiene	Staff hygiene compliance and hand washing procedures	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
114	Cleaning and Disinfection	Kitchen cleaning schedules and sanitization procedures	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
115	Pest Control	Pest monitoring and prevention procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
116	Food Storage and Handling	Stock rotation, storage separation, and date checking	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
117	Cross-Contamination Prevention	Procedures to prevent cross-contamination between raw and ready-to-eat foods	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
118	Allergen Management	Allergen information and communication procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
119	Training Records	Staff training documentation and verification	t	MONTHLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
120	Equipment Maintenance	Equipment inspection and maintenance procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
121	Waste Management	Waste handling and disposal procedures	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
122	Water Supply and Drainage	Water temperature and drainage system checks	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	09:00:00
123	Structure and Facilities	Premises condition and facility integrity checks	t	MONTHLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
124	Supplier and Traceability	Supplier approval and traceability procedures	t	QUARTERLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
125	Documentation and Record Keeping	Record completion and storage procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	00:00:00
112	Temperature Control (PM)	Afternoon temperature checks for refrigeration and freezer equipment	t	DAILY	23:59:00	t	\N	2025-11-20 14:40:58.190648+00	\N	\N	17:00:00
126	Food Safety Management System (HACCP)	HACCP-based food safety management procedures and documentation	t	MONTHLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
127	Temperature Control (AM)	Morning temperature checks for all refrigeration, freezer, and cooking equipment	t	DAILY	12:00:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	08:00:00
128	Temperature Control (PM)	Afternoon temperature checks for refrigeration and freezer equipment	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	12:00:00
129	Personal Hygiene	Staff hygiene compliance and hand washing procedures	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
130	Cleaning and Disinfection	Kitchen cleaning schedules and sanitization procedures	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
131	Pest Control	Pest monitoring and prevention procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
132	Food Storage and Handling	Stock rotation, storage separation, and date checking	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
133	Cross-Contamination Prevention	Procedures to prevent cross-contamination between raw and ready-to-eat foods	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
134	Allergen Management	Allergen information and communication procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
135	Training Records	Staff training documentation and verification	t	MONTHLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
136	Equipment Maintenance	Equipment inspection and maintenance procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
137	Waste Management	Waste handling and disposal procedures	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
138	Water Supply and Drainage	Water temperature and drainage system checks	t	DAILY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	09:00:00
139	Structure and Facilities	Premises condition and facility integrity checks	t	MONTHLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
140	Supplier and Traceability	Supplier approval and traceability procedures	t	QUARTERLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
141	Documentation and Record Keeping	Record completion and storage procedures	t	WEEKLY	23:59:00	t	\N	2025-11-20 15:51:08.690777+00	\N	\N	00:00:00
\.


--
-- Data for Name: checklist_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.checklist_items (id, item_name, is_completed, notes, item_data, photo_url, checklist_id, task_id, created_at, completed_at, updated_at) FROM stdin;
1	AM Fridge Temperature Checks	f	\N	\N	\N	2	77	2025-11-20 17:29:23.326911+00	\N	\N
2	AM Freezer Temperature Checks	f	\N	\N	\N	2	78	2025-11-20 17:29:23.326911+00	\N	\N
3	Delivery Temperature Check	f	\N	\N	\N	2	79	2025-11-20 17:29:23.326911+00	\N	\N
4	PM Fridge Temperature Checks	f	\N	\N	\N	3	80	2025-11-20 17:29:23.326911+00	\N	\N
5	PM Freezer Temperature Checks	f	\N	\N	\N	3	81	2025-11-20 17:29:23.326911+00	\N	\N
6	Hand Washing Compliance Check	f	\N	\N	\N	4	82	2025-11-20 17:29:23.326911+00	\N	\N
7	Personal Hygiene Inspection	f	\N	\N	\N	4	83	2025-11-20 17:29:23.326911+00	\N	\N
8	Staff Illness Reporting Check	f	\N	\N	\N	4	84	2025-11-20 17:29:23.326911+00	\N	\N
9	Daily Kitchen Cleaning Check	f	\N	\N	\N	5	85	2025-11-20 17:29:23.326911+00	\N	\N
10	Food Contact Surfaces Sanitization	f	\N	\N	\N	5	86	2025-11-20 17:29:23.326911+00	\N	\N
11	Pest Control Device Check	f	\N	\N	\N	6	87	2025-11-20 17:29:23.326911+00	\N	\N
12	Stock Rotation Check (FIFO)	f	\N	\N	\N	7	88	2025-11-20 17:29:23.326911+00	\N	\N
13	Food Storage Separation Audit	f	\N	\N	\N	7	89	2025-11-20 17:29:23.326911+00	\N	\N
14	Color-Coded Equipment Check	f	\N	\N	\N	8	90	2025-11-20 17:29:23.326911+00	\N	\N
15	Separate Preparation Area Audit	f	\N	\N	\N	8	91	2025-11-20 17:29:23.326911+00	\N	\N
16	Allergen Information Update	f	\N	\N	\N	9	92	2025-11-20 17:29:23.326911+00	\N	\N
17	Refrigeration Equipment Check	f	\N	\N	\N	11	94	2025-11-20 17:29:23.326911+00	\N	\N
18	Waste Bin Cleaning	f	\N	\N	\N	12	95	2025-11-20 17:29:23.326911+00	\N	\N
19	Waste Storage Area Inspection	f	\N	\N	\N	12	96	2025-11-20 17:29:23.326911+00	\N	\N
20	Water Temperature Check	f	\N	\N	\N	13	97	2025-11-20 17:29:23.326911+00	\N	\N
21	Supplier Approval Review	f	\N	\N	\N	16	99	2025-11-20 17:29:23.326911+00	\N	\N
22	Daily Records Completion Check	f	\N	\N	\N	17	100	2025-11-20 17:29:23.326911+00	\N	\N
23	AM Fridge Temperature Checks	f	\N	\N	\N	19	77	2025-11-20 17:29:23.326911+00	\N	\N
24	AM Freezer Temperature Checks	f	\N	\N	\N	19	78	2025-11-20 17:29:23.326911+00	\N	\N
25	Delivery Temperature Check	f	\N	\N	\N	19	79	2025-11-20 17:29:23.326911+00	\N	\N
26	PM Fridge Temperature Checks	f	\N	\N	\N	20	80	2025-11-20 17:29:23.326911+00	\N	\N
27	PM Freezer Temperature Checks	f	\N	\N	\N	20	81	2025-11-20 17:29:23.326911+00	\N	\N
28	Hand Washing Compliance Check	f	\N	\N	\N	21	82	2025-11-20 17:29:23.326911+00	\N	\N
29	Personal Hygiene Inspection	f	\N	\N	\N	21	83	2025-11-20 17:29:23.326911+00	\N	\N
30	Staff Illness Reporting Check	f	\N	\N	\N	21	84	2025-11-20 17:29:23.326911+00	\N	\N
33	Pest Control Device Check	f	\N	\N	\N	23	87	2025-11-20 17:29:23.326911+00	\N	\N
34	Stock Rotation Check (FIFO)	f	\N	\N	\N	24	88	2025-11-20 17:29:23.326911+00	\N	\N
35	Food Storage Separation Audit	f	\N	\N	\N	24	89	2025-11-20 17:29:23.326911+00	\N	\N
36	Color-Coded Equipment Check	f	\N	\N	\N	25	90	2025-11-20 17:29:23.326911+00	\N	\N
37	Separate Preparation Area Audit	f	\N	\N	\N	25	91	2025-11-20 17:29:23.326911+00	\N	\N
38	Allergen Information Update	f	\N	\N	\N	26	92	2025-11-20 17:29:23.326911+00	\N	\N
39	Refrigeration Equipment Check	f	\N	\N	\N	28	94	2025-11-20 17:29:23.326911+00	\N	\N
40	Waste Bin Cleaning	f	\N	\N	\N	29	95	2025-11-20 17:29:23.326911+00	\N	\N
41	Waste Storage Area Inspection	f	\N	\N	\N	29	96	2025-11-20 17:29:23.326911+00	\N	\N
42	Water Temperature Check	f	\N	\N	\N	30	97	2025-11-20 17:29:23.326911+00	\N	\N
43	Supplier Approval Review	f	\N	\N	\N	33	99	2025-11-20 17:29:23.326911+00	\N	\N
44	Daily Records Completion Check	f	\N	\N	\N	34	100	2025-11-20 17:29:23.326911+00	\N	\N
45	HACCP Plan Review	f	\N	\N	\N	35	75	2025-11-20 17:29:23.326911+00	\N	\N
46	HACCP Records Verification	f	\N	\N	\N	35	76	2025-11-20 17:29:23.326911+00	\N	\N
47	HACCP Plan Review	f	\N	\N	\N	36	75	2025-11-20 17:29:23.326911+00	\N	\N
48	HACCP Records Verification	f	\N	\N	\N	36	76	2025-11-20 17:29:23.326911+00	\N	\N
49	Food Hygiene Training Verification	f	\N	\N	\N	37	93	2025-11-20 17:29:23.326911+00	\N	\N
50	Food Hygiene Training Verification	f	\N	\N	\N	38	93	2025-11-20 17:29:23.326911+00	\N	\N
51	Premises Condition Inspection	f	\N	\N	\N	39	98	2025-11-20 17:29:23.326911+00	\N	\N
52	Premises Condition Inspection	f	\N	\N	\N	40	98	2025-11-20 17:29:23.326911+00	\N	\N
31	Daily Kitchen Cleaning Check	t	\N	\N	\N	22	85	2025-11-20 17:29:23.326911+00	2025-11-20 17:35:55.095696+00	2025-11-20 17:35:55.089674+00
32	Food Contact Surfaces Sanitization	t	\N	\N	\N	22	86	2025-11-20 17:29:23.326911+00	2025-11-20 17:35:58.520976+00	2025-11-20 17:35:58.517767+00
\.


--
-- Data for Name: checklists; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.checklists (id, checklist_date, status, category_id, site_id, completed_by_id, total_items, completed_items, completion_percentage, created_at, completed_at, updated_at) FROM stdin;
1	2025-11-01	PENDING	126	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
2	2025-11-20	PENDING	127	12	\N	3	0	0	2025-11-20 16:52:17.978587+00	\N	\N
3	2025-11-20	PENDING	128	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
4	2025-11-20	PENDING	129	12	\N	3	0	0	2025-11-20 16:52:17.978587+00	\N	\N
5	2025-11-20	PENDING	130	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
6	2025-11-20	PENDING	131	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
7	2025-11-20	PENDING	132	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
8	2025-11-20	PENDING	133	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
9	2025-11-20	PENDING	134	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
10	2025-11-01	PENDING	135	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
11	2025-11-20	PENDING	136	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
12	2025-11-20	PENDING	137	12	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
13	2025-11-20	PENDING	138	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
14	2025-11-01	PENDING	139	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
15	2025-10-01	PENDING	140	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
16	2026-01-01	PENDING	140	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
17	2025-11-20	PENDING	141	12	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
18	2025-11-01	PENDING	126	11	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
19	2025-11-20	PENDING	127	11	\N	3	0	0	2025-11-20 16:52:17.978587+00	\N	\N
20	2025-11-20	PENDING	128	11	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
21	2025-11-20	PENDING	129	11	\N	3	0	0	2025-11-20 16:52:17.978587+00	\N	\N
23	2025-11-20	PENDING	131	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
24	2025-11-20	PENDING	132	11	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
25	2025-11-20	PENDING	133	11	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
26	2025-11-20	PENDING	134	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
27	2025-11-01	PENDING	135	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
28	2025-11-20	PENDING	136	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
29	2025-11-20	PENDING	137	11	\N	2	0	0	2025-11-20 16:52:17.978587+00	\N	\N
30	2025-11-20	PENDING	138	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
31	2025-11-01	PENDING	139	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
32	2025-10-01	PENDING	140	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
33	2026-01-01	PENDING	140	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
34	2025-11-20	PENDING	141	11	\N	1	0	0	2025-11-20 16:52:17.978587+00	\N	\N
36	2025-12-01	PENDING	126	12	\N	2	0	0	2025-11-20 17:19:49.221841+00	\N	\N
22	2025-11-20	COMPLETED	130	11	9	2	2	100	2025-11-20 16:52:17.978587+00	2025-11-20 17:35:58.530372+00	2025-11-20 17:35:58.517767+00
35	2025-12-01	PENDING	126	11	\N	2	0	0	2025-11-20 17:14:09.788637+00	\N	\N
37	2025-12-01	PENDING	135	11	\N	1	0	0	2025-11-20 17:20:35.40781+00	\N	\N
38	2025-12-01	PENDING	135	12	\N	1	0	0	2025-11-20 17:20:35.40781+00	\N	\N
39	2025-12-01	PENDING	139	11	\N	1	0	0	2025-11-20 17:20:35.40781+00	\N	\N
40	2025-12-01	PENDING	139	12	\N	1	0	0	2025-11-20 17:20:35.40781+00	\N	\N
\.


--
-- Data for Name: defects; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.defects (id, title, description, severity, status, photo_url, site_id, checklist_item_id, reported_by_id, closed_by_id, created_at, closed_at, updated_at) FROM stdin;
1	Freezer broken 	Xxx	MEDIUM	OPEN	\N	11	\N	9	\N	2025-11-18 15:50:36.512619+00	\N	\N
2	G`s knee is fucked 	it is 	CRITICAL	OPEN	\N	11	\N	9	\N	2025-11-19 19:25:56.45289+00	\N	\N
\.


--
-- Data for Name: organization_modules; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organization_modules (id, module_name, is_enabled, organization_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: organizations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.organizations (id, name, org_id, is_active, contact_person, contact_email, contact_phone, address, subscription_tier, custom_price_per_site, subscription_start_date, subscription_end_date, is_trial, created_at, updated_at) FROM stdin;
5	Zynthio	zyn	t	Attila Juahsz	hello@prstart.co.uk	+4407928742127	110 Izatt avenue, Dunfermline, KY113BJ	enterprise	\N	\N	\N	t	2025-11-17 17:45:45.379841+00	2025-11-17 17:49:15.116208+00
9	PRStart Consultancy	PRS	t	Attila Juhasz	dj.atesz@gmail.com	+447928742127	110, izatt avenue, Fife, Dunfermline Central, Scotland, KY11 3BJ	enterprise	\N	\N	\N	t	2025-11-17 18:51:36.642741+00	\N
10	Test Restaurant Ltd	test-rest-1763639586	t	John Doe	test1763639586@example.com	01234567890	123 Test Street, Test City	basic	\N	2025-11-20 11:53:06.183419+00	2025-12-20 11:53:06.183421+00	t	2025-11-20 11:53:06.170687+00	\N
\.


--
-- Data for Name: password_reset_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.password_reset_tokens (id, token, user_id, expires_at, used, created_at) FROM stdin;
\.


--
-- Data for Name: promotions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.promotions (id, name, description, trial_days, is_active, created_at, updated_at, start_date, end_date) FROM stdin;
1	Standard Trial	Default 30-day trial period	30	t	2025-11-19 19:08:29.459992+00	\N	\N	\N
\.


--
-- Data for Name: site_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.site_tasks (id, site_id, task_id, created_at) FROM stdin;
\.


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sites (id, name, site_code, is_active, address, city, postcode, country, organization_id, daily_report_enabled, daily_report_time, weekly_report_enabled, weekly_report_day, weekly_report_time, report_recipients, created_at, updated_at) FROM stdin;
12	Tony Macaroni Straiton	TMSTRAITON	t	21 Straiton Mains, Midlothian West	Midlothian	EH20 9PW	UK	9	f	09:00	t	1	09:00	hello@prstart.co.uk, test@example.com	2025-11-19 14:32:39.403879+00	2025-11-19 17:18:13.201343+00
11	Test site	TS	t	Dunfermline Central	Fife	KY113BJ	UK	9	t	09:00	t	1	09:00	hello@prstart.co.uk	2025-11-17 20:33:42.995882+00	2025-11-19 17:18:59.458171+00
\.


--
-- Data for Name: task_field_responses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_field_responses (id, checklist_item_id, task_field_id, text_value, number_value, boolean_value, json_value, file_url, auto_defect_id, completed_at, completed_by) FROM stdin;
271	31	223	\N	\N	t	null	\N	\N	2025-11-20 17:35:55.089674+00	9
272	31	224		\N	\N	null	\N	\N	2025-11-20 17:35:55.089674+00	9
273	32	225	\N	\N	t	null	\N	\N	2025-11-20 17:35:58.517767+00	9
\.


--
-- Data for Name: task_fields; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_fields (id, task_id, field_type, field_label, field_order, is_required, validation_rules, options, show_if, created_at, updated_at) FROM stdin;
4	2	temperature	Fridge Temperature (°C)	1	t	{"min": -5, "max": 8, "create_defect_if": "out_of_range"}	null	\N	2025-11-17 21:05:13.257619+00	\N
5	2	photo	Photo of Temperature Display	2	f	null	null	\N	2025-11-17 21:05:13.257619+00	\N
6	2	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.257619+00	\N
7	3	temperature	Freezer Temperature (°C)	1	t	{"min": -25, "max": -18, "create_defect_if": "out_of_range"}	null	\N	2025-11-17 21:05:13.268439+00	\N
8	3	photo	Photo of Temperature Display	2	f	null	null	\N	2025-11-17 21:05:13.268439+00	\N
9	3	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.268439+00	\N
14	5	yes_no	Equipment in Good Working Order?	1	t	null	null	\N	2025-11-17 21:05:13.289097+00	\N
15	5	yes_no	Any Damage Visible?	2	t	null	null	\N	2025-11-17 21:05:13.289097+00	\N
16	5	photo	Photo of Equipment	3	f	null	null	\N	2025-11-17 21:05:13.289097+00	\N
17	5	text	Issues Found	4	f	null	null	\N	2025-11-17 21:05:13.289097+00	\N
22	7	yes_no	Area Cleaned?	1	t	null	null	\N	2025-11-17 21:05:13.308231+00	\N
23	7	yes_no	Cleaning Products Used?	2	t	null	null	\N	2025-11-17 21:05:13.308231+00	\N
24	7	photo	Photo of Cleaned Area	3	f	null	null	\N	2025-11-17 21:05:13.308231+00	\N
25	7	text	Notes	4	f	null	null	\N	2025-11-17 21:05:13.308231+00	\N
26	8	yes_no	Area Cleaned?	1	t	null	null	\N	2025-11-17 21:05:13.316478+00	\N
27	8	yes_no	Cleaning Products Used?	2	t	null	null	\N	2025-11-17 21:05:13.316478+00	\N
28	8	photo	Photo of Cleaned Area	3	f	null	null	\N	2025-11-17 21:05:13.316478+00	\N
29	8	text	Notes	4	f	null	null	\N	2025-11-17 21:05:13.316478+00	\N
30	9	text	Supplier Name	1	t	null	null	\N	2025-11-17 21:05:13.325235+00	\N
31	9	temperature	Delivery Temperature (if applicable)	2	f	{"min": -5, "max": 8}	null	\N	2025-11-17 21:05:13.325235+00	\N
32	9	yes_no	Packaging Intact?	3	t	null	null	\N	2025-11-17 21:05:13.325235+00	\N
33	9	yes_no	Quality Acceptable?	4	t	null	null	\N	2025-11-17 21:05:13.325235+00	\N
34	9	photo	Photo of Delivery	5	f	null	null	\N	2025-11-17 21:05:13.325235+00	\N
35	10	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.333097+00	\N
36	10	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.333097+00	\N
37	10	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.333097+00	\N
38	11	yes_no	Evidence of Pest Activity?	1	t	null	null	\N	2025-11-17 21:05:13.341735+00	\N
39	11	dropdown	Type of Pest (if any)	2	f	null	["None", "Rodents", "Insects", "Birds", "Other"]	\N	2025-11-17 21:05:13.341735+00	\N
40	11	photo	Photo Evidence	3	f	null	null	\N	2025-11-17 21:05:13.341735+00	\N
41	11	text	Action Taken	4	f	null	null	\N	2025-11-17 21:05:13.341735+00	\N
42	12	yes_no	Evidence of Pest Activity?	1	t	null	null	\N	2025-11-17 21:05:13.349553+00	\N
43	12	dropdown	Type of Pest (if any)	2	f	null	["None", "Rodents", "Insects", "Birds", "Other"]	\N	2025-11-17 21:05:13.349553+00	\N
44	12	photo	Photo Evidence	3	f	null	null	\N	2025-11-17 21:05:13.349553+00	\N
45	12	text	Action Taken	4	f	null	null	\N	2025-11-17 21:05:13.349553+00	\N
46	13	yes_no	Food Storage Correct?	1	t	null	null	\N	2025-11-17 21:05:13.357501+00	\N
47	13	yes_no	Date Labels Present?	2	t	null	null	\N	2025-11-17 21:05:13.357501+00	\N
48	13	yes_no	No Cross-Contamination Risk?	3	t	null	null	\N	2025-11-17 21:05:13.357501+00	\N
49	13	photo	Photo Evidence	4	f	null	null	\N	2025-11-17 21:05:13.357501+00	\N
50	13	text	Issues Found	5	f	null	null	\N	2025-11-17 21:05:13.357501+00	\N
51	14	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.36616+00	\N
52	14	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.36616+00	\N
53	14	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.36616+00	\N
54	15	temperature	Temperature (°C)	1	t	{"min": -30, "max": 90}	null	\N	2025-11-17 21:05:13.374308+00	\N
55	15	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.374308+00	\N
56	16	temperature	Temperature (°C)	1	t	{"min": -30, "max": 90}	null	\N	2025-11-17 21:05:13.382773+00	\N
57	16	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.382773+00	\N
58	17	yes_no	Equipment in Good Working Order?	1	t	null	null	\N	2025-11-17 21:05:13.390896+00	\N
59	17	yes_no	Any Damage Visible?	2	t	null	null	\N	2025-11-17 21:05:13.390896+00	\N
60	17	photo	Photo of Equipment	3	f	null	null	\N	2025-11-17 21:05:13.390896+00	\N
61	17	text	Issues Found	4	f	null	null	\N	2025-11-17 21:05:13.390896+00	\N
62	18	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.399396+00	\N
63	18	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.399396+00	\N
64	18	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.399396+00	\N
65	19	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.407703+00	\N
66	19	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.407703+00	\N
67	19	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.407703+00	\N
68	20	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.415194+00	\N
69	20	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.415194+00	\N
70	20	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.415194+00	\N
71	21	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.42355+00	\N
72	21	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.42355+00	\N
73	21	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.42355+00	\N
74	22	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.431714+00	\N
75	22	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.431714+00	\N
76	22	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.431714+00	\N
77	23	yes_no	Waste Bins Emptied?	1	t	null	null	\N	2025-11-17 21:05:13.438824+00	\N
78	23	yes_no	Recycling Separated Correctly?	2	t	null	null	\N	2025-11-17 21:05:13.438824+00	\N
79	23	yes_no	Bin Area Clean?	3	t	null	null	\N	2025-11-17 21:05:13.438824+00	\N
80	23	text	Notes	4	f	null	null	\N	2025-11-17 21:05:13.438824+00	\N
81	24	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.44688+00	\N
82	24	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.44688+00	\N
83	24	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.44688+00	\N
84	25	yes_no	Equipment Present?	1	t	null	null	\N	2025-11-17 21:05:13.45565+00	\N
85	25	yes_no	In Good Condition?	2	t	null	null	\N	2025-11-17 21:05:13.45565+00	\N
86	25	yes_no	Inspection Date Current?	3	t	null	null	\N	2025-11-17 21:05:13.45565+00	\N
87	25	photo	Photo of Inspection Tag	4	f	null	null	\N	2025-11-17 21:05:13.45565+00	\N
88	25	text	Notes	5	f	null	null	\N	2025-11-17 21:05:13.45565+00	\N
89	26	yes_no	Equipment Present?	1	t	null	null	\N	2025-11-17 21:05:13.463776+00	\N
90	26	yes_no	In Good Condition?	2	t	null	null	\N	2025-11-17 21:05:13.463776+00	\N
91	26	yes_no	Inspection Date Current?	3	t	null	null	\N	2025-11-17 21:05:13.463776+00	\N
92	26	photo	Photo of Inspection Tag	4	f	null	null	\N	2025-11-17 21:05:13.463776+00	\N
93	26	text	Notes	5	f	null	null	\N	2025-11-17 21:05:13.463776+00	\N
94	27	yes_no	Equipment Present?	1	t	null	null	\N	2025-11-17 21:05:13.471993+00	\N
95	27	yes_no	In Good Condition?	2	t	null	null	\N	2025-11-17 21:05:13.471993+00	\N
96	27	yes_no	Inspection Date Current?	3	t	null	null	\N	2025-11-17 21:05:13.471993+00	\N
97	27	photo	Photo of Inspection Tag	4	f	null	null	\N	2025-11-17 21:05:13.471993+00	\N
98	27	text	Notes	5	f	null	null	\N	2025-11-17 21:05:13.471993+00	\N
99	28	temperature	Temperature (°C)	1	t	{"min": -30, "max": 90}	null	\N	2025-11-17 21:05:13.480218+00	\N
100	28	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.480218+00	\N
101	29	yes_no	Task Completed Successfully?	1	t	null	null	\N	2025-11-17 21:05:13.488258+00	\N
102	29	photo	Photo Evidence	2	f	null	null	\N	2025-11-17 21:05:13.488258+00	\N
103	29	text	Notes	3	f	null	null	\N	2025-11-17 21:05:13.488258+00	\N
104	1	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 11:58:56.631369+00	\N
105	1	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 104, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -5, "max": 10, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 11:58:56.631369+00	\N
106	30	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:15:53.602299+00	\N
107	30	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 106, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -5, "max": 10, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:15:53.602299+00	\N
108	31	number	How many freezers need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:15:53.602299+00	\N
109	31	repeating_group	Freezer Temperature Records	2	t	{"repeat_count_field_id": 108, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -25, "max": -15, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Freezer Photo"}]}	\N	\N	2025-11-18 12:15:53.602299+00	\N
110	32	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:15:53.602299+00	\N
111	32	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 110, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -5, "max": 10, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:15:53.602299+00	\N
112	33	number	How many freezers need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:15:53.602299+00	\N
113	33	repeating_group	Freezer Temperature Records	2	t	{"repeat_count_field_id": 112, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -25, "max": -15, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Freezer Photo"}]}	\N	\N	2025-11-18 12:15:53.602299+00	\N
114	34	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:33:57.41385+00	\N
115	34	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 114, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": 0, "max": 5, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:33:57.41385+00	\N
116	34	yes_no	Any issues observed?	3	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
117	34	text	Notes (optional)	4	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
118	35	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:33:57.41385+00	\N
119	35	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 118, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": 0, "max": 5, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:33:57.41385+00	\N
120	35	yes_no	Any issues observed?	3	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
121	35	text	Notes (optional)	4	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
122	36	number	How many freezers need checking?	1	t	{"min": 1, "max": 10}	\N	\N	2025-11-18 12:33:57.41385+00	\N
123	36	repeating_group	Freezer Temperature Records	2	t	{"repeat_count_field_id": 122, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -25, "max": -18, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Freezer Photo"}]}	\N	\N	2025-11-18 12:33:57.41385+00	\N
124	36	yes_no	Any issues observed?	3	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
125	36	text	Notes (optional)	4	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
126	37	number	How many hot holding units?	1	t	{"min": 1, "max": 10}	\N	\N	2025-11-18 12:33:57.41385+00	\N
127	37	repeating_group	Hot Holding Unit Temperature Records	2	t	{"repeat_count_field_id": 126, "repeat_label": "Unit", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": 63, "max": 100, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Unit Photo"}]}	\N	\N	2025-11-18 12:33:57.41385+00	\N
128	37	text	Notes (optional)	3	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
129	4	yes_no	Premises secure on arrival?	1	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
130	4	dropdown	Kitchen clean and ready?	2	t	\N	["Excellent", "Good", "Fair", "Poor"]	\N	2025-11-18 12:33:57.41385+00	\N
131	4	yes_no	Hand wash stations stocked (soap & towels)?	3	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
132	4	yes_no	Fire exits clear?	4	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
133	4	yes_no	Bins empty and clean?	5	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
134	4	yes_no	Any pest activity observed?	6	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
135	4	text	Notes (optional)	7	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
136	6	yes_no	All food stored correctly?	1	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
137	6	dropdown	Kitchen cleaned and sanitized?	2	t	\N	["Excellent", "Good", "Fair", "Poor"]	\N	2025-11-18 12:33:57.41385+00	\N
138	6	yes_no	All surfaces wiped down?	3	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
139	6	yes_no	All equipment turned off?	4	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
140	6	yes_no	All fire sources extinguished (gas off, candles out)?	5	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
141	6	yes_no	Doors and windows locked?	6	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
142	6	yes_no	Alarm set?	7	t	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
143	6	text	Notes (optional)	8	f	\N	\N	\N	2025-11-18 12:33:57.41385+00	\N
144	38	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:43:01.317348+00	\N
145	38	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 144, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": 0, "max": 5, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:43:01.317348+00	\N
146	39	number	How many freezers need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:43:01.317348+00	\N
147	39	repeating_group	Freezer Temperature Records	2	t	{"repeat_count_field_id": 146, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -25, "max": -18, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Freezer Photo"}]}	\N	\N	2025-11-18 12:43:01.317348+00	\N
148	40	number	How many fridges need checking?	1	t	{"min": 1, "max": 20}	\N	\N	2025-11-18 12:43:01.317348+00	\N
149	40	repeating_group	Fridge Temperature Records	2	t	{"repeat_count_field_id": 148, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": 0, "max": 5, "create_defect_if": "out_of_range"}, {"type": "photo", "label": "Fridge Photo"}]}	\N	\N	2025-11-18 12:43:01.317348+00	\N
150	49	yes_no	HACCP Plan Reviewed?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
151	49	text	Updates Made (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
152	50	yes_no	All Records Complete?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
153	50	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
154	51	number	Number of Fridges	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 14:40:58.190648+00	\N
155	51	repeating_group	Fridge Temperature Readings	2	t	{"repeat_count_field_id": 154, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 14:40:58.190648+00	\N
156	52	number	Number of Freezers	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 14:40:58.190648+00	\N
157	52	repeating_group	Freezer Temperature Readings	2	t	{"repeat_count_field_id": 156, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 14:40:58.190648+00	\N
158	53	yes_no	Did you receive any deliveries?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
159	53	number	Number of Suppliers	2	f	\N	\N	{"field_order": 1, "equals": true}	2025-11-20 14:40:58.190648+00	\N
160	53	repeating_group	Delivery Details	3	f	{"repeat_count_field_id": 159, "repeat_label": "Delivery", "repeat_template": [{"type": "text", "label": "Supplier Name"}, {"type": "text", "label": "Item Description"}, {"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 10}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	{"field_order": 1, "equals": true}	2025-11-20 14:40:58.190648+00	\N
161	54	number	Number of Fridges	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 14:40:58.190648+00	\N
162	54	repeating_group	Fridge Temperature Readings	2	t	{"repeat_count_field_id": 161, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 14:40:58.190648+00	\N
163	55	number	Number of Freezers	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 14:40:58.190648+00	\N
164	55	repeating_group	Freezer Temperature Readings	2	t	{"repeat_count_field_id": 163, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 14:40:58.190648+00	\N
165	56	yes_no	Hand Washing Procedures Followed?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
166	56	text	Issues Observed (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
167	57	yes_no	All Staff in Proper Attire?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
168	57	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
169	58	yes_no	Any Staff Reported Illness?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
170	58	text	Details and Action Taken	2	f	\N	\N	{"field_order": 1, "equals": true}	2025-11-20 14:40:58.190648+00	\N
171	59	yes_no	Daily Cleaning Completed?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
172	59	text	Areas Needing Attention	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
173	60	yes_no	All Surfaces Sanitized?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
174	61	yes_no	All Devices Functional?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
175	61	yes_no	Any Pest Activity Observed?	2	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
176	61	text	Details of Pest Activity	3	f	\N	\N	{"field_order": 2, "equals": true}	2025-11-20 14:40:58.190648+00	\N
177	61	photo	Photo Evidence	4	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
178	62	yes_no	FIFO System Working Properly?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
179	62	yes_no	Any Expired Items Found?	2	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
180	62	text	Expired Items Removed	3	f	\N	\N	{"field_order": 2, "equals": true}	2025-11-20 14:40:58.190648+00	\N
181	63	yes_no	Proper Separation Maintained?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
182	63	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
183	64	yes_no	Color-Coding Used Correctly?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
184	65	yes_no	Separation Maintained?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
185	66	yes_no	Allergen Information Up-to-Date?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
186	66	text	Menu Changes (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
187	67	yes_no	All Staff Certified?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
188	67	text	Staff Names and Certificate Expiry	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
189	68	yes_no	All Equipment Operating Properly?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
190	68	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
191	69	yes_no	All Bins Cleaned?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
192	70	yes_no	Storage Area Acceptable?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
193	71	yes_no	Hot Water Adequate?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
194	71	temperature	Temperature (°C)	2	f	{"min": 0, "max": 100}	\N	\N	2025-11-20 14:40:58.190648+00	\N
195	72	yes_no	Premises in Good Condition?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
196	72	text	Repairs Needed (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
197	72	photo	Photo Evidence	3	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
198	73	yes_no	All Suppliers Approved?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
199	73	text	Supplier List Review Notes	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
200	74	yes_no	All Daily Records Complete?	1	t	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
201	74	text	Missing Records (if any)	2	f	\N	\N	\N	2025-11-20 14:40:58.190648+00	\N
202	75	yes_no	HACCP Plan Reviewed?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
203	75	text	Updates Made (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
204	76	yes_no	All Records Complete?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
205	76	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
206	77	number	Number of Fridges	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 15:51:08.690777+00	\N
207	77	repeating_group	Fridge Temperature Readings	2	t	{"repeat_count_field_id": 206, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 15:51:08.690777+00	\N
208	78	number	Number of Freezers	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 15:51:08.690777+00	\N
209	78	repeating_group	Freezer Temperature Readings	2	t	{"repeat_count_field_id": 208, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 15:51:08.690777+00	\N
210	79	yes_no	Did you receive any deliveries?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
211	79	number	Number of Suppliers	2	f	\N	\N	{"field_order": 1, "equals": true}	2025-11-20 15:51:08.690777+00	\N
212	79	repeating_group	Delivery Details	3	f	{"repeat_count_field_id": 211, "repeat_label": "Delivery", "repeat_template": [{"type": "text", "label": "Supplier Name"}, {"type": "text", "label": "Item Description"}, {"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 10}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	{"field_order": 1, "equals": true}	2025-11-20 15:51:08.690777+00	\N
213	80	number	Number of Fridges	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 15:51:08.690777+00	\N
214	80	repeating_group	Fridge Temperature Readings	2	t	{"repeat_count_field_id": 213, "repeat_label": "Fridge", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -10, "max": 15, "auto_defect_threshold": 5, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 15:51:08.690777+00	\N
215	81	number	Number of Freezers	1	t	{"min": 0, "max": 50}	\N	\N	2025-11-20 15:51:08.690777+00	\N
216	81	repeating_group	Freezer Temperature Readings	2	t	{"repeat_count_field_id": 215, "repeat_label": "Freezer", "repeat_template": [{"type": "temperature", "label": "Temperature (\\u00b0C)", "min": -30, "max": 0, "auto_defect_threshold": -18, "auto_defect_operator": ">"}, {"type": "photo", "label": "Photo Evidence (optional)"}]}	\N	\N	2025-11-20 15:51:08.690777+00	\N
217	82	yes_no	Hand Washing Procedures Followed?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
218	82	text	Issues Observed (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
219	83	yes_no	All Staff in Proper Attire?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
220	83	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
221	84	yes_no	Any Staff Reported Illness?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
222	84	text	Details and Action Taken	2	f	\N	\N	{"field_order": 1, "equals": true}	2025-11-20 15:51:08.690777+00	\N
223	85	yes_no	Daily Cleaning Completed?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
224	85	text	Areas Needing Attention	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
225	86	yes_no	All Surfaces Sanitized?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
226	87	yes_no	All Devices Functional?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
227	87	yes_no	Any Pest Activity Observed?	2	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
228	87	text	Details of Pest Activity	3	f	\N	\N	{"field_order": 2, "equals": true}	2025-11-20 15:51:08.690777+00	\N
229	87	photo	Photo Evidence	4	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
230	88	yes_no	FIFO System Working Properly?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
231	88	yes_no	Any Expired Items Found?	2	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
232	88	text	Expired Items Removed	3	f	\N	\N	{"field_order": 2, "equals": true}	2025-11-20 15:51:08.690777+00	\N
233	89	yes_no	Proper Separation Maintained?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
234	89	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
235	90	yes_no	Color-Coding Used Correctly?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
236	91	yes_no	Separation Maintained?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
237	92	yes_no	Allergen Information Up-to-Date?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
238	92	text	Menu Changes (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
239	93	yes_no	All Staff Certified?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
240	93	text	Staff Names and Certificate Expiry	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
241	94	yes_no	All Equipment Operating Properly?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
242	94	text	Issues Found (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
243	95	yes_no	All Bins Cleaned?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
244	96	yes_no	Storage Area Acceptable?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
245	97	yes_no	Hot Water Adequate?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
246	97	temperature	Temperature (°C)	2	f	{"min": 0, "max": 100}	\N	\N	2025-11-20 15:51:08.690777+00	\N
247	98	yes_no	Premises in Good Condition?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
248	98	text	Repairs Needed (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
249	98	photo	Photo Evidence	3	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
250	99	yes_no	All Suppliers Approved?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
251	99	text	Supplier List Review Notes	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
252	100	yes_no	All Daily Records Complete?	1	t	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
253	100	text	Missing Records (if any)	2	f	\N	\N	\N	2025-11-20 15:51:08.690777+00	\N
\.


--
-- Data for Name: tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tasks (id, name, description, is_active, order_index, form_config, has_dynamic_form, category_id, created_at, updated_at, allocated_departments, priority) FROM stdin;
1	Opening Fridge Temperature Checks	Check all fridge temperatures at opening. Legal range: 0°C to 5°C. Temperature outside range creates HIGH defect automatically.	t	1	\N	t	1	2025-11-17 20:24:29.66744+00	\N	\N	high
2	Closing Fridge Temperature Checks	Check all fridge temperatures at closing. Legal range: 0°C to 5°C.	t	2	\N	t	1	2025-11-17 20:24:29.66744+00	\N	\N	high
3	Freezer Temperature Checks	Daily freezer temperature monitoring. Legal range: -18°C to -25°C.	t	3	\N	t	1	2025-11-17 20:24:29.66744+00	\N	\N	high
4	Daily Opening Checklist	Complete opening safety and hygiene checks including premises security, hand wash stations, fire exits, and pest activity.	t	1	\N	t	2	2025-11-17 20:24:29.66744+00	\N	\N	high
5	Equipment Check	Verify all equipment is operational and gas/electrical safety checks.	t	2	\N	t	2	2025-11-17 20:24:29.66744+00	\N	\N	medium
6	Daily Closing Checklist	End of day checklist including food storage, cleaning, equipment shutdown, and security.	t	1	\N	t	3	2025-11-17 20:24:29.66744+00	\N	\N	high
7	Daily Kitchen Deep Clean	Complete kitchen cleaning including surfaces, sinks, equipment, floors, walls, and drains.	t	1	\N	t	4	2025-11-17 20:24:29.66744+00	\N	\N	high
8	Weekly Deep Clean Schedule	Weekly deep cleaning of areas behind equipment, ventilation filters, light fixtures, storage areas.	t	2	\N	t	4	2025-11-17 20:24:29.66744+00	\N	\N	medium
9	Delivery Inspection	Inspect all deliveries including vehicle cleanliness, temperatures, packaging, and dates.	t	1	\N	t	5	2025-11-17 20:24:29.66744+00	\N	\N	high
10	Daily Use-By Date Check	Check all items for expiry dates and ensure FIFO stock rotation.	t	2	\N	t	5	2025-11-17 20:24:29.66744+00	\N	\N	high
11	Daily Pest Activity Check	Check for any signs of pest activity. Any evidence creates HIGH defect.	t	1	\N	t	6	2025-11-17 20:24:29.66744+00	\N	\N	high
12	Monthly Pest Control Inspection	Monthly professional pest control inspection and treatment record.	t	2	\N	t	6	2025-11-17 20:24:29.66744+00	\N	\N	medium
13	Daily Staff Hygiene Check	Check staff uniforms, wound coverings, and illness reporting.	t	1	\N	t	7	2025-11-17 20:24:29.66744+00	\N	\N	medium
14	Weekly Hand Washing Observation	Observe and record proper hand washing technique and station supplies.	t	2	\N	t	7	2025-11-17 20:24:29.66744+00	\N	\N	low
15	Cooking Temperature Verification	Verify core cooking temperatures (minimum 75°C for meat).	t	1	\N	t	8	2025-11-17 20:24:29.66744+00	\N	\N	high
16	Reheating Temperature Check	Ensure reheated food reaches minimum 75°C core temperature.	t	2	\N	t	8	2025-11-17 20:24:29.66744+00	\N	\N	high
17	Weekly Equipment Inspection	Check all kitchen equipment for proper operation and safety.	t	1	\N	t	9	2025-11-17 20:24:29.66744+00	\N	\N	medium
18	Monthly Gas Safety Check	Monthly gas equipment safety inspection.	t	2	\N	t	9	2025-11-17 20:24:29.66744+00	\N	\N	high
19	Monthly License Display Check	Verify premises license and personal license are displayed correctly.	t	1	\N	t	10	2025-11-17 20:24:29.66744+00	\N	\N	medium
20	Quarterly Insurance Check	Verify public liability and employer's liability insurance is valid.	t	2	\N	t	10	2025-11-17 20:24:29.66744+00	\N	\N	medium
21	Daily Allergen Check	Verify allergen information is up to date and staff are briefed.	t	1	\N	t	11	2025-11-17 20:24:29.66744+00	\N	\N	high
22	Weekly Allergen Training Check	Verify staff knowledge of 14 allergens and cross-contamination procedures.	t	2	\N	t	11	2025-11-17 20:24:29.66744+00	\N	\N	medium
23	Daily Waste Disposal	Ensure bins are emptied, sanitized, and waste area is clean.	t	1	\N	t	12	2025-11-17 20:24:29.66744+00	\N	\N	medium
24	Weekly Grease Trap Check	Clean and inspect grease trap, check drainage.	t	2	\N	t	12	2025-11-17 20:24:29.66744+00	\N	\N	medium
25	Daily Fire Safety Check	Check fire exits, signs, doors, and alarm panel.	t	1	\N	t	13	2025-11-17 20:24:29.66744+00	\N	\N	high
26	Weekly Fire Extinguisher Check	Check all fire extinguishers and fire blanket.	t	2	\N	t	13	2025-11-17 20:24:29.66744+00	\N	\N	high
27	Monthly Fire Alarm Test	Test fire alarm system and record evacuation time.	t	3	\N	t	13	2025-11-17 20:24:29.66744+00	\N	\N	high
28	Weekly Hot Water Temperature Check	Check hot water outlet temperature (≥50°C) and cold water (<20°C).	t	1	\N	t	14	2025-11-17 20:24:29.66744+00	\N	\N	medium
29	Monthly Tap Flush (Unused Outlets)	Flush all unused taps to prevent legionella.	t	2	\N	t	14	2025-11-17 20:24:29.66744+00	\N	\N	low
30	AM Fridge Temperature Checks	Record morning fridge temperatures	t	1	\N	t	15	2025-11-18 12:15:53.602299+00	\N	\N	medium
31	AM Freezer Temperature Checks	Record morning freezer temperatures	t	2	\N	t	15	2025-11-18 12:15:53.602299+00	\N	\N	medium
32	PM Fridge Temperature Checks	Record evening fridge temperatures	t	1	\N	t	16	2025-11-18 12:15:53.602299+00	\N	\N	medium
33	PM Freezer Temperature Checks	Record evening freezer temperatures	t	2	\N	t	16	2025-11-18 12:15:53.602299+00	\N	\N	medium
34	Opening Fridge Temperature Checks	Record morning fridge temperatures (Legal requirement: 0°C to 5°C)	t	1	\N	t	17	2025-11-18 12:33:57.41385+00	\N	\N	medium
35	Closing Fridge Temperature Checks	Record evening fridge temperatures (Legal requirement: 0°C to 5°C)	t	2	\N	t	17	2025-11-18 12:33:57.41385+00	\N	\N	medium
36	Freezer Temperature Checks	Record freezer temperatures (Legal requirement: -25°C to -18°C)	t	3	\N	t	17	2025-11-18 12:33:57.41385+00	\N	\N	medium
37	Hot Holding Temperature Check	Check hot holding units during lunch service (Legal minimum: 63°C)	t	4	\N	t	17	2025-11-18 12:33:57.41385+00	\N	\N	medium
38	Opening Fridge Temperature Checks	Check and record all fridge temperatures with photos	t	1	\N	t	20	2025-11-18 12:43:01.317348+00	\N	\N	medium
39	Freezer Temperature Checks	Check and record all freezer temperatures with photos	t	2	\N	t	20	2025-11-18 12:43:01.317348+00	\N	\N	medium
40	Closing Fridge Temperature Checks	Check and record all fridge temperatures with photos	t	1	\N	t	21	2025-11-18 12:43:01.317348+00	\N	\N	medium
41	Unlock premises	Unlock all doors and disable alarm	t	1	\N	f	22	2025-11-18 12:43:01.317348+00	\N	\N	medium
42	Check for damage	Visual inspection of premises for damage	t	2	\N	f	22	2025-11-18 12:43:01.317348+00	\N	\N	medium
43	Turn on equipment	Switch on all necessary kitchen equipment	t	3	\N	f	22	2025-11-18 12:43:01.317348+00	\N	\N	medium
44	Check stock levels	Verify adequate stock for the day	t	4	\N	f	22	2025-11-18 12:43:01.317348+00	\N	\N	medium
45	Clean all surfaces	Wipe down all work surfaces and equipment	t	1	\N	f	23	2025-11-18 12:43:01.317348+00	\N	\N	medium
46	Empty bins	Empty all waste bins and replace liners	t	2	\N	f	23	2025-11-18 12:43:01.317348+00	\N	\N	medium
47	Turn off equipment	Switch off all non-essential equipment	t	3	\N	f	23	2025-11-18 12:43:01.317348+00	\N	\N	medium
48	Lock premises	Secure all doors and windows, activate alarm	t	4	\N	f	23	2025-11-18 12:43:01.317348+00	\N	\N	medium
49	HACCP Plan Review	Review all critical control points, verify procedures are current, and update documentation as needed	t	1	\N	t	110	2025-11-20 14:40:58.190648+00	\N	\N	medium
50	HACCP Records Verification	Check monitoring sheets, corrective actions, and verification records	t	2	\N	t	110	2025-11-20 14:40:58.190648+00	\N	\N	medium
51	AM Fridge Temperature Checks	Check and record temperatures of all refrigeration units (must be ≤5°C)	t	1	\N	t	111	2025-11-20 14:40:58.190648+00	\N	\N	medium
52	AM Freezer Temperature Checks	Check and record temperatures of all freezers (must be ≤-18°C)	t	2	\N	t	111	2025-11-20 14:40:58.190648+00	\N	\N	medium
53	Delivery Temperature Check	Record temperatures and reject if outside safe limits	t	3	\N	t	111	2025-11-20 14:40:58.190648+00	\N	\N	medium
54	PM Fridge Temperature Checks	Check and record temperatures of all refrigeration units (must be ≤5°C)	t	1	\N	t	112	2025-11-20 14:40:58.190648+00	\N	\N	medium
55	PM Freezer Temperature Checks	Check and record temperatures of all freezers (must be ≤-18°C)	t	2	\N	t	112	2025-11-20 14:40:58.190648+00	\N	\N	medium
56	Hand Washing Compliance Check	Ensure staff wash hands before handling food, after breaks, after touching raw food	t	1	\N	t	113	2025-11-20 14:40:58.190648+00	\N	\N	medium
57	Personal Hygiene Inspection	Verify clean uniform, hair net/hat, no jewelry, clean hands, covered wounds	t	2	\N	t	113	2025-11-20 14:40:58.190648+00	\N	\N	medium
58	Staff Illness Reporting Check	Ensure no staff with vomiting, diarrhea, or infections are handling food	t	3	\N	t	113	2025-11-20 14:40:58.190648+00	\N	\N	medium
59	Daily Kitchen Cleaning Check	Clean all surfaces, equipment, floors following cleaning schedule	t	1	\N	t	114	2025-11-20 14:40:58.190648+00	\N	\N	medium
60	Food Contact Surfaces Sanitization	Clean with detergent, rinse, and apply sanitizer	t	2	\N	t	114	2025-11-20 14:40:58.190648+00	\N	\N	medium
61	Pest Control Device Check	Check devices are functional, clean fly killers, note any pest activity	t	1	\N	t	115	2025-11-20 14:40:58.190648+00	\N	\N	medium
62	Stock Rotation Check (FIFO)	Check date labels, rotate stock, remove expired items	t	1	\N	t	116	2025-11-20 14:40:58.190648+00	\N	\N	medium
63	Food Storage Separation Audit	Check storage areas maintain separation (raw below cooked, covered items)	t	2	\N	t	116	2025-11-20 14:40:58.190648+00	\N	\N	medium
64	Color-Coded Equipment Check	Check boards, knives, and cloths are color-coded and used for designated purposes	t	1	\N	t	117	2025-11-20 14:40:58.190648+00	\N	\N	medium
65	Separate Preparation Area Audit	Check physical separation or time separation is maintained	t	2	\N	t	117	2025-11-20 14:40:58.190648+00	\N	\N	medium
66	Allergen Information Update	Verify allergen matrix is current and accurate for all 14 allergens	t	1	\N	t	118	2025-11-20 14:40:58.190648+00	\N	\N	medium
67	Food Hygiene Training Verification	Check certificates are current and new staff are enrolled in training	t	1	\N	t	119	2025-11-20 14:40:58.190648+00	\N	\N	medium
68	Refrigeration Equipment Check	Check door seals, cleanliness, defrost cycles, and unusual noises	t	1	\N	t	120	2025-11-20 14:40:58.190648+00	\N	\N	medium
69	Waste Bin Cleaning	Empty, clean, and sanitize internal and external bins	t	1	\N	t	121	2025-11-20 14:40:58.190648+00	\N	\N	medium
70	Waste Storage Area Inspection	Verify area is clean, bins are lidded, no pest attraction, no overflow	t	2	\N	t	121	2025-11-20 14:40:58.190648+00	\N	\N	medium
71	Water Temperature Check	Check hot water reaches adequate temperature for effective hand washing	t	1	\N	t	122	2025-11-20 14:40:58.190648+00	\N	\N	medium
72	Premises Condition Inspection	Check for cracks, holes, peeling paint, water damage that could harbor pests	t	1	\N	t	123	2025-11-20 14:40:58.190648+00	\N	\N	medium
73	Supplier Approval Review	Verify all suppliers are approved, have adequate food safety credentials	t	1	\N	t	124	2025-11-20 14:40:58.190648+00	\N	\N	medium
74	Daily Records Completion Check	Check temperature logs, cleaning schedules, and delivery records are filled in	t	1	\N	t	125	2025-11-20 14:40:58.190648+00	\N	\N	medium
75	HACCP Plan Review	Review all critical control points, verify procedures are current, and update documentation as needed	t	1	\N	t	126	2025-11-20 15:51:08.690777+00	\N	\N	medium
76	HACCP Records Verification	Check monitoring sheets, corrective actions, and verification records	t	2	\N	t	126	2025-11-20 15:51:08.690777+00	\N	\N	medium
77	AM Fridge Temperature Checks	Check and record temperatures of all refrigeration units (must be ≤5°C)	t	1	\N	t	127	2025-11-20 15:51:08.690777+00	\N	\N	medium
78	AM Freezer Temperature Checks	Check and record temperatures of all freezers (must be ≤-18°C)	t	2	\N	t	127	2025-11-20 15:51:08.690777+00	\N	\N	medium
79	Delivery Temperature Check	Record temperatures and reject if outside safe limits	t	3	\N	t	127	2025-11-20 15:51:08.690777+00	\N	\N	medium
80	PM Fridge Temperature Checks	Check and record temperatures of all refrigeration units (must be ≤5°C)	t	1	\N	t	128	2025-11-20 15:51:08.690777+00	\N	\N	medium
81	PM Freezer Temperature Checks	Check and record temperatures of all freezers (must be ≤-18°C)	t	2	\N	t	128	2025-11-20 15:51:08.690777+00	\N	\N	medium
82	Hand Washing Compliance Check	Ensure staff wash hands before handling food, after breaks, after touching raw food	t	1	\N	t	129	2025-11-20 15:51:08.690777+00	\N	\N	medium
83	Personal Hygiene Inspection	Verify clean uniform, hair net/hat, no jewelry, clean hands, covered wounds	t	2	\N	t	129	2025-11-20 15:51:08.690777+00	\N	\N	medium
84	Staff Illness Reporting Check	Ensure no staff with vomiting, diarrhea, or infections are handling food	t	3	\N	t	129	2025-11-20 15:51:08.690777+00	\N	\N	medium
85	Daily Kitchen Cleaning Check	Clean all surfaces, equipment, floors following cleaning schedule	t	1	\N	t	130	2025-11-20 15:51:08.690777+00	\N	\N	medium
86	Food Contact Surfaces Sanitization	Clean with detergent, rinse, and apply sanitizer	t	2	\N	t	130	2025-11-20 15:51:08.690777+00	\N	\N	medium
87	Pest Control Device Check	Check devices are functional, clean fly killers, note any pest activity	t	1	\N	t	131	2025-11-20 15:51:08.690777+00	\N	\N	medium
88	Stock Rotation Check (FIFO)	Check date labels, rotate stock, remove expired items	t	1	\N	t	132	2025-11-20 15:51:08.690777+00	\N	\N	medium
89	Food Storage Separation Audit	Check storage areas maintain separation (raw below cooked, covered items)	t	2	\N	t	132	2025-11-20 15:51:08.690777+00	\N	\N	medium
90	Color-Coded Equipment Check	Check boards, knives, and cloths are color-coded and used for designated purposes	t	1	\N	t	133	2025-11-20 15:51:08.690777+00	\N	\N	medium
91	Separate Preparation Area Audit	Check physical separation or time separation is maintained	t	2	\N	t	133	2025-11-20 15:51:08.690777+00	\N	\N	medium
92	Allergen Information Update	Verify allergen matrix is current and accurate for all 14 allergens	t	1	\N	t	134	2025-11-20 15:51:08.690777+00	\N	\N	medium
93	Food Hygiene Training Verification	Check certificates are current and new staff are enrolled in training	t	1	\N	t	135	2025-11-20 15:51:08.690777+00	\N	\N	medium
94	Refrigeration Equipment Check	Check door seals, cleanliness, defrost cycles, and unusual noises	t	1	\N	t	136	2025-11-20 15:51:08.690777+00	\N	\N	medium
95	Waste Bin Cleaning	Empty, clean, and sanitize internal and external bins	t	1	\N	t	137	2025-11-20 15:51:08.690777+00	\N	\N	medium
96	Waste Storage Area Inspection	Verify area is clean, bins are lidded, no pest attraction, no overflow	t	2	\N	t	137	2025-11-20 15:51:08.690777+00	\N	\N	medium
97	Water Temperature Check	Check hot water reaches adequate temperature for effective hand washing	t	1	\N	t	138	2025-11-20 15:51:08.690777+00	\N	\N	medium
98	Premises Condition Inspection	Check for cracks, holes, peeling paint, water damage that could harbor pests	t	1	\N	t	139	2025-11-20 15:51:08.690777+00	\N	\N	medium
99	Supplier Approval Review	Verify all suppliers are approved, have adequate food safety credentials	t	1	\N	t	140	2025-11-20 15:51:08.690777+00	\N	\N	medium
100	Daily Records Completion Check	Check temperature logs, cleaning schedules, and delivery records are filled in	t	1	\N	t	141	2025-11-20 15:51:08.690777+00	\N	\N	medium
\.


--
-- Data for Name: user_sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_sites (id, user_id, site_id, created_at) FROM stdin;
7	9	11	2025-11-19 16:38:22.309424+00
8	9	12	2025-11-19 16:38:22.309424+00
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, email, hashed_password, first_name, last_name, role, is_active, phone, organization_id, created_at, updated_at, department, job_title, must_change_password) FROM stdin;
6	hello@prstart.co.uk	$2b$12$LW2Lcb34moBa.4HtSkDbxuqH3BjG59vJ05zP3/rPPxtBQmgo2vqtq	Attila	Juhasz	SUPER_ADMIN	t	\N	5	2025-11-17 17:46:20.879462+00	2025-11-17 18:14:39.090308+00	\N	\N	f
7	dj.atesz@gmail.com	$2b$12$GFfHmbCEjTrDj.nvQPDS3uPcrViWL45gGwgopFR2oEpL/CIhEJwBW	Attila	Juhasz	ORG_ADMIN	t	\N	9	2025-11-17 18:51:36.655644+00	2025-11-17 18:52:54.768038+00	\N	\N	f
9	lamer@atesz.co.uk	$2b$12$W9XVKFx2oHTYLN9S9R9i..CxJ5XVRFbl69vRSr1QuzkwT13KAPzoa	test	user	SITE_USER	t	\N	9	2025-11-17 20:53:50.512519+00	2025-11-18 09:48:57.685374+00	\N	\N	f
10	admin-test1763639586@example.com	$2b$12$Q.5lNc1vdFPLQQeBZTM4p.RlUM/kVE2aVm.MDJ9rm4JJHtRozsWQi	John	Doe	ORG_ADMIN	t	\N	10	2025-11-20 11:53:06.170687+00	\N	\N	\N	f
\.


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 141, true);


--
-- Name: checklist_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.checklist_items_id_seq', 52, true);


--
-- Name: checklists_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.checklists_id_seq', 40, true);


--
-- Name: defects_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.defects_id_seq', 2, true);


--
-- Name: organization_modules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organization_modules_id_seq', 15, true);


--
-- Name: organizations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.organizations_id_seq', 10, true);


--
-- Name: password_reset_tokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.password_reset_tokens_id_seq', 1, false);


--
-- Name: promotions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.promotions_id_seq', 1, true);


--
-- Name: site_tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.site_tasks_id_seq', 1, false);


--
-- Name: sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sites_id_seq', 12, true);


--
-- Name: task_field_responses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_field_responses_id_seq', 273, true);


--
-- Name: task_fields_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_fields_id_seq', 253, true);


--
-- Name: tasks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tasks_id_seq', 100, true);


--
-- Name: user_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_sites_id_seq', 8, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: checklist_items checklist_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklist_items
    ADD CONSTRAINT checklist_items_pkey PRIMARY KEY (id);


--
-- Name: checklists checklists_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklists
    ADD CONSTRAINT checklists_pkey PRIMARY KEY (id);


--
-- Name: defects defects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects
    ADD CONSTRAINT defects_pkey PRIMARY KEY (id);


--
-- Name: organization_modules organization_modules_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_modules
    ADD CONSTRAINT organization_modules_pkey PRIMARY KEY (id);


--
-- Name: organizations organizations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organizations
    ADD CONSTRAINT organizations_pkey PRIMARY KEY (id);


--
-- Name: password_reset_tokens password_reset_tokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_pkey PRIMARY KEY (id);


--
-- Name: promotions promotions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.promotions
    ADD CONSTRAINT promotions_pkey PRIMARY KEY (id);


--
-- Name: site_tasks site_tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_tasks
    ADD CONSTRAINT site_tasks_pkey PRIMARY KEY (id);


--
-- Name: sites sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (id);


--
-- Name: task_field_responses task_field_responses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses
    ADD CONSTRAINT task_field_responses_pkey PRIMARY KEY (id);


--
-- Name: task_fields task_fields_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_fields
    ADD CONSTRAINT task_fields_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: user_sites user_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sites
    ADD CONSTRAINT user_sites_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_categories_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_categories_id ON public.categories USING btree (id);


--
-- Name: ix_checklist_items_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_checklist_items_id ON public.checklist_items USING btree (id);


--
-- Name: ix_checklists_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_checklists_id ON public.checklists USING btree (id);


--
-- Name: ix_defects_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_defects_id ON public.defects USING btree (id);


--
-- Name: ix_organization_modules_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organization_modules_id ON public.organization_modules USING btree (id);


--
-- Name: ix_organizations_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_organizations_id ON public.organizations USING btree (id);


--
-- Name: ix_organizations_org_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_organizations_org_id ON public.organizations USING btree (org_id);


--
-- Name: ix_password_reset_tokens_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_password_reset_tokens_id ON public.password_reset_tokens USING btree (id);


--
-- Name: ix_password_reset_tokens_token; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_password_reset_tokens_token ON public.password_reset_tokens USING btree (token);


--
-- Name: ix_site_tasks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_site_tasks_id ON public.site_tasks USING btree (id);


--
-- Name: ix_sites_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_sites_id ON public.sites USING btree (id);


--
-- Name: ix_task_field_responses_checklist_item_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_task_field_responses_checklist_item_id ON public.task_field_responses USING btree (checklist_item_id);


--
-- Name: ix_task_field_responses_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_task_field_responses_id ON public.task_field_responses USING btree (id);


--
-- Name: ix_task_fields_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_task_fields_id ON public.task_fields USING btree (id);


--
-- Name: ix_task_fields_task_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_task_fields_task_id ON public.task_fields USING btree (task_id);


--
-- Name: ix_tasks_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_tasks_id ON public.tasks USING btree (id);


--
-- Name: ix_user_sites_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_user_sites_id ON public.user_sites USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: categories categories_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: checklist_items checklist_items_checklist_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklist_items
    ADD CONSTRAINT checklist_items_checklist_id_fkey FOREIGN KEY (checklist_id) REFERENCES public.checklists(id);


--
-- Name: checklist_items checklist_items_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklist_items
    ADD CONSTRAINT checklist_items_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: checklists checklists_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklists
    ADD CONSTRAINT checklists_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: checklists checklists_completed_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklists
    ADD CONSTRAINT checklists_completed_by_id_fkey FOREIGN KEY (completed_by_id) REFERENCES public.users(id);


--
-- Name: checklists checklists_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checklists
    ADD CONSTRAINT checklists_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- Name: defects defects_checklist_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects
    ADD CONSTRAINT defects_checklist_item_id_fkey FOREIGN KEY (checklist_item_id) REFERENCES public.checklist_items(id);


--
-- Name: defects defects_closed_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects
    ADD CONSTRAINT defects_closed_by_id_fkey FOREIGN KEY (closed_by_id) REFERENCES public.users(id);


--
-- Name: defects defects_reported_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects
    ADD CONSTRAINT defects_reported_by_id_fkey FOREIGN KEY (reported_by_id) REFERENCES public.users(id);


--
-- Name: defects defects_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.defects
    ADD CONSTRAINT defects_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- Name: organization_modules organization_modules_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.organization_modules
    ADD CONSTRAINT organization_modules_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: password_reset_tokens password_reset_tokens_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.password_reset_tokens
    ADD CONSTRAINT password_reset_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: site_tasks site_tasks_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_tasks
    ADD CONSTRAINT site_tasks_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- Name: site_tasks site_tasks_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.site_tasks
    ADD CONSTRAINT site_tasks_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id);


--
-- Name: sites sites_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- Name: task_field_responses task_field_responses_auto_defect_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses
    ADD CONSTRAINT task_field_responses_auto_defect_id_fkey FOREIGN KEY (auto_defect_id) REFERENCES public.defects(id);


--
-- Name: task_field_responses task_field_responses_checklist_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses
    ADD CONSTRAINT task_field_responses_checklist_item_id_fkey FOREIGN KEY (checklist_item_id) REFERENCES public.checklist_items(id) ON DELETE CASCADE;


--
-- Name: task_field_responses task_field_responses_completed_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses
    ADD CONSTRAINT task_field_responses_completed_by_fkey FOREIGN KEY (completed_by) REFERENCES public.users(id);


--
-- Name: task_field_responses task_field_responses_task_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_field_responses
    ADD CONSTRAINT task_field_responses_task_field_id_fkey FOREIGN KEY (task_field_id) REFERENCES public.task_fields(id) ON DELETE CASCADE;


--
-- Name: task_fields task_fields_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_fields
    ADD CONSTRAINT task_fields_task_id_fkey FOREIGN KEY (task_id) REFERENCES public.tasks(id) ON DELETE CASCADE;


--
-- Name: tasks tasks_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- Name: user_sites user_sites_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sites
    ADD CONSTRAINT user_sites_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- Name: user_sites user_sites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sites
    ADD CONSTRAINT user_sites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_organization_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organizations(id);


--
-- PostgreSQL database dump complete
--

\unrestrict mvWt3qiycOLHTKf5iM78spRUZ3gGPTlWgLdmpNwoPhufn4scTcS4zgpoQKrBaii

