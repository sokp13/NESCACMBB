select *
from player natural join perdef
where Team_Id = 'TUF';

drop view if exists points_per_game;
create view points_per_game as
select p.First_Name, p.Last_Name, cast(r.fgm as float)/r.fga as 'TEST'
from player as p natural join totals as r
where r.poss >=25;

select *
from points_per_game
where Last_Name = 'Thoerner';

select First_Name, Last_Name, pd_poss
from player natural join perdef
where pd_poss >=75;