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
  console.log(post);

  if (!post)
    return <div className="mt-20 text-center text-xl">Post not found</div>;

  return (
    <>
      <Header />
      <main className="mx-auto max-w-4xl p-4">
        <h1 className="text-2xl text-slate-600 ">{post.title}</h1>
        <p className="mt-2 text-slate-400">{post.date}</p>

        <article className="prose">
          <Markdown>{post.content}</Markdown>
        </article>
      </main>
    </>
  );
}
