import React from "react";
import Link from "next/link";

export default function Header() {
  return (
    <nav className="w-full flex justify-center border-b border-gray-200 h-16">
      <div className="w-full max-w-6xl flex justify-between items-center p-3 text-sm">
        <div className=" text-black w-full">
          <div className="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
            <div className="flex items-center">
              <h1 className="text-lg font-bold">
                <Link href="/" className="hover:text-gray-300">
                  {" "}
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
              >
                <svg
                  className="w-6 h-6"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path d="M12 2C6.48 2 2 6.48 2 12c0 4.42 2.87 8.17 6.84 9.49.5.09.68-.22.68-.48 0-.24-.01-.87-.01-1.71-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.12-1.47-1.12-1.47-.91-.62.07-.61.07-.61 1 .07 1.53 1.03 1.53 1.03.89 1.53 2.34 1.09 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.56-1.11-4.56-4.94 0-1.09.39-1.98 1.03-2.68-.1-.25-.45-1.27.1-2.65 0 0 .84-.27 2.75 1.02.8-.22 1.65-.33 2.5-.33s1.7.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02.55 1.38.2 2.4.1 2.65.64.7 1.03 1.59 1.03 2.68 0 3.84-2.34 4.69-4.57 4.94.36.31.68.92.68 1.85 0 1.34-.01 2.42-.01 2.75 0 .27.18.58.69.48A10.001 10.001 0 0 0 22 12c0-5.52-4.48-10-10-10z" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
