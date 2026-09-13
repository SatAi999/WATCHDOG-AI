import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "WATCHDOG — Autonomous Web Intelligence & Action Agent",
  description: "Don't just watch the web. Understand what changed, why it matters, and what should happen next.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#08090d] text-slate-100 antialiased font-sans">
        {children}
      </body>
    </html>
  );
}
