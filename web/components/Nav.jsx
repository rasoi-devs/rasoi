import Link from "next/link";
import Image from "next/image";
import React from "react";

function Nav() {
  return (
    <header className="body-font mb-6 rounded-3xl bg-background-100 p-6 text-gray-600 shadow-md">
      <div className="container mx-auto flex flex-col flex-wrap items-center md:flex-row">
        <Link
          href="/"
          className="title-font mb-4 flex items-center font-medium text-gray-900 md:mb-0"
        >
          <Image
            src="/icon-512.png"
            alt="Rasoi Logo"
            width={40}
            height={40}
            priority
          />
          <span className="ml-3 text-xl">Rasoi</span>
        </Link>
        <nav className="flex flex-wrap items-center justify-center text-base md:ml-4 md:mr-auto md:border-l md:border-gray-400 md:py-1 md:pl-4">
          <Link href="/" className="mr-5 hover:text-gray-900">
            Home
          </Link>
          <Link href="/search" className="mr-5 hover:text-gray-900">
            Search
          </Link>
          <Link href="/recipes" className="mr-5 hover:text-gray-900">
            Recipes
          </Link>
          <Link href="/about" className="mr-5 hover:text-gray-900">
            About
          </Link>
        </nav>
      </div>
    </header>
  );
}

export default Nav;
