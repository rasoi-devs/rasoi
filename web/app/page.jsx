import Image from "next/image";
import Link from "next/link";
import recipes from "../public/recipes.json";

// async function getRecommendations() {
//   const res = await fetch(`${process.env.API_URL}/recommendations`);
//   if (!res.ok) throw new Error("Failed to fetch recommendations");
//   return res.json();
// }

export default async function Home() {
  // const recommendations = await getRecommendations();
  const recommendations = recipes.slice(0, 6);

  return (
    <>
      <h2 className="mb-3 text-3xl italic">Top picks for you 👌</h2>
      <div className="flex flex-wrap justify-center gap-3">
        {recommendations.length === 0 ? (
          <p className="text-xl text-red-500">No recommendation!</p>
        ) : (
          recommendations.map((r, idx) => (
            <Link
              href={`/recipes/${r.id}`}
              key={idx}
              className="w-[20rem] rounded-2xl bg-background-100 p-6"
            >
              <h3 className="text-xl text-secondary-800">{r.title}</h3>
              <p className="truncate">{r.directions.join(" ")}</p>
            </Link>
          ))
        )}
      </div>

      <Link
        href="/search"
        className="zoomInOut mx-auto mt-3 flex w-fit rounded-full border-0 bg-primary-500 px-10 py-4 text-3xl text-white hover:bg-primary-700 focus:outline-none"
      >
        More -&gt;
      </Link>
    </>
  );
}
