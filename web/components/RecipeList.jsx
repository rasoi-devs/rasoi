import React from "react";
import Link from "next/link";

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
            } w-[20rem] rounded-2xl bg-background-100 p-6`}
          >
            {skeleton ? (
              <>
                <div className="mb-2.5 h-4 max-w-[330px] rounded-full bg-background-300"></div>
                <div className="mb-2.5 h-4 max-w-[100px] rounded-full bg-background-300"></div>
              </>
            ) : (
              <h3 className="text-xl text-secondary-800">{r.title}</h3>
            )}
            {skeleton ? (
              <div className="h-2 max-w-[330px] rounded-full bg-background-300"></div>
            ) : (
              <p className="truncate">{r.directions.join(" ")}</p>
            )}
          </Link>
        ))
      )}
    </div>
  );
}

export default RecipeList;
