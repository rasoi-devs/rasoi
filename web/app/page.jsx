import Image from "next/image";
import Link from "next/link";
import recipes from "../public/recipes.json";
import RecipeList from "@/components/RecipeList";

// async function getRecommendations() {
//   const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/recommendations`);
//   if (!res.ok) throw new Error("Failed to fetch recommendations");
//   return res.json();
// }

export default async function Home() {
  // const recommendations = await getRecommendations();
  const recommendations = recipes.slice(0, 6);

  return (
    <main>
      <h2 className="mb-3 text-3xl italic">Top picks for you 👌</h2>
      <RecipeList recipes={recommendations} emptyText="No recommendation!" />

      <Link
        href="/search"
        className="zoomInOut mx-auto mt-3 flex w-fit rounded-full border-0 bg-primary-500 px-10 py-4 text-3xl text-white hover:bg-primary-700 focus:outline-none"
      >
        More -&gt;
      </Link>
    </main>
  );
}
