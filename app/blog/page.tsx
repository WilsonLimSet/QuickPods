// blog.server.js
import React from "react";
import Header from "@/components/Header";
import { getSortedPosts } from "../../lib/posts";

export default async function Blog() {
  const posts = await getSortedPosts(); // Asynchronously fetch your posts
  return (
    <>
      <Header />
      <h2 className="mb-4 text-center text-2xl font-light">
        Latest Blog Posts (Work in Progress)
      </h2>
      <div>
        {posts.map(
          (post: {
            slug: React.Key | null | undefined;
            title: string;
            date: string;
            excerpt: string;
          }) => (
            <div key={post.slug}>
              <h3>{post.title}</h3>
              <p>{post.date}</p>
              <p>{post.excerpt}</p>
            </div>
          ),
        )}
      </div>
    </>
  );
}
