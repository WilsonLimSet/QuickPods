"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/utils/supabase/client";
import Header from "@/components/Header";
import PodCard from "../components/PodCard";
import Footer from "@/components/Footer";

// Define the type for your card data
interface CardData {
  id: string;
  interviewer: string;
  interviewee: string;
  insights: string[];
  thumbnail_url: string;
  youtube_url: string;
  publishDate: string;
  tag: string;
  md_slug: string;
}

export default function Index() {
  const [cards, setCards] = useState<CardData[]>([]);

  useEffect(() => {
    const init = async () => {
      try {
        const supabase = createClient();
        const { data, error } = await supabase.from("Podcasts").select("*");
        if (error) throw error;
        if (data) {
          setCards(data);
          console.log(data);
        }
      } catch (e) {
        console.error("Error connecting to Supabase", e);
      }
    };

    init();
  }, []);

  return (
    <>
      <Header />
      {/* <main className="flex w-full flex-1 flex-col items-center py-10"> */}
      <main className="flex  flex-col items-center py-10">
        <div className="grid max-w-7xl grid-cols-1 gap-3 px-2 md:grid-cols-2 lg:grid-cols-4">
          {cards.map((card, index) => (
            <PodCard key={index} {...card} />
          ))}
        </div>
      </main>

      <Footer />
    </>
  );
}
