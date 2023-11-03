import React from "react";

export const metadata = {
  title: "Search",
  description: "Select search method.",
  openGraph: { title: "Search" },
};

function Search() {
  return (
    <div className="flex min-h-40 flex-row flex-wrap items-center justify-center gap-5">
      <button className="flex max-h-20 min-w-[15rem] flex-row items-center rounded-2xl bg-primary-500 px-6 py-12 text-3xl text-black hover:bg-primary-700">
        🔍 ingredients
      </button>

      <div className="hidden h-full w-[5rem] sm:block">
        <div className="h-40 w-1/2 border-r-2 border-background-200"></div>
      </div>

      <button className="flex max-h-20 min-w-[15rem] flex-row items-center rounded-2xl bg-secondary-500 px-6 py-12 text-3xl text-black hover:bg-secondary-700">
        🔍 dish name
      </button>
    </div>
  );
}

export default Search;
