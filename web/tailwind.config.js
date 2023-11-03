/** @type {import('tailwindcss').Config} */

const colors = require("tailwindcss/colors");

// https://www.realtimecolors.com/?colors=130e01-ffffff-6c3702-00c7a9-1902d6&fonts=Poppins-Poppins

module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        text: {
          50: "#fef7e7",
          100: "#fcefcf",
          200: "#fae09e",
          300: "#f7d06e",
          400: "#f5c13d",
          500: "#f2b10d",
          600: "#c28e0a",
          700: "#916a08",
          800: "#614705",
          900: "#302303",
          950: "#181201",
        },
        background: {
          50: "#f2f2f2",
          100: "#e6e6e6",
          200: "#cccccc",
          300: "#b3b3b3",
          400: "#999999",
          500: "#808080",
          600: "#666666",
          700: "#4d4d4d",
          800: "#333333",
          900: "#1a1a1a",
          950: "#0d0d0d",
        },
        primary: {
          50: "#fef2e6",
          100: "#fee6cd",
          200: "#fdcc9b",
          300: "#fcb369",
          400: "#fb9937",
          500: "#fa8005",
          600: "#c86604",
          700: "#964c03",
          800: "#643302",
          900: "#321a01",
          950: "#190d01",
        },
        secondary: {
          50: "#e5fffb",
          100: "#ccfff7",
          200: "#99fff0",
          300: "#66ffe8",
          400: "#33ffe0",
          500: "#00ffd9",
          600: "#00ccad",
          700: "#009982",
          800: "#006657",
          900: "#00332b",
          950: "#001a16",
        },
        accent: {
          50: "#e9e6ff",
          100: "#d2cdfe",
          200: "#a69afe",
          300: "#7968fd",
          400: "#4c35fd",
          500: "#2003fc",
          600: "#1902ca",
          700: "#130297",
          800: "#0d0165",
          900: "#060132",
          950: "#030019",
        },
      },
    },
  },
  plugins: [],
};
