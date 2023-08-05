## Definition (Last visited 2023-08-05)

This is my super app for improving my productivity and life !

* It aims to help me capture knowledge in notes
* Motivates me reading these notes and not have them buried
* Allows me to plan projects, organise thoughts and get reminded of past convictions.
* It is not limited to notes, Lots of exciting features to come with aim to get me more productive and useful
* Also this is my way of learning Web development and playing around with new tech



### Technical Structure (Last visited 2023-08-05)

1. Python Backend
2. HTML + Jinja Frontend
3. AWS RDS Postgress database
4. Heroku Deployment


#### 1. Python Backend

* app.py has all backend code for now aside from database DDL to create the tables

#### 2. HTML + Jinja Frontend + Browser Javascript

* /templates folder has all html files and templates for now

#### 3. AWS RDS Posgresql database

Link: https://eu-north-1.console.aws.amazon.com/rds/home?region=eu-north-1#database:id=note-app;is-cluster=false (only Kareem can access this)

Region: Stockholm (eu-north-1)

**To connect in dbeaver:**

host: endpoint link in aws

Port: 5432

Database: postgres

Username/Password: with Kareem only (create your own RDS if you are not Kareem xD)


**DDL to create in the database:**

```
CREATE TABLE public.note_items (
	note_id serial4 NOT NULL,
	title varchar(150) NOT NULL,
	body text NULL,
	date_added date NULL DEFAULT CURRENT_TIMESTAMP,
	last_read_at timestamp NULL,
	is_archived bool NULL DEFAULT false,
	created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
	CONSTRAINT note_items_pkey PRIMARY KEY (note_id)
);

CREATE OR REPLACE VIEW public.note_items_unarchived
AS 
(
SELECT note_items.note_id,
    note_items.title,
    note_items.body,
    note_items.date_added,
    note_items.last_read_at,
    note_items.is_archived,
    note_items.created_at
   FROM 
   	note_items
  WHERE 
  	NOT note_items.is_archived
 )
 ;
```


## How to run the code:
* Python Environment installation

## New Features and Bug Fixes
* 

## Development:

Planning new features in frontend and backend