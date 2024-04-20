"use client";

import React, { useState, useEffect } from "react";
import { toast } from "react-toastify";
import RecipeList from "./RecipeList";

function Recommendations() {
  const [recipes, setRecipes] = useState([]);
  const [loading, setLoading] = useState(true);

  const showAuthInfo = () => {
    toast.info(
      "Please authorize to get personalized recommendations.",
    );
  };

  const fetchGenenralRecommendations = () => {
    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/recommendations`)
      .then((res) => res.json())
      .then((jsonData) => setRecipes(jsonData))
      .catch((_) => toast.error("You might be offline!"))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    // try to fetch personalized recommendations
    const accessToken = window.localStorage.getItem("accessToken");
    if (!accessToken) {
      showAuthInfo();
      fetchGenenralRecommendations();
      return;
    }

    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/recommendations/personalized`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => res.json())
      .then((jsonData) => setRecipes(jsonData))
      .catch(() => {
        showAuthInfo();
        // show general recommendations as fallback
        fetchGenenralRecommendations();
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <RecipeList
      skeleton={loading}
      recipes={recipes}
      emptyText="No recommendation!"
    />
  );
}

export default Recommendations;
