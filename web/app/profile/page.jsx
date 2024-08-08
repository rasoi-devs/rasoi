"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { PieChart } from "react-minimal-pie-chart";
import uniqolor from "uniqolor";
import { useRouter } from "next/navigation";

function Page() {
  const router = useRouter();

  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [pieChartData, setPieChartData] = useState([]);

  useEffect(() => {
    // if not authenticated, send user to /auth,
    // after auth, send back to that page
    const accessToken = window.localStorage.getItem("accessToken");
    if (!accessToken) {
      router.push("/auth?next=/profile");
      toast.error("Please authenticate!");
      return;
    }

    setLoading(true);
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    })
      .then((res) => res.json())
      .then((profileJson) => {
        setProfile(profileJson);

        // generate profiling pie-chart data from history
        let recipes = [];
        for (let i = 0; i < profileJson.comments.length; i++)
          recipes.push(profileJson.comments[i].recipe);
        for (let i = 0; i < profileJson.ratings.length; i++)
          recipes.push(profileJson.ratings[i].recipe);

        let profiling = new Map();
        for (let i = 0; i < recipes.length; i++) {
          const ingredients = recipes[i].ingredients;
          for (let j = 0; j < ingredients.length; j++) {
            let freq = profiling.get(ingredients[j]) + 1 || 1;
            profiling.set(ingredients[j], freq);
          }
        }
        let chartData = [];
        for (const [k, v] of profiling) {
          chartData.push({ title: k, value: v, color: uniqolor(k).color });
        }
        // sort acc. to values (freqs)
        chartData.sort((a, b) => b.value - a.value);
        // top 20
        chartData = chartData.slice(0, 20);
        setPieChartData(chartData);
      })
      .catch(() => {
        router.push("/auth?next=/profile");
        toast.error("Please authenticate!");
        return;
      })
      .finally(() => setLoading(false));
  }, [router]);

  if (loading) {
    return (
      <div role="status" className="m-auto">
        <svg
          aria-hidden="true"
          className="inline h-10 w-10 animate-spin fill-primary-500 text-white"
          viewBox="0 0 100 101"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
            fill="currentColor"
          />
          <path
            d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
            fill="currentFill"
          />
        </svg>
        <span className="sr-only">Loading...</span>
      </div>
    );
  }

  return (
    <>
      {profile && (
        <>
          <h2 className="mt-3 text-3xl">User Profile</h2>
          <div>
            <span className="font-bold">Email:</span> {profile.email}
          </div>
          <div>
            <span className="font-bold">Active:</span>{" "}
            {profile.active ? "Yes" : "No"}
          </div>
          {profile.comments.length !== 0 && (
            <div className="mt-3">
              <h3 className="text-lg font-bold">Comments</h3>
              <ul>
                {profile.comments.map((comment) => (
                  <li key={comment.id}>
                    <Link
                      href={`/recipes/${comment.recipe_id}`}
                      target="_blank"
                      className="text-blue-500 hover:underline"
                    >
                      {comment.content}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {profile.ratings.length !== 0 && (
            <div>
              <h3 className="text-lg font-bold">Ratings</h3>
              <ul>
                {profile.ratings.map((rating) => (
                  <li key={rating.id}>
                    <Link
                      href={`/recipes/${rating.recipe_id}`}
                      className="text-blue-500 hover:underline"
                      target="_blank"
                    >
                      {rating.rate}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {pieChartData.length !== 0 && (
            <PieChart
              className="w-[20rem] self-center"
              animate={true}
              segmentsShift={5}
              radius={45}
              data={pieChartData}
              label={({ dataEntry }) => dataEntry.title}
              labelStyle={{
                fontSize: ".25rem",
                opacity: ".8",
                color: "white",
              }}
            />
          )}
        </>
      )}
    </>
  );
}

export default Page;
