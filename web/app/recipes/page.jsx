import React from "react";
import recipes from "../../public/recipes.json";
import Link from "next/link";
import generateMeta from "@/utils/meta";

export async function generateMetadata({ params, searchParams }, parent) {
  return generateMeta("Recipes", "Check out our recipe collection.");
}

function Page() {
  return (
    <>
      <h2 className="mb-3 text-3xl italic">Our Collection ✨</h2>
      <div className="flex flex-wrap justify-center gap-3">
        {recipes.length === 0 ? (
          <p className="text-xl text-red-500">No recipes!</p>
        ) : (
          recipes.map((r, idx) => (
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
    </>
  );
}

export default Page;
