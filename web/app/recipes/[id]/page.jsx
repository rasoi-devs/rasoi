import React from "react";
import recipes from "../../../public/recipes.json";
import Link from "next/link";

export async function generateMetadata({ params, searchParams }, parent) {
  const recipe = await fetchRecipe(params.id);

  return {
    title: recipe.title,
    description: recipe.directions.join(" "),
    openGraph: {
      title: recipe.title,
      description: recipe.directions.join(" "),
    },
  };
}

// export async function generateStaticParams() {
//   return recipes.map((recipe) => ({ id: recipe.id.toString() }));
// }

async function fetchRecipe(id) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/recipes/${id}`);
  if (!res.ok) throw new Error("Failed to fetch recipe");
  return res.json();
}

export default async function Page({ params: { id } }) {
  const recipe = await fetchRecipe(id);

  return (
    <main className="d-flex flex-col">
      <h1 className="mb-3 text-3xl italic">{recipe.title}</h1>

      <h2 className="mt-3 text-2xl" id="features">
        Ingredients
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.full_ingredients.map((i, idx) => (
          <li key={idx}>{i}</li>
        ))}
      </ul>

      <h2 className="mt-3 text-2xl" id="features">
        Directions
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.directions.map((d, idx) => (
          <li key={idx}>{d}</li>
        ))}
      </ul>

      <Link
        target="_blank"
        href={`https://${recipe.link}`}
        className="font-medium text-blue-600 hover:underline"
      >
        Source
      </Link>
    </main>
  );
}
