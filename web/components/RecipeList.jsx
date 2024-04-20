import React from "react";
import Link from "next/link";
import Image from "next/image";

function RecipeList({ recipes, emptyText = "No recipe!", skeleton = false }) {
  if (skeleton) recipes = [...Array(20).keys()];

  return (
    <div className="flex flex-wrap justify-center gap-3">
      {recipes.length === 0 ? (
        <p className="text-xl text-red-500">{emptyText}</p>
      ) : (
        recipes.map((r, idx) => (
          <Link
            href={skeleton ? "#" : `/recipes/${r.id}`}
            key={idx}
            className={`${
              skeleton && "animate-pulse"
            } w-[20rem] rounded-2xl bg-background-100 p-6 shadow-md`}
          >
            {skeleton ? (
              <>
                <div className="mb-2.5 flex h-36 items-center justify-center rounded-xl bg-background-300">
                  <svg
                    className="h-10 w-10 text-background-200"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="currentColor"
                    viewBox="0 0 20 18"
                  >
                    <path d="M18 0H2a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2Zm-5.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Zm4.376 10.481A1 1 0 0 1 16 15H4a1 1 0 0 1-.895-1.447l3.5-7A1 1 0 0 1 7.468 6a.965.965 0 0 1 .9.5l2.775 4.757 1.546-1.887a1 1 0 0 1 1.618.1l2.541 4a1 1 0 0 1 .028 1.011Z" />
                  </svg>
                </div>
                <div className="mb-2.5 h-4 max-w-[330px] rounded-full bg-background-300"></div>
                <div className="mb-2.5 h-4 max-w-[100px] rounded-full bg-background-300"></div>
              </>
            ) : (
              <>
                <div className="relative h-36">
                  <Image
                    src={`${process.env.NEXT_PUBLIC_API_URL}/recipe-images/${r.image_name}.jpg`}
                    fill
                    className="rounded-xl object-cover"
                    alt={`${r.title} image`}
                  />
                </div>
                <h3 className="text-xl text-secondary-800">{r.title}</h3>
              </>
            )}
            {skeleton ? (
              <div className="h-2 max-w-[330px] rounded-full bg-background-300"></div>
            ) : (
              <p className="truncate">{r.instructions.join(" ")}</p>
            )}
          </Link>
        ))
      )}
    </div>
  );
}

export default RecipeList;
