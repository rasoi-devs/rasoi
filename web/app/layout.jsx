import { Itim } from "next/font/google";
import "./globals.css";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";
import generateMeta from "@/utils/meta";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

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
        <Nav />
        {children}
        <ToastContainer position="bottom-right" />
        <Footer />
      </body>
    </html>
  );
}
