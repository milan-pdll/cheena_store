// Tailwind CSS design configuration with royal luxury color tokens and typography
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "1.5rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        pitch: {
          950: "#050608",
          900: "#0b0d12",
          800: "#131720",
          700: "#1d2330",
          600: "#2a3244",
        },
        gold: {
          50: "#fbf8ee",
          100: "#f5edd2",
          200: "#ebdb9f",
          300: "#dec26b",
          400: "#d4af37", // Royal Gold primary
          500: "#b89025",
          600: "#99711c",
          700: "#7a5518",
          800: "#644419",
          900: "#533718",
        },
        offwhite: {
          50: "#ffffff",
          100: "#fcfcfd",
          200: "#f5f6f8",
          300: "#e9ebef",
          400: "#d2d6df",
        },
      },
      fontFamily: {
        sans: ["var(--font-sans)", "system-ui", "sans-serif"],
        display: ["var(--font-display)", "Georgia", "serif"],
      },
      letterSpacing: {
        tightest: "-0.04em",
        widest: "0.2em",
      },
      boxShadow: {
        glow: "0 0 25px -5px rgba(212, 175, 55, 0.25)",
        luxury: "0 10px 30px -10px rgba(0, 0, 0, 0.5)",
      },
    },
  },
  plugins: [],
};

export default config;
