"use client";

import { useEffect, useState, useCallback } from "react";
import { createClient } from "@/utils/supabase/client";
import Header from "@/components/Header";
import dynamic from "next/dynamic";
import Footer from "@/components/Footer";
import NewsletterSignup from "@/components/NewsletterSignup";
import { useInView } from "react-intersection-observer";
import SkeletonPodCard from "@/components/SkeletonPodCard";
import { useTranslations } from "next-intl";

interface CardData {
  id: number;
  interviewer: string;
  interviewee: string;
  insights: string[];
  thumbnail_url: string;
  publish_date: string;
  tag: string;
  md_slug: string;
  blog_content: string;
  views: number;
}

const LazyPodCard = dynamic(() => import("@/components/PodCard"), {
  ssr: false,
  loading: () => <p>Loading...</p>,
});

export default function Index({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const [cards, setCards] = useState<CardData[]>([]);
  const [isLoadingInitial, setIsLoadingInitial] = useState(true); // Track initial loading
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [sortOrder, setSortOrder] = useState("DESC");
  const { ref, inView } = useInView({ threshold: 0.5, triggerOnce: false });
  const [searchQuery, setSearchQuery] = useState("");
  const [locale, setLocale] = useState<string>("en");
  const t = useTranslations("home");

  useEffect(() => {
    params.then((resolvedParams) => {
      setLocale(resolvedParams.locale || "en");
    });
  }, [params]);

  const fetchInitialData = useCallback(async () => {
    const supabase = createClient();

    let query = supabase
      .from("podcasts")
      .select("*")
      .eq("locale", locale)
      .limit(8);

    // Apply sorting based on the sortOrder state
    switch (sortOrder) {
      case "ASC":
        query = query.order("publish_date", { ascending: true });
        break;
      case "DESC":
        query = query.order("publish_date", { ascending: false });
        break;
      case "MOSTVIEWS":
        query = query
          .order("views", { ascending: false })
          .order("id", { ascending: false });
        break;
      case "LEASTVIEWS":
        query = query
          .order("views", { ascending: true })
          .order("id", { ascending: true });
        break;
    }

    try {
      const { data, error } = await query;
      if (error) throw error;
      setCards(data || []);
      setHasMore(data?.length === 8);
      setIsLoadingInitial(false);
    } catch (e) {
      console.error("Error connecting to Supabase", e);
      setIsLoadingInitial(false);
    }
  }, [sortOrder, locale]);

  useEffect(() => {
    fetchInitialData();
  }, [fetchInitialData]);

  const fetchMorePodcasts = useCallback(async () => {
    if (!isLoadingMore && hasMore && cards.length > 0) {
      setIsLoadingMore(true);
      const supabase = createClient();

      const lastCard = cards[cards.length - 1];
      let query = supabase
        .from("podcasts")
        .select("*")
        .eq("locale", locale)
        .limit(10);

      switch (sortOrder) {
        case "ASC":
          query = query
            .gt("publish_date", lastCard.publish_date)
            .order("publish_date", { ascending: true });
          break;
        case "DESC":
          query = query
            .lt("publish_date", lastCard.publish_date)
            .order("publish_date", { ascending: false });
          break;
        case "MOSTVIEWS":
          // Sort primarily by views, then by publish_date to ensure consistent ordering
          query = query
            .or(
              `views.lt.${lastCard.views},and(views.eq.${lastCard.views},publish_date.lt.${lastCard.publish_date})`,
            )
            .order("views", { ascending: false })
            .order("publish_date", { ascending: false });
          break;
        case "LEASTVIEWS":
          // Sort primarily by views, then by publish_date to ensure consistent ordering
          query = query
            .or(
              `views.gt.${lastCard.views},and(views.eq.${lastCard.views},publish_date.gt.${lastCard.publish_date})`,
            )
            .order("views", { ascending: true })
            .order("publish_date", { ascending: true });
          break;
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
  }, [cards, isLoadingMore, hasMore, sortOrder, locale]);

  useEffect(() => {
    if (inView && hasMore) {
      fetchMorePodcasts();
    }
  }, [inView, hasMore, fetchMorePodcasts]);

  const filteredCards = cards.filter((card) =>
    (card.blog_content || "")
      .toLowerCase()
      .includes((searchQuery || "").toLowerCase()),
  );

  return (
    <>
      <Header />
      <main className="flex flex-col items-center py-10">
        <div className="mb-8 w-full max-w-7xl px-4">
          <NewsletterSignup />
        </div>

        <div className="mb-4 flex flex-col items-center space-y-2 md:flex-row md:space-x-2 md:space-y-0">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t("search")}
            className="w-full rounded-md border bg-background p-2 text-foreground md:w-auto"
          />
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value)}
            className="w-full rounded-md border bg-background p-2 text-foreground md:w-auto"
          >
            <option value="DESC">{t("sortLatest")}</option>
            <option value="ASC">{t("sortEarliest")}</option>
            <option value="MOSTVIEWS">{t("sortMostViews")}</option>
            <option value="LEASTVIEWS">{t("sortLeastViews")}</option>
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
            <div>{t("noResults")}</div>
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
