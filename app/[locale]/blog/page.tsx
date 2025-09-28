// pages/blog/index.tsx
import React from "react";
import Header from "@/components/Header";
import { getSortedPosts } from "@/lib/posts";
import BlogCard from "@/components/BlogCard";
import Footer from "@/components/Footer";

export default async function Blog() {
  const posts = await getSortedPosts(); // Asynchronously fetch your posts

  return (
    <>
      <Header />
      <h2 className="my-8 text-center text-2xl text-white">
        Latest Blog Posts
      </h2>
      <div className="mx-auto max-w-4xl px-4">
        {posts.map((post: { slug: string; title: string; excerpt: string; date: string }) => (
          <BlogCard
            key={post.slug}
            post={{
              slug: post.slug,
              title: post.title,
              description: post.excerpt,
              date: post.date,
            }}
          />
        ))}
      </div>
      <Footer />
    </>
  );
}
