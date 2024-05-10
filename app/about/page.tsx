import React from 'react';
import Header from '@/components/Header';

export default function About() {
  return (
    <div className="container mx-auto px-4 py-8">
      <Header />
      <h2 className="text-center text-2xl font-light mb-4">Just a bunch of pods (podcast-lovers) 🎙️</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-8">
        <img src="/path/to/image1.jpg" alt="Image description" className="w-full h-auto" />
        <img src="/path/to/image2.jpg" alt="Image description" className="w-full h-auto" />
        <img src="/path/to/image3.jpg" alt="Image description" className="w-full h-auto" />
      </div>
      <p className="text-lg mb-4">
        At Cocoa Pods, we leverage the Reflex framework and Gemini AI technology to transform how you experience podcasts. Reflex optimizes the user interface, making navigation both intuitive and fluid, while Gemini AI enhances content analysis, meticulously listening for and extracting key insights from each podcast. This synergy ensures that our platform not only simplifies discovery but also tailors personalized recommendations to your unique interests.
      </p>
      <p className="text-lg mb-4">
        Understanding the challenges of the vast daily podcast releases, Cocoa Pods distills and condenses each podcast into concise insights. Starting from our minimalistic landing page, you can easily filter by date or topic to access podcasts that offer unique insights, capturing the essence without the clutter. Join Cocoa Pods' community to connect deeply with the topics you care about, all through a platform that's as insightful as it is straightforward.
      </p>
      <p className="text-lg">
        May we too, cross paths in a podcast one day 👋
      </p>
    </div>
  );
}
