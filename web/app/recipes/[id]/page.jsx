import React from "react";
import Image from "next/image";
import RecipeList from "@/components/RecipeList";
import RatingInteractive from "@/components/RatingInteractive";
import { Rating } from "@smastrom/react-rating";
import CommentInteractive from "@/components/CommentInteractive";
import generateMeta from "@/utils/meta";

export async function generateMetadata({ params, searchParams }, parent) {
  const recipe = await fetchRecipe(params.id);

  return generateMeta(
    recipe.title,
    recipe.instructions.join(" "),
    `${process.env.NEXT_PUBLIC_API_URL}/recipe-images/${encodeURIComponent(
      recipe.image_name,
    )}.jpg`,
  );
}

async function fetchRecipe(id) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/recipes/${id}`);
  if (!res.ok) throw new Error("Failed to fetch recipe");
  return res.json();
}

async function fetchSimilarRecipes(id) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/recipes/${id}/similar`,
  );
  if (!res.ok) throw new Error("Failed to fetch similar recipes");
  return res.json();
}

async function fetchRatings(id) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/recipes/${id}/ratings`,
    // on page refresh, refresh this value (invalidate cache)
    { cache: "no-cache" },
  );
  if (!res.ok) throw new Error("Failed to fetch ratings");
  return res.json();
}

async function fetchComments(id) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/recipes/${id}/comments`,
    // on page refresh, refresh this value (invalidate cache)
    { cache: "no-cache" },
  );
  if (!res.ok) throw new Error("Failed to fetch comments");
  return res.json();
}

export default async function Page({ params: { id } }) {
  const recipe = await fetchRecipe(id);
  const similarRecipes = await fetchSimilarRecipes(id);
  const ratings = await fetchRatings(id);
  const comments = await fetchComments(id);
  const totalRating = ratings.map((r) => r.rate).reduce((a, b) => a + b, 0);
  let avgRating = 0;
  if (ratings.length > 0) avgRating = Math.round(totalRating / ratings.length);

  return (
    <main className="flex flex-col">
      <h1 className="mb-3 text-3xl italic text-accent-500">{recipe.title}</h1>

      <Image
        src={`${
          process.env.NEXT_PUBLIC_API_URL
        }/recipe-images/${encodeURIComponent(recipe.image_name)}.jpg`}
        width={500}
        height={500}
        className="self-center rounded-xl shadow-md"
        alt={`${recipe.title} image`}
      />

      {totalRating > 0 && (
        <div className="mt-3 flex flex-row items-center gap-2 text-xl text-accent-500">
          <p>Rated {avgRating}</p>
          <Rating readOnly value={avgRating} className="max-w-[10rem]" />
        </div>
      )}

      <h2 className="mt-3 text-2xl text-accent-500" id="instructions">
        Instructions
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.instructions.map((d, idx) => (
          <li key={idx}>{d}</li>
        ))}
      </ul>

      <h2 className="mt-3 text-2xl text-accent-500" id="ingredients">
        Ingredients
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.ingredients_full.map((i, idx) => (
          <li key={idx}>{i}</li>
        ))}
      </ul>

      <div className="mt-3 flex flex-row items-center gap-2 text-xl">
        <p>
          Your <span className="text-secondary-500">rating</span>:
        </p>
        <RatingInteractive
          recipeId={recipe.id}
          allRatings={ratings}
          nextUrlPrefix={`/recipes/${recipe.id}`}
        />
      </div>

      <h2 className="mt-3 text-2xl text-accent-500">You may also like 😋</h2>
      <RecipeList recipes={similarRecipes} />

      <h2 className="mt-3 text-2xl text-accent-500" id="ingredients">
        Comments
      </h2>

      <CommentInteractive
        recipeId={recipe.id}
        nextUrlPrefix={`/recipes/${recipe.id}`}
      />

      {comments.length > 0 &&
        comments.map((c, idx) => (
          <article
            key={idx}
            className="mt-2 border-t border-gray-200 bg-white text-base"
          >
            <footer className="flex items-center justify-between">
              <div className="flex items-center">
                <p className="mr-3 inline-flex items-center font-semibold text-gray-900">
                  {c.user.email}
                </p>
                <p className="text-sm text-gray-600">
                  <time
                    pubdate={c.created_at}
                    dateTime={c.created_at}
                    title={c.created_at}
                  >
                    {new Date(c.created_at).toLocaleString()}
                  </time>
                </p>
              </div>
            </footer>
            <p className="text-gray-500">{c.content}</p>
          </article>
        ))}
    </main>
  );
}
