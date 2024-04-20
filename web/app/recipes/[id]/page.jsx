import React from "react";
import Image from "next/image";
import RecipeList from "@/components/RecipeList";
import RatingInteractive from "@/components/RatingInteractive";
import { Rating } from "@smastrom/react-rating";

export async function generateMetadata({ params, searchParams }, parent) {
  const recipe = await fetchRecipe(params.id);

  return {
    title: recipe.title,
    description: recipe.instructions.join(" "),
    openGraph: {
      title: recipe.title,
      description: recipe.instructions.join(" "),
    },
  };
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

export default async function Page({ params: { id } }) {
  const recipe = await fetchRecipe(id);
  const similarRecipes = await fetchSimilarRecipes(id);
  const ratings = await fetchRatings(id);
  const totalRating = ratings.map((r) => r.rate).reduce((a, b) => a + b, 0);
  let avgRating = 0;
  if (ratings.length > 0) avgRating = Math.round(totalRating / ratings.length);

  return (
    <main className="flex flex-col">
      <h1 className="mb-3 text-3xl italic text-accent-500">{recipe.title}</h1>

      <Image
        src={`${process.env.NEXT_PUBLIC_API_URL}/recipe-images/${recipe.image_name}.jpg`}
        width={500}
        height={500}
        className="self-center rounded-xl shadow-md"
        alt={`${recipe.title} image`}
      />

      {totalRating > 0 ? (
        <div className="mt-3 flex flex-row items-center gap-10 text-xl text-accent-500">
          <p>Rated {avgRating}</p>
          <Rating readOnly value={avgRating} className="max-w-[10rem]" />
        </div>
      ) : (
        <p className="mt-3 text-xl">
          Be the <span className="text-secondary-500">first</span> to rate this
          item!
        </p>
      )}

      <div className="mt-3 flex flex-row items-center gap-2 text-xl">
        <p>
          Your <span className="text-secondary-500">rating</span>:
        </p>
        <RatingInteractive recipeId={recipe.id} allRatings={ratings} />
      </div>

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

      <h2 className="mt-4 text-2xl text-accent-500">You may also like 😋</h2>
      <RecipeList recipes={similarRecipes} />
    </main>
  );
}
