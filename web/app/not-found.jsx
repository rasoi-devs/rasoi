import Link from "next/link";

export default function NotFound() {
  return (
    <div className="w-max m-auto">
      <h2 className="text-3xl font-bold">404 Food Not Found</h2>
      <p>Could not find requested resource</p>
      <Link className="font-medium text-blue-600 hover:underline" href="/">
        Return Home
      </Link>
    </div>
  );
}
