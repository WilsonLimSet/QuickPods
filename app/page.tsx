"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/utils/supabase/client";
import Header from "@/components/Header";
import Card from "../components/PodCard";
import Footer from "@/components/Footer";

// Define the type for your card data
interface CardData {
  id: string;
  interviewer: string;
  interviewee: string;
  insights: string[];
  thumbnail_url: string;
  youtubeUrl: string;
  publishDate: string;
  tag: string;
}

export default function Index() {
  const [cards, setCards] = useState<CardData[]>([]); // Use the CardData type
  const [isSupabaseConnected, setIsSupabaseConnected] = useState(false);

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
        setIsSupabaseConnected(true);
      } catch (e) {
        console.error("Error connecting to Supabase", e);
        setIsSupabaseConnected(false);
      }
    };

    init();
  }, []);

  return (
    <div className="flex-1 w-full flex flex-col gap-20 items-center">
      <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
      CEO Insights

        <div className="w-full max-w-4xl flex justify-between items-center p-3 text-sm">
          {isSupabaseConnected}
        </div>
      </nav>

      <div className="animate-in flex-1 flex flex-col gap-20 opacity-0 max-w-6xl px-3">
 
  <main className="flex flex-wrap justify-center items-start gap-6">
    <h2 className="w-full text-center font-bold text-4xl mb-4">CEO Insights</h2>
    {cards.map((card, index) => (
      <div className="w-full sm:w-1/2 md:w-1/3 p-4" key={index}>
        <Card {...card} />
      </div>
    ))}
  </main>
</div>
      <Footer />
    </div>
  );
}
