"use client";

import { useEffect, useState, useCallback } from "react";
import { createClient } from "@/utils/supabase/client";
import Header from "@/components/Header";
import dynamic from "next/dynamic";
import Footer from "@/components/Footer";
import { useInView } from "react-intersection-observer";

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

const LazyPodCard = dynamic(() => import("../components/PodCard"), {
  ssr: false,
});

export default function Index() {
  const [cards, setCards] = useState<CardData[]>([]);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [sortOrder, setSortOrder] = useState("ASC"); // 'ASC' or 'DESC'
  const { ref, inView } = useInView({ threshold: 0.5, triggerOnce: false });

  const fetchInitialData = useCallback(async () => {
    try {
      const supabase = createClient();
      let query = supabase
        .from("Podcasts")
        .select("*")
        .order("publish_date", { ascending: sortOrder === "ASC" });

      const { data, error } = await query.range(0, 9);
      if (error) throw error;
      setCards(data || []);
      setHasMore(data?.length === 10);
    } catch (e) {
      console.error("Error connecting to Supabase", e);
    }
  }, [sortOrder]);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  const fetchMorePodcasts = useCallback(async () => {
    if (!isLoadingMore && hasMore && cards.length > 0) {
      setIsLoadingMore(true);
      try {
        const supabase = createClient();
        const lastCard = cards[cards.length - 1];
        let query = supabase
          .from("Podcasts")
          .select("*")
          .order("publish_date", { ascending: sortOrder === "ASC" })
          .limit(10);

        if (sortOrder === "ASC") {
          query = query.gt("publish_date", lastCard.publish_date);
        } else {
          query = query.lt("publish_date", lastCard.publish_date);
        }

        const { data, error } = await query;
        if (error) throw error;
        if (data) {
          const existingIds = new Set(cards.map((card) => card.id));
          const newItems = data.filter((item) => !existingIds.has(item.id));
          setCards((prev) => [...prev, ...newItems]);
          setHasMore(data.length === 10);
        }
      } catch (e) {
        console.error("Error fetching more podcasts", e);
      } finally {
        setIsLoadingMore(false);
      }
    }
  }, [cards, isLoadingMore, hasMore, sortOrder]);

  useEffect(() => {
    if (inView && hasMore) {
      fetchMorePodcasts();
    }
  }, [inView, fetchMorePodcasts]);

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
          {cards.map((card) => (
            <LazyPodCard key={`${card.id}-${card.publish_date}`} {...card} />
          ))}
        </div>
        {isLoadingMore && (
          <div className="loading-indicator">Loading More...</div>
        )}
        <div ref={ref} style={{ height: "20px", width: "100%" }} />
      </main>
      <Footer />
    </>
  );
}
