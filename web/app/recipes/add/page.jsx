"use client";

import React, { useState } from "react";
import { toast } from "react-toastify";

function Page() {
  const [ingredients, setIngredients] = useState([""]);
  const [instructions, setInstructions] = useState([""]);
  const [shortIngredients, setShortIngredients] = useState([]);
  const [loadingShortIngredients, setLoadingShortIngredients] = useState(false);

  return (
    <form className="flex min-h-[20rem] flex-col">
      <legend className="text-3xl italic text-accent-500">Add recipe</legend>

      <section id="title" className="mt-3">
        <label htmlFor="inp-title" className="text-md text-accent-600">
          Title
        </label>
        <input
          type="text"
          id="inp-title"
          className="block w-full rounded-xl border-2 p-2 text-gray-900 outline-none focus:border-primary-500 focus:ring-primary-500"
          placeholder="john.doe@company.com"
          required
        />
      </section>

      <section id="instructions" className="mt-3">
        <label className="text-md text-accent-600">Instructions</label>
        {instructions.map((ins, idx) => (
          <div key={idx} className="flex gap-2">
            <input
              type="text"
              className="mt-1 block w-full rounded-xl border-2 p-2 text-gray-900 outline-none focus:border-primary-500 focus:ring-primary-500"
              placeholder="john.doe@company.com"
              required={idx !== instructions.length - 1}
              value={ins}
              onChange={(e) => {
                const val = e.target.value.trim();
                let newInstructions = [...instructions];
                newInstructions[idx] = val;
                if (newInstructions.at(-1) !== "") newInstructions.push("");
                setInstructions(newInstructions);
              }}
            />
            {idx !== instructions.length - 1 && (
              <button
                onClick={() =>
                  setInstructions(instructions.filter((_, ix) => ix !== idx))
                }
              >
                ❌
              </button>
            )}
          </div>
        ))}
      </section>

      <section id="ingredients" className="mt-3">
        <label className="text-md text-accent-600">Ingredients</label>
        {ingredients.map((ig, igx) => (
          <div key={igx} className="flex gap-2">
            <input
              type="text"
              className="mt-1 block w-full rounded-xl border-2 p-2 text-gray-900 outline-none focus:border-primary-500 focus:ring-primary-500"
              placeholder="john.doe@company.com"
              required={igx !== ingredients.length - 1}
              value={ig}
              onChange={(e) => {
                const val = e.target.value.trim();
                let newIngredients = [...ingredients];
                newIngredients[igx] = val;
                if (newIngredients.at(-1) !== "") newIngredients.push("");
                setIngredients(newIngredients);
              }}
            />
            {igx !== ingredients.length - 1 && (
              <button
                onClick={() =>
                  setIngredients(ingredients.filter((_, idx) => idx !== igx))
                }
              >
                ❌
              </button>
            )}
          </div>
        ))}
      </section>

      <button
        className="mt-3 self-center rounded-lg bg-secondary-600 px-4 py-2.5 text-center text-xl font-medium text-black outline-none focus:ring-4 focus:ring-secondary-200 enabled:cursor-pointer enabled:hover:bg-secondary-800 disabled:opacity-50"
        disabled={
          loadingShortIngredients ||
          (ingredients.length === 1 && ingredients[0] === "")
        }
        onClick={(e) => {
          e.preventDefault();
          const url = new URL(
            `${process.env.NEXT_PUBLIC_API_URL}/short-ingredients`,
          );
          ingredients.forEach((i) => url.searchParams.append("q", i));
          setLoadingShortIngredients(true);
          fetch(url)
            .then((res) => res.json())
            .then((shortIngredientsJson) => {
              // FIXME: not working
              if (shortIngredientsJson.length === 0)
                toast.warn("Ingredients cannot be extracted!");
              setShortIngredients(shortIngredientsJson);
            })
            .catch((_) => toast.error("You might be offline!"))
            .finally(() => setLoadingShortIngredients(false));
        }}
      >
        Fetch Short ingredients
      </button>

      {shortIngredients.length !== 0 && (
        <section id="short-ingredients" className="mt-3">
          <h3 className="text-md text-accent-600">Short ingredients</h3>
          <ul>
            {shortIngredients.map((shi, idx) => (
              <li key={idx}>{shi}</li>
            ))}
          </ul>
        </section>
      )}

      <button
        disabled={shortIngredients.length < 1}
        className="mt-3 self-center rounded-lg bg-primary-500 px-4 py-2.5 text-center text-xl font-medium text-white outline-none focus:ring-4 focus:ring-primary-200 enabled:cursor-pointer enabled:hover:bg-primary-700 disabled:opacity-50"
      >
        Submit
      </button>
    </form>
  );
}

export default Page;
