import { Itim } from "next/font/google";
import "./globals.css";
import Nav from "@/components/Nav";
import Footer from "@/components/Footer";

const poppins = Itim({ subsets: ["latin"], weight: "400" });

export const metadata = {
  // TODO: update base URL
  metadataBase: new URL("http://localhost:3000"),
  title: {
    default: "Rasoi",
    template: "%s | Rasoi",
  },
  description: "A social media for recipes 🍳.",
  openGraph: {
    title: {
      default: "Rasoi",
      template: "%s | Rasoi",
    },
    description: "A social media for recipes 🍳.",
    // url: "https://nextjs.org",
    siteName: "Rasoi",
    images: [
      {
        url: "/icon-512-maskable.png",
        width: 512,
        height: 512,
        alt: "Rasoi Logo",
      },
    ],
    locale: "en_US",
    type: "website",
  },
  icons: {
    icon: "/favicon.ico",
    apple: "/apple-touch-icon.png",
  },
  manifest: "/manifest.json",
  // appLinks: {
  //   ios: {
  //     url: 'https://nextjs.org/ios',
  //     app_store_id: 'app_store_id',
  //   },
  //   android: {
  //     package: 'com.example.android/package',
  //     app_name: 'app_name_android',
  //   },
  //   web: {
  //     url: 'https://nextjs.org/web',
  //     should_fallback: true,
  //   },
  // },
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`flex min-h-screen flex-col justify-between p-6 ${poppins.className}`}
      >
        <Nav />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
