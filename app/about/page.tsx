import React from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function About() {
  return (
    <>
      <Header />
      <h2 className="my-8 text-center text-2xl font-bold text-black">
        Effortless Podcast Discovery 🎧
      </h2>
      <div className="mx-auto max-w-4xl px-4 py-8">
        <p className="mb-4 text-center text-lg  text-black ">
          Welcome to CEO Insights, where we make discovering your next favorite
          podcast effortless through generating summaries for you to easily read
          through and determine which one is actually worth your time. 🌟
        </p>
      </div>
      <Footer />
    </>
  );
}
