"use client";

import React, { useState, useRef, useEffect, useCallback } from "react";
import { WithContext as ReactTags } from "react-tag-input";
import { toast } from "react-toastify";
import RecipeList from "@/components/RecipeList";

const KeyCodes = {
  COMMA: 188,
  ENTER: 13,
  TAB: 9,
};

const DEBOUNCE_TIMEOUT = 100; // milliseconds

function SearchByIngredients() {
  const [ingredients, setIngredients] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [emptyMessage, setEmptyMessage] = useState(
    "Start adding ingredients...",
  );

  // debounce, so that server isn't DDOSed with a flood of search queries
  const timeout = useRef(null);
  const prevInput = useRef("");

  const fetchSuggestions = (i) => {
    if (i.trim().length === 0) return;

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/ingredients-search?q=${i}`)
      .then((res) => res.json())
      .then((ingredientsJson) =>
        setSuggestions(
          ingredientsJson.map((i) => ({ id: i.name, text: i.name })),
        ),
      )
      .catch((_) => toast.error("You might be offline!"));
  };

  const fetchRecipeFromIngredients = useCallback(() => {
    if (ingredients.length === 0) {
      setRecipes([]);
      return;
    }

    const url = new URL(
      `${process.env.NEXT_PUBLIC_API_URL}/recipes-from-ingredients`,
    );
    ingredients.forEach((i) => url.searchParams.append("q", i.text));

    setLoading(true);
    fetch(url)
      .then((res) => res.json())
      .then((recipesJson) => {
        setRecipes(recipesJson);
        if (recipesJson.length === 0) setEmptyMessage("No results found!");
      })
      .catch((_) => toast.error("You might be offline!"))
      .finally(() => setLoading(false));
  }, [ingredients]);

  useEffect(() => {
    fetchRecipeFromIngredients();
  }, [ingredients, fetchRecipeFromIngredients]);

  const handleTagAddition = (tag) => {
    setIngredients([...ingredients, tag]);
  };

  return (
    <main className="flex flex-1 flex-col">
      <ReactTags
        placeholder="Coconut"
        tags={ingredients}
        delimiters={[KeyCodes.COMMA, KeyCodes.TAB, KeyCodes.ENTER]}
        handleAddition={handleTagAddition}
        handleDelete={(i) =>
          setIngredients(ingredients.filter((_, idx) => idx !== i))
        }
        suggestions={suggestions}
        allowDragDrop={false}
        handleInputChange={(val, _) => {
          // debounce
          val = val.trim();
          prevInput.current = val;
          clearTimeout(timeout.current);
          timeout.current = setTimeout(() => {
            if (val === prevInput.current && val.length !== 0) {
              fetchSuggestions(val);
            }
          }, DEBOUNCE_TIMEOUT);
        }}
        onClearAll={() => setIngredients([])}
        autofocus
        minQueryLength={1}
        inputFieldPosition="bottom"
        autocomplete
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

export default SearchByIngredients;
