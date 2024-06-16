"use client";

import { useEffect, useState, useCallback } from "react";
import { createClient } from "@/utils/supabase/client";
import Header from "@/components/Header";
import dynamic from "next/dynamic";
import Footer from "@/components/Footer";
import { useInView } from "react-intersection-observer";
import SkeletonPodCard from "@/components/SkeletonPodCard";
import { debounce } from "lodash";

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
  blog_content: string;
}

const LazyPodCard = dynamic(() => import("../components/PodCard"), {
  ssr: false,
  loading: () => <p>Loading...</p>,
});

export default function Index() {
  const [cards, setCards] = useState<CardData[]>([]);
  const [isLoadingInitial, setIsLoadingInitial] = useState(true); // Track initial loading
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [sortOrder, setSortOrder] = useState("DESC"); // Default to 'DESC' for most recent
  const { ref, inView } = useInView({ threshold: 0.5, triggerOnce: false });
  const [searchQuery, setSearchQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState(searchQuery);

  const fetchInitialData = useCallback(async () => {
    try {
      const supabase = createClient();
      let query = supabase
        .from("Podcasts")
        .select("*")
        .order("publish_date", { ascending: sortOrder === "ASC" })
        .limit(8); // Limit to 8 items initially for faster loading

      const { data, error } = await query;
      if (error) throw error;
      setCards(data || []);
      setHasMore(data?.length === 8); // Adjust according to the new limit
      setIsLoadingInitial(false); // Set to false once data is loaded
    } catch (e) {
      console.error("Error connecting to Supabase", e);
      setIsLoadingInitial(false); // Ensure loading state is updated even on error
    }
  }, [sortOrder]);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  useEffect(() => {
    const handler = debounce(() => {
      setDebouncedQuery(searchQuery);
    }, 300); // Adjust timing as needed

    handler();
    return () => handler.cancel();
  }, [searchQuery]);

  const fetchMorePodcasts = useCallback(async () => {
    if (!isLoadingMore && hasMore && cards.length > 0) {
      setIsLoadingMore(true);
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
      setIsLoadingMore(false);
    }
  }, [cards, isLoadingMore, hasMore, sortOrder]);

  useEffect(() => {
    if (inView && hasMore) {
      fetchMorePodcasts();
    }
  }, [inView, fetchMorePodcasts]);

  const filteredCards = cards.filter((card) =>
    (card.blog_content || "")
      .toLowerCase()
      .includes((searchQuery || "").toLowerCase()),
  );

  return (
    <>
      <Header />
      <main className="flex flex-col items-center py-10">
        <div className="mb-4 items-center space-x-2">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search"
            className="rounded-md border bg-background p-2 text-foreground"
          />
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="rounded-md border bg-background p-2 text-foreground"
          >
            <option value="ASC">Sort by Earliest Date</option>
            <option value="DESC">Sort by Latest Date</option>
          </select>
        </div>
        <div className="grid max-w-7xl grid-cols-1 gap-3 px-2 md:grid-cols-2 lg:grid-cols-4">
          {isLoadingInitial ? (
            Array.from({ length: 8 }, (_, index) => (
              <SkeletonPodCard key={index} />
            ))
          ) : filteredCards.length > 0 ? (
            filteredCards.map((card) => (
              <LazyPodCard key={`${card.id}-${card.publish_date}`} {...card} />
            ))
          ) : (
            <div>No results found.</div>
          )}
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
