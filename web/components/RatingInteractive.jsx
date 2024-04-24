"use client";

import { useEffect, useState } from "react";
import { Rating as ReactRating } from "@smastrom/react-rating";
import { toast } from "react-toastify";
import { useRouter } from "next/navigation";

export default function RatingInteractive({ recipeId, allRatings }) {
  const router = useRouter();
  const [rating, setRating] = useState(0);

  useEffect(() => {
    const accessToken = window.localStorage.getItem("accessToken");
    const user = JSON.parse(window.localStorage.getItem("user"));
    if (!accessToken || !user) return;

    // if current user already rated, don't allow him to rate
    // just set rating to > 0, to disable it.
    const currentUserRating = allRatings.filter(
      (r) => r.user.id === user.id,
    )[0];
    if (currentUserRating) setRating(currentUserRating.rate);
  }, [allRatings]);

  const submitRating = async (val) => {
    // if not authenticated, send user to /auth
    const accessToken = window.localStorage.getItem("accessToken");
    if (!accessToken) router.push("/auth");

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/recipes/${recipeId}/ratings`,
      {
        method: "post",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ rate: val }),
      },
    );
    if (!res.ok) {
      router.push("/auth");
      throw Error("Please authenticate!");
    }
    router.refresh();
  };

  return (
    <ReactRating
      className="max-w-[10rem]"
      value={rating}
      readOnly={rating > 0}
      onChange={(val) => {
        toast
          .promise(submitRating(val), {
            pending: "Submit rating...",
            error: "Please authenticate!",
            success: `Rated ${val} ⭐!`,
          })
          .then(() => setRating(val));
      }}
      transition="position"
    />
  );
}
