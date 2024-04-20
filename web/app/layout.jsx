import "./globals.css";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import generateMeta from "@/utils/meta";
import Image from "next/image";

import { Itim } from "next/font/google";
import bgSvg from "./bg.svg";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import '@smastrom/react-rating/style.css'

const poppins = Itim({ subsets: ["latin"], weight: "400" });

export async function generateMetadata({ params, searchParams }, parent) {
  return generateMeta();
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`flex min-h-screen flex-col justify-between p-6 ${poppins.className}`}
      >
        <Image
          src={bgSvg}
          alt="Background top"
          quality={100}
          fill
          className="object-cover opacity-50 -z-20"
        />
        <Nav />
        {children}
        <ToastContainer position="bottom-right" />
        <Footer />
      </body>
    </html>
  );
}
