drop table if exists yelp
go
create table Yelp (
	 id				varchar(50)
	,name			varchar(50)
	,price			varchar(5)
	,rating			float
	,review_count	int
	,street			varchar(50)
	,city_prov_pc	varchar(50)
	,country varchar(50)
	)
go
select * from yelp