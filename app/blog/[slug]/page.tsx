import { getSortedPosts } from "@/lib/posts";
import React from "react";
import Markdown from "markdown-to-jsx";
import Header from "@/components/Header";

const getPostContent = (slug: string) => {
  const posts = getSortedPosts();
  return posts.find((post: any) => post.slug === slug);
};

export async function generateMetadata({
  params,
  searchParams,
}: {
  params: any;
  searchParams: any;
}) {
  const id = params?.slug ? " ⋅ " + params?.slug : "";
  return {
    title: `Blog Post${id.replaceAll("_", " ")}`,
  };
}

export default function BlogPostPage({ params }: { params: any }) {
  const slug = params.slug;
  const post = getPostContent(slug);

  if (!post) return <div>Post not found</div>;

  return (
    <>
      <Header />
      <main>
        <article>
          <Markdown>{post.content}</Markdown>
        </article>
      </main>
    </>
  );
}
