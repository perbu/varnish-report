

CREATE TABLE batches(
	id integer primary key asc, 
	arch varchar(128), 
	rev char(7), 
	timestamp integer,
	error integer,
	xfail integer,
	pass integer,
	skip integer,
	total integer,
	xpass integer,
	fail integer
	);

CREATE TABLE failures(
	id integer primary key asc, 
	test varchar(16),
	runtime real, 
	log text);

