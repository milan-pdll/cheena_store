// Root layout component providing font styling, global metadata, and shell container
import type { Metadata } from "next";
import { Inter, Montserrat } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
});

const montserrat = Montserrat({
  subsets: ["latin"],
  variable: "--font-display",
  weight: ["500", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: "APEX PITCH | Premium Football Boots & Jersey Store",
  description:
    "Curated collection of match-grade football boots and authentic player edition jerseys. Direct contact purchasing via WhatsApp.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${montserrat.variable} dark`}>
      <body className="bg-pitch-900 text-offwhite-100 antialiased selection:bg-gold-400 selection:text-pitch-950">
        {children}
      </body>
    </html>
  );
}
