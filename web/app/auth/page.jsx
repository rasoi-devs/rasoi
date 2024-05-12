"use client";

import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";
import { useRouter } from "next/navigation";

function Page() {
  const router = useRouter();

  // to get where to redirect after auth success
  const [next, setNext] = useState("/");

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [accept, setAccept] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // manually add hash fragment as well
    const urlParams = new URLSearchParams(window.location.search);
    const nextUrl = urlParams.get("next") || "/";
    const hash = window.location.hash;
    setNext(nextUrl + hash);
  }, []);

  const authHelper = (isRegister = false) => {
    setLoading(true);
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);
    const endpoint = isRegister ? "register" : "token";
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/${endpoint}`, {
      method: "post",
      body: formData,
    })
      .then((res) => res.json())
      .then((jsonData) => {
        const accessToken = jsonData.access_token;
        const user = jsonData.user;
        if (!accessToken) {
          throw Error("Can't authorize!");
        }
        window.localStorage.setItem("accessToken", accessToken);
        window.localStorage.setItem("user", JSON.stringify(user));
        toast.success("Welcome! 👋");
        router.push(next);
      })
      .catch((_) => toast.error("Can't authorize!"))
      .finally(() => setLoading(false));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !password) return;
    if (!accept) {
      toast.error("Please accept the terms!");
      return;
    }

    setLoading(true);
    // check for account's existence
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/user-exists?q=${email}`)
      .then((res) => res.json())
      .then((isExist) => {
        if (isExist) {
          // if exist, fire token fetch and store accessToken in localStorage
          authHelper();
        } else {
          // if doesn't exist, confirm account creation,
          // create account and store accessToken in localStorage
          if (window.confirm("You don't have an account, create one?")) {
            authHelper(true);
          } else {
            setLoading(false);
          }
        }
      })
      .catch((_) => toast.error("You might be offline!"));
  };

  return (
    <main className="flex flex-col items-center">
      <div className="space-y-4 rounded-lg bg-background-100/50 p-6 shadow-md sm:p-8 md:space-y-6">
        <h1 className="text-xl font-bold leading-tight tracking-tight text-gray-900 md:text-2xl">
          Authenticate yourself
        </h1>
        <form className="space-y-4 md:space-y-6" onSubmit={handleSubmit}>
          <div>
            <label
              htmlFor="email"
              className="mb-2 block text-sm font-medium text-gray-900"
            >
              Your email
            </label>
            <input
              type="email"
              name="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={loading}
              required
              className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 outline-none focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            />
          </div>
          <div>
            <label
              htmlFor="password"
              className="mb-2 block text-sm font-medium text-gray-900"
            >
              Password
            </label>
            <input
              type="password"
              name="password"
              id="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
              className="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-gray-900 outline-none focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            />
          </div>
          <div className="flex items-center justify-between">
            <div className="flex items-start">
              <div className="flex h-5 items-center">
                <input
                  id="accept"
                  aria-describedby="accept"
                  type="checkbox"
                  name="accept"
                  checked={accept}
                  onChange={(e) => setAccept(e.target.checked)}
                  required
                  disabled={loading}
                  className="focus:ring-3 h-4 w-4 cursor-pointer rounded border border-gray-300 bg-gray-50 text-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="ml-3 text-sm">
                <label
                  htmlFor="accept"
                  className="cursor-pointer text-gray-500"
                >
                  I accept that privacy is a myth.
                </label>
              </div>
            </div>
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-primary-500 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-4 focus:ring-primary-300"
          >
            {loading && (
              <svg
                aria-hidden="true"
                role="status"
                className="me-3 inline h-4 w-4 animate-spin text-gray-200"
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
                  fill="#fa8005"
                />
              </svg>
            )}
            Go!
          </button>
        </form>
      </div>
    </main>
  );
}

export default Page;
