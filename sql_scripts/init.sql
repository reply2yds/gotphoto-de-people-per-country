drop table if exists places;

create table `places` (
  `city` varchar(80) default null,
  `county` varchar(80) default null,
  `country` varchar(80) default null
);

drop table if exists places_info;

create table `places_info` (
  `id` int not null auto_increment,
  `city` varchar(80) default null,
  `county` varchar(80) default null,
  `country` varchar(80) default null,
  primary key (`id`)
);


drop table if exists peoples;

create table `peoples` (
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `place_of_birth` varchar(80) default null
);

drop table if exists peoples_info;

create table `peoples_info` (
  `id` int not null auto_increment,
  `given_name` varchar(80) default null,
  `family_name` varchar(80) default null,
  `date_of_birth` date default null,
  `birth_place_id` int default null,
  FOREIGN KEY (birth_place_id) REFERENCES places_info(id),
  primary key (`id`)
);