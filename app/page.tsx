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
    <div className="flex-1 w-full flex flex-col items-center bg-gray-100">
      <nav className="w-full flex justify-center border-b border-gray-200 h-16">
        
     
        <div className="w-full max-w-6xl flex justify-between items-center p-3 text-sm">
           <Header />
        </div>
      </nav>

      <main className="flex-1 w-full flex flex-col items-center py-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3 px-2 max-w-6xl">
          {cards.map((card, index) => (
            <PodCard key={index} {...card} />
          ))}
        </div>
      </main>

      <Footer />
    </div>
  );
}

