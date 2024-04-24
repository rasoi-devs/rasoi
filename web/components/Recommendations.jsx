"use client";

import React, { useCallback, useMemo, useRef, useState } from "react";
import { toast } from "react-toastify";
import RecipeList from "./RecipeList";
import InfiniteScroll from "react-infinite-scroller";
import { useRouter } from "next/navigation";

function Recommendations() {
  const router = useRouter();
  const [recipes, setRecipes] = useState([]);

  const showAuthInfo = () => {
    toast.info("Please authorize to get personalized recommendations.");
  };

  const fetchGenenralRecommendations = (page) => {
    // setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/recommendations/?page=${page}`)
      .then((res) => res.json())
      .then((jsonData) => setRecipes([...recipes, ...jsonData]))
      .catch((_) => toast.error("You might be offline!"));
    // .finally(() => setLoading(false));
  };

  const fetchRecommendations = (page = 0) => {
    // try to fetch personalized recommendations
    const accessToken = window.localStorage.getItem("accessToken");
    if (!accessToken) {
      fetchGenenralRecommendations(page);
      // don't repeat on refetch
      if (page < 1) showAuthInfo();
      return;
    }

    // setLoading(true);
    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/recommendations/personalized?page=${page}`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      },
    )
      .then((res) => res.json())
      .then((jsonData) => setRecipes([...recipes, ...jsonData]))
      .catch(() => {
        toast.error("Session expired! Please login.");
        router.push("/auth");
      });
    //   .finally(() => setLoading(false));
  };

  return (
    <InfiniteScroll
      pageStart={-1}
      loadMore={(page) => fetchRecommendations(page)}
      // FIXME: when will it end?
      hasMore={true}
      loader={<RecipeList key={0} skeleton={true} nSkeleton={3} />}
    >
      {recipes.length > 0 && <RecipeList recipes={recipes} />}
    </InfiniteScroll>
  );
}

export default Recommendations;
