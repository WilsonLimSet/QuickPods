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
  publish_date: string;
  tag: string;
  md_slug: string;
}

export default function Index() {
  const [cards, setCards] = useState<CardData[]>([]);
  const [sortOrder, setSortOrder] = useState("ASC"); // 'ASC' or 'DESC'

  useEffect(() => {
    const init = async () => {
      try {
        const supabase = createClient();
        let query = supabase.from("Podcasts").select("*");

        if (sortOrder === "ASC") {
          query = query.order("publish_date", { ascending: true });
        } else {
          query = query.order("publish_date", { ascending: false });
        }

        const { data, error } = await query;
        if (error) throw error;
        if (data) {
          setCards(data);
        }
      } catch (e) {
        console.error("Error connecting to Supabase", e);
      }
    };
    init();
  }, [sortOrder]);

  return (
    <>
      <Header />
      <main className="flex flex-col items-center py-10">
        <div className="mb-4">
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="rounded-md border p-2"
          >
            <option value="ASC">Sort by Earliest Date</option>
            <option value="DESC">Sort by Latest Date</option>
          </select>
        </div>
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
