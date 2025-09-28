import React from "react";
import Markdown from "markdown-to-jsx";
import Header from "@/components/Header";
import SocialShare from "@/components/SocialShare";
import { Metadata } from "next";
import { notFound } from "next/navigation";
import { createClient } from "@/utils/supabase/server";
import { locales } from "@/i18n/request";
import { getTranslations } from "next-intl/server";

async function getPostBySlug(slug: string, locale: string = "en") {
  const supabase = await createClient();
  const { data, error } = await supabase
    .from("podcasts")
    .select("*")
    .eq("md_slug", slug)
    .eq("locale", locale)
    .single();

  if (error || !data) {
    // Fallback to English if locale version doesn't exist
    if (locale !== "en") {
      const { data: fallbackData } = await supabase
        .from("podcasts")
        .select("*")
        .eq("md_slug", slug)
        .eq("locale", "en")
        .single();
      return fallbackData;
    }
    return null;
  }
  return data;
}

export const dynamic = "force-dynamic";
export const revalidate = 0;

export async function generateMetadata({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}): Promise<Metadata> {
  const { locale, slug } = await params;
  const post = await getPostBySlug(slug, locale);

  if (!post) {
    return {
      title: "Post Not Found | QuickPods",
    };
  }

  const description =
    post.blog_content?.slice(0, 160).replace(/#/g, "").trim() ||
    `Interview with ${post.interviewee}`;
  const ogImage = post.thumbnail_url || "/og-default.png";
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://quickpods.io";

  const languages: Record<string, string> = {};
  for (const loc of locales) {
    languages[loc] = `${baseUrl}/${loc}/blog/${slug}`;
  }

  return {
    title: `${post.interviewee} Interview | QuickPods`,
    description,
    openGraph: {
      title: `${post.interviewee} Interview`,
      description,
      type: "article",
      publishedTime: post.publish_date,
      authors: [post.interviewee, post.interviewer],
      images: [ogImage],
      url: `${baseUrl}/${locale}/blog/${slug}`,
      locale: locale,
    },
    twitter: {
      card: "summary_large_image",
      title: `${post.interviewee} Interview`,
      description,
      images: [ogImage],
    },
    alternates: {
      canonical: `${baseUrl}/${locale}/blog/${slug}`,
      languages,
    },
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ locale: string; slug: string }>;
}) {
  const { locale, slug } = await params;
  const post = await getPostBySlug(slug, locale);
  const t = await getTranslations("blog");

  if (!post) {
    notFound();
  }

  const fullUrl = `https://quickpods.io/${locale}/blog/${slug}`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: `${t("interviewWith")} ${post.interviewee}`,
    datePublished: post.publish_date,
    author: [
      {
        "@type": "Person",
        name: post.interviewee,
      },
      {
        "@type": "Person",
        name: post.interviewer,
      },
    ],
    description:
      post.blog_content?.slice(0, 160).replace(/#/g, "").trim() ||
      `${t("interviewWith")} ${post.interviewee}`,
    image: post.thumbnail_url,
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <Header />
      <main className="mx-auto max-w-4xl p-4">
        <article>
          <h1 className="text-3xl font-bold text-white">
            {t("interviewWith")} {post.interviewee}
          </h1>
          {post.interviewee_title && (
            <p className="mt-1 text-xl text-gray-300">
              {post.interviewee_title}
            </p>
          )}
          <p className="mt-2 text-gray-400">
            {t("by")} {post.interviewer} • {post.publish_date}
          </p>

          {post.thumbnail_url && (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={post.thumbnail_url}
              alt={post.interviewee}
              className="my-6 w-full rounded-lg"
            />
          )}

          <div className="prose prose-invert max-w-none">
            {post.blog_content ? (
              <Markdown>{post.blog_content}</Markdown>
            ) : (
              <p>
                {t("interviewWith")} {post.interviewee} on {post.interviewer}
                &apos;s channel.
              </p>
            )}
          </div>

          {post.youtube_url && (
            <div className="my-8">
              <a
                href={post.youtube_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block rounded-md bg-red-600 px-6 py-3 font-semibold text-white transition-colors hover:bg-red-700"
              >
                {t("watchOnYoutube")} →
              </a>
            </div>
          )}

          <SocialShare
            url={fullUrl}
            title={`${t("interviewWith")} ${post.interviewee}`}
          />
        </article>
      </main>
    </>
  );
}
