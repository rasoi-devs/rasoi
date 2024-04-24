"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "react-toastify";

function CommentInteractive({ recipeId }) {
  const router = useRouter();
  const [comment, setComment] = useState("");

  const warnAuth = () => {
    // on pressing the comment entry textbox,
    // check auth status and fire warning
    const accessToken = window.localStorage.getItem("accessToken");
    if (!accessToken) {
      toast.warn("Please authenticate to post comment!");
      return null;
    }
    return accessToken;
  };

  const submitComment = async (e) => {
    e.preventDefault();

    // if not authenticated, send user to /auth
    const accessToken = warnAuth();
    if (!accessToken) {
      router.push("/auth");
      return;
    }

    const cmnt = comment.trim();
    if (cmnt.length === 0) return;

    const res = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/recipes/${recipeId}/comments`,
      {
        method: "post",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ content: cmnt }),
      },
    );
    if (!res.ok) {
      router.push("/auth");
      throw Error("Please authenticate!");
    }
    router.refresh();
  };

  return (
    <form
      onSubmit={(e) =>
        toast.promise(submitComment(e), {
          pending: "Submit comment...",
          error: "Please authenticate!",
          success: "Thanks for sharing your thoughts 🙌",
        })
      }
    >
      <div className="mb-4 rounded-lg rounded-t-lg border border-gray-200 bg-white px-4 py-2">
        <label htmlFor="comment" className="sr-only">
          Your comment
        </label>
        <textarea
          id="comment"
          rows="4"
          className="w-full border-0 px-0 text-sm text-gray-900 focus:outline-none focus:ring-0"
          placeholder="Write a comment..."
          required
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          onClick={warnAuth}
        />
      </div>
      <button
        type="submit"
        className="inline-flex items-center rounded-lg bg-primary-500 px-4 py-2.5 text-center text-xs font-medium text-white outline-none hover:bg-primary-700 focus:ring-4 focus:ring-primary-200"
      >
        Post comment
      </button>
    </form>
  );
}

export default CommentInteractive;
