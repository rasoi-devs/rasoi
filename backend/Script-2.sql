-- some random sql query experiments, might be useful later

select title, ner, (select count(*) from unnest(ner) as ing where ing=any(array['eggs', 'water'])) as mc from recipe order by mc desc limit 10;

select title, ner
from recipe
where
'{"eggs","water","sugar"}' <@ ner;

create index idx_ner on recipe using gin(ner);

select * from recipe where title like '%mutton%';

select distinct SUBSTRING(link, 0, 15) from recipe;

delete from recipe r where not exists (select * from recipe_ingredient ri where r.id = ri.recipe_id);

(
  select 
    * 
  from 
    recipe 
  where 
    title ilike '%khichuri%'
) 
union 
  (
    select 
      * 
    from 
      recipe 
    where 
      title ilike '%bhetki%'
  ) 
union 
  (
    select 
      * 
    from 
      recipe 
    where 
      title ilike '% ilish%'
  ) 
union 
  (
    select 
      * 
    from 
      recipe 
    where 
      title ilike '%sambar%'
  );

select
	link
from
	recipe
where
	id in (
	select
		min(r.id) as id
	from
		recipe r
	group by
		left(r.link,
		10));


SELECT COUNT(*) AS cnt, MIN(link) 
FROM recipe r1
WHERE EXISTS (
    SELECT 1 
    FROM recipe r2 
    WHERE LEFT(r1.link, 5) = LEFT(r2.link, 5)
)
GROUP BY LEFT(link, 5) 
ORDER BY cnt DESC;

	
SELECT COUNT(*) AS cnt, MIN(link) 
FROM recipe 
WHERE LEFT(link, 5) IN (
    SELECT DISTINCT LEFT(link, 5) 
    FROM recipe
) 
GROUP BY LEFT(link, 5) 
ORDER BY cnt DESC;

select distinct name from ingredient i where i.name ilike 'sugar%' limit 10;

--ALTER TABLE ingredient ADD COLUMN id SERIAL PRIMARY KEY;
