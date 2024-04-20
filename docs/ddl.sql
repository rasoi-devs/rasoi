-- public.recipe definition

-- Drop table

-- DROP TABLE recipe;

CREATE TABLE recipe (
	id bigserial NOT NULL,
	title varchar NOT NULL,
	image_name varchar NOT NULL,
	instructions _varchar NOT NULL,
	ingredients_full _varchar NOT NULL,
	ingredients _varchar NOT NULL,
	image_features public.vector NOT NULL,
	CONSTRAINT recipe_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_recipe_image_name ON public.recipe USING btree (image_name);
CREATE INDEX ix_recipe_title ON public.recipe USING btree (title);


-- public."user" definition

-- Drop table

-- DROP TABLE "user";

CREATE TABLE "user" (
	id bigserial NOT NULL,
	email varchar NOT NULL,
	hashed_password varchar NOT NULL,
	active bool NOT NULL,
	CONSTRAINT user_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);

-- public.rating definition

-- Drop table

-- DROP TABLE rating;

CREATE TABLE rating (
	id bigserial NOT NULL,
	created_at timestamptz NOT NULL DEFAULT now(),
	updated_at timestamptz NULL,
	rate int4 NOT NULL,
	user_id int8 NULL,
	recipe_id int8 NULL,
	CONSTRAINT rating_pkey PRIMARY KEY (id),
	CONSTRAINT rating_recipe_id_fkey FOREIGN KEY (recipe_id) REFERENCES recipe(id),
	CONSTRAINT rating_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id)
);


-- public.ingredient definition

-- Drop table

-- DROP TABLE ingredient;

CREATE TABLE ingredient (
	"name" varchar NOT NULL,
	CONSTRAINT ingredient_pkey PRIMARY KEY (name)
);