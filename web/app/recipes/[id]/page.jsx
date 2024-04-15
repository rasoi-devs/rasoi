import React from "react";
import recipes from "../../../public/recipes.json";
import Image from "next/image";

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
    <main className="flex flex-col">
      <h1 className="mb-3 text-3xl italic">{recipe.title}</h1>

      <Image
        src={`${process.env.NEXT_PUBLIC_API_URL}/recipe-images/${recipe.image_name}.jpg`}
        width={500}
        height={500}
        className="rounded-xl shadow-md self-center"
        alt={`${recipe.title} image`}
      />

      <h2 className="mt-3 text-2xl" id="instructions">
        Instructions
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.instructions.map((d, idx) => (
          <li key={idx}>{d}</li>
        ))}
      </ul>

      <h2 className="mt-3 text-2xl" id="ingredients">
        Ingredients
      </h2>
      <ul className="list-inside list-disc space-y-1">
        {recipe.ingredients_full.map((i, idx) => (
          <li key={idx}>{i}</li>
        ))}
      </ul>
    </main>
  );
}
