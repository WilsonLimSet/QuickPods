import React from "react";
import Header from "@/components/Header";

export default function About() {
  return (
    //<div className="container mx-auto px-4 py-8">
    //<div className="flex-1 w-full flex flex-col items-center bg-gray-100">
    <>
      <Header />
      <h2 className="mb-4 text-center text-2xl font-light">
        Just a bunch of pods (podcast-lovers) 🎙️
      </h2>
      <div className="my-8 grid grid-cols-1 gap-4 md:grid-cols-3">
        <img
          src="/path/to/image1.jpg"
          alt="Image description"
          className="h-auto w-full"
        />
        <img
          src="/path/to/image2.jpg"
          alt="Image description"
          className="h-auto w-full"
        />
        <img
          src="/path/to/image3.jpg"
          alt="Image description"
          className="h-auto w-full"
        />
      </div>
      <p className="mb-4 text-lg">
        At Cocoa Pods, we leverage the Reflex framework and Gemini AI technology
        to transform how you experience podcasts. Reflex optimizes the user
        interface, making navigation both intuitive and fluid, while Gemini AI
        enhances content analysis, meticulously listening for and extracting key
        insights from each podcast. This synergy ensures that our platform not
        only simplifies discovery but also tailors personalized recommendations
        to your unique interests.
      </p>
      <p className="mb-4 text-lg">
        Understanding the challenges of the vast daily podcast releases, Cocoa
        Pods distills and condenses each podcast into concise insights. Starting
        from our minimalistic landing page, you can easily filter by date or
        topic to access podcasts that offer unique insights, capturing the
        essence without the clutter. Join Cocoa Pods' community to connect
        deeply with the topics you care about, all through a platform that's as
        insightful as it is straightforward.
      </p>
      <p className="text-lg">May we too, cross paths in a podcast one day 👋</p>
    </>
  );
}
