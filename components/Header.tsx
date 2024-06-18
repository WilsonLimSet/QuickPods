import React from "react";
import Link from "next/link";

export default function Header() {
  return (
    <nav
      className="w-full flex justify-center border-b border-gray-700 h-16"
      style={{ backgroundColor: "var(--background)" }}
    >
      <div
        className="w-full max-w-6xl flex justify-between items-center p-3 text-sm"
        style={{ color: "var(--foreground)" }}
      >
        <div className="flex items-center">
          <h1 className="text-lg font-bold">
            <Link href="/" className="hover:text-gray-300">
              CEO Insights
            </Link>
          </h1>
        </div>
        <div className="flex gap-8 items-center">
          <Link href="/about" className="hover:text-gray-300">
            About
          </Link>
          <Link href="/blog" className="hover:text-gray-300">
            Blog
          </Link>
          <Link
            href="https://ceoinsights.canny.io/feature-requests"
            className="hover:text-gray-300"
            target="_blank"
          >
            Roadmap
          </Link>
          <a
            href="https://github.com/WilsonLimSet/ceo-insights"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-300"
          >
            <img
              src="/github-mark-white.svg"
              alt="GitHub"
              className="w-6 h-6"
            />
          </a>
        </div>
      </div>
    </nav>
  );
}
