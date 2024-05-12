import Recommendations from "@/components/Recommendations";
import Link from "next/link";

// async function getRecommendations() {
//   const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/recommendations`);
//   if (!res.ok) throw new Error("Failed to fetch recommendations");
//   return res.json();
// }

export default function Home() {
  // const recommendations = await getRecommendations();

  return (
    <main>
      <h2 className="mb-3 text-3xl italic">Top picks for you 👌</h2>

      <Recommendations />

      <Link
        href="/recipes/add"
        className="zoomInOut fixed bottom-10 right-10 mx-auto flex cursor-pointer items-center rounded-full border-0 bg-primary-500 px-8 py-4 text-xl text-white hover:bg-primary-700 focus:outline-none"
      >
        <svg
          // class="h-6 w-6 text-gray-800 dark:text-white"
          aria-hidden="true"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 12h14m-7 7V5"
          />
        </svg>
        Add recipe
      </Link>
    </main>
  );
}
