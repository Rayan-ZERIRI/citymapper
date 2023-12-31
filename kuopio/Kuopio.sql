DROP DATABASE projet;
CREATE DATABASE projet;
\c projet
DROP TABLE bus;
DROP TABLE nodes;
DROP TABLE combined;
DROP TABLE walk;
DROP TABLE temporal_day;
DROP TABLE temporal_week;
DROP TABLE stats;
DROP TABLE routes;


CREATE TABLE bus (
    from_stop_I INT, 
    to_stop_I INT,
    d INT, 
    duration_avg NUMERIC(11,6),
    n_vehicles INT, 
    route_I_counts VARCHAR(100) 
);

CREATE TABLE nodes (
    stop_I NUMERIC PRIMARY KEY,
    latitude numeric(10,5),
	longitude numeric(10,5),
    name VARCHAR(100)
);
CREATE TABLE combined (
    from_stop_I NUMERIC,
    to_stop_I NUMERIC, 
    d NUMERIC, 
    duration_avg NUMERIC, 
    n_vehicles NUMERIC,
    route_I_counts VARCHAR(100),
    route_type NUMERIC
);

CREATE TABLE walk (
    from_stop_I INT, 
    to_stop_I INT,
    d INT, 
    d_walk INT,
    n_vehicles NUMERIC
);  

CREATE TABLE temporal_day (
    from_stop_I INT,
    to_stop_I INT,
    dep_time_ut INT,
    arr_time_ut INT,
    route_type INT,
    trip_I INT,
    seq INT,
    route_I INT 
    
     
);
CREATE TABLE temporal_week(
    from_stop_I INT,
    to_stop_I INT,
    dep_time_ut INT,
    arr_time_ut INT,
    route_type INT,
    trip_I INT,
    seq INT,
    route_I INT 
  
);

CREATE TABLE stats (
    buffer_center NUMERIC(10,8),
    buffer_center_lon NUMERIC(10,8),
    buffer_radius_km NUMERIC(3,1),
    extract_start_date VARCHAR(100),
    link_distance_avg_m INT,
    n_connections INT,
    n_links INT,
    n_stops INT,
    network_length_m INT,
    vehicle_kilometers NUMERIC(16,10)
);

CREATE TABLE routes (
    route_I NUMERIC,
    route_name VARCHAR(100),
    route_type NUMERIC
);




DROP TABLE p_history;
DROP TABLE p_users;
CREATE TABLE p_users (
    username VARCHAR(100)
);

CREATE TABLE p_history (
	from_station VARCHAR(100),
    to_station VARCHAR(100)
);


INSERT INTO p_users(username) values ('Anonymous');


