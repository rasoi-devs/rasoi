"use client";

import React, { useEffect, useRef, useState } from "react";
import { toast } from "react-toastify";
import RecipeList from "@/components/RecipeList";

const DEBOUNCE_TIMEOUT = 500; //milliseconds

function SearchByName() {
  const [input, setInput] = useState("");
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [emptyMessage, setEmptyMessage] = useState("Start searching...");

  // debounce, so that server isn't DDOSed with a flood of search queries
  const timeout = useRef(null);
  const prevInput = useRef("");

  const search = (i) => {
    if (i.trim().length === 0) return;

    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/recipes-search?q=${i}`)
      .then((res) => res.json())
      .then((recipesJson) => {
        setRecipes(recipesJson);
        if (recipesJson.length === 0) setEmptyMessage("No results found!");
      })
      .catch((_) => toast.error("You might be offline!"))
      .finally(() => setLoading(false));
  };

  return (
    <main className="flex flex-1 flex-col">
      <input
        className="block w-full rounded-xl border-2 border-gray-300 bg-gray-50 p-4 text-lg text-gray-900 focus:border-primary-500 focus:outline-none focus:ring-primary-500"
        placeholder="Coconut"
        autoFocus
        value={input}
        onInput={(e) => {
          let i = e.target.value;
          setInput(i);
          if (i.trim().length === 0) setEmptyMessage("Start searching...");

          // debounce
          i = i.trim();
          prevInput.current = i;
          clearTimeout(timeout.current);
          timeout.current = setTimeout(() => {
            if (i === prevInput.current && i.length !== 0) {
              // console.log("srch", i, prevInput.current);
              search(i);
            }
          }, DEBOUNCE_TIMEOUT);
        }}
      />

      <div className="p-2"></div>

      <RecipeList
        recipes={recipes}
        skeleton={loading}
        emptyText={emptyMessage}
      />
    </main>
  );
}

export default SearchByName;
