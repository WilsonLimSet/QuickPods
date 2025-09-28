import React from "react";
import Link from "next/link";
import ThemeToggle from "./ThemeToggle";
import Image from "next/image";

export default function Header() {
  return (
    <nav
      className="flex h-16 w-full justify-center border-b border-gray-700"
      style={{ backgroundColor: "var(--background)" }}
    >
      <div
        className="flex w-full max-w-6xl items-center justify-between p-3 text-sm"
        style={{ color: "var(--foreground)" }}
      >
        <div className="flex items-center">
          <h1 className="text-lg font-bold">
            <Link href="/" className="hover:text-gray-300">
              QuickPods
            </Link>
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <Link href="/about" className="hover:text-gray-300">
            About
          </Link>
          <a
            href="https://github.com/WilsonLimSet/QuickPods"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-gray-300"
          >
            <Image
              src="/github-mark-white.svg"
              alt="GitHub"
              width={24}
              height={24}
            />
          </a>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  );
}
