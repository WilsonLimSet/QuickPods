"use client";

import { useTranslations } from "next-intl";

export default function Footer() {
  const t = useTranslations("footer");

  return (
    <footer className="flex w-full justify-center border-t border-gray-700 p-8 text-center text-sm text-gray-300">
      <p>
        {t("builtBy")}{" "}
        <a
          href="https://wilsonlimsetiawan.com/"
          target="_blank"
          className="font-bold text-white hover:underline"
          rel="noreferrer"
        >
          @wilsonlimset
        </a>
      </p>
    </footer>
  );
}
