"use client";

import React, { useState } from "react";
import { useTranslations } from "next-intl";

export default function NewsletterSignup() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [message, setMessage] = useState("");
  const t = useTranslations("newsletter");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");

    try {
      const response = await fetch("/api/newsletter", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        throw new Error("Failed to subscribe");
      }

      setStatus("success");
      setMessage(t("successMessage"));
      setEmail("");
    } catch (error) {
      setStatus("error");
      setMessage(t("errorMessage"));
    }
  };

  return (
    <div className="w-full rounded-lg border border-gray-700 bg-gray-900 p-6">
      <h3 className="mb-2 text-xl font-bold text-white">{t("title")}</h3>
      <p className="mb-4 text-gray-300">{t("description")}</p>

      <form onSubmit={handleSubmit} className="flex flex-col gap-3 sm:flex-row">
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder={t("emailPlaceholder")}
          required
          disabled={status === "loading"}
          className="flex-1 rounded-md border border-gray-700 bg-gray-800 px-4 py-2 text-white placeholder-gray-400 focus:border-blue-500 focus:outline-none disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={status === "loading"}
          className="rounded-md bg-blue-600 px-6 py-2 font-semibold text-white transition-colors hover:bg-blue-700 disabled:opacity-50"
        >
          {status === "loading" ? t("subscribing") : t("subscribe")}
        </button>
      </form>

      {status === "success" && (
        <p className="mt-3 text-sm text-green-400">{message}</p>
      )}
      {status === "error" && (
        <p className="mt-3 text-sm text-red-400">{message}</p>
      )}

      <p className="mt-3 text-xs text-gray-500">{t("privacyNote")}</p>
    </div>
  );
}
