
CREATE TABLE public.datasetnewsscore
(
    newsid integer NOT NULL,
    grammarscore integer,
    wordcount integer,
    ads integer,
    subdomains integer,
    datecheck integer,
    author integer,
    CONSTRAINT datasetnewsscore_pkey PRIMARY KEY (newsid)
)



CREATE TABLE public.domainfilterlist
(
    url text COLLATE pg_catalog."default" NOT NULL,
    domaintype text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT domainfilterlist_pkey PRIMARY KEY (url, domaintype)
)




CREATE TABLE public.domaintypescore
(
    type text COLLATE pg_catalog."default" NOT NULL,
    score integer
)


CREATE TABLE public.news
(
    newsid integer NOT NULL DEFAULT nextval('news_newsid_seq'::regclass),
    article text COLLATE pg_catalog."default",
    title text COLLATE pg_catalog."default",
    author text COLLATE pg_catalog."default",
    originalcontent text COLLATE pg_catalog."default",
    createddate timestamp without time zone,
    fetcheddate timestamp without time zone,
    articleurl text COLLATE pg_catalog."default" NOT NULL,
    lastused timestamp without time zone,
    urlsearch text COLLATE pg_catalog."default",
    CONSTRAINT news_pkey PRIMARY KEY (newsid),
    CONSTRAINT news_articleurl_key UNIQUE (articleurl)
)

CREATE TABLE public.newsfetchedapi
(
    id integer NOT NULL DEFAULT nextval('newsfetchedapi_id_seq'::regclass),
    url text COLLATE pg_catalog."default" NOT NULL,
    author text COLLATE pg_catalog."default",
    title text COLLATE pg_catalog."default",
    description text COLLATE pg_catalog."default",
    imageurl text COLLATE pg_catalog."default",
    publishedat timestamp without time zone,
    CONSTRAINT newsfetchedapi_pkey PRIMARY KEY (id),
    CONSTRAINT newsfetchedapi_url_key UNIQUE (url)
)

CREATE TABLE public.score
(
    newsid integer NOT NULL,
    grammar integer,
    wordcount integer,
    ads integer,
    subdomain integer,
    datecheck integer,
    author integer,
    CONSTRAINT score_pkey PRIMARY KEY (newsid)
)
