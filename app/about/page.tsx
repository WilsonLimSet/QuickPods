import React from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function About() {
  return (
    <>
      <Header />
      <div className="mx-auto max-w-4xl px-4 py-8 text-center">
        <h2 className="my-8 text-3xl font-bold text-white">
          Blinkist for Podcasts 🎧
        </h2>
        <p className="mb-4 text-lg text-gray-300">
          Welcome to QuickPods, where we make discovering your next favorite
          podcast effortless through generating summaries for you to easily read
          through and determine which one is actually worth your time. 🌟
        </p>
      </div>
      <Footer />
    </>
  );
}
