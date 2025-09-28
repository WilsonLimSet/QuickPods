import Link from "next/link";
import React from "react";

interface Post {
  slug: string;
  title: string;
  description: string;
  date: string;
}

interface PostCardProps {
  post: Post;
}

export default function PostCard({ post }: PostCardProps) {
  return (
    <Link href={`/blog/${post.slug}`} passHref>
      <div className="mb-4 block cursor-pointer rounded-lg border p-4 transition-shadow hover:shadow-lg">
        <h3 className="mb-2 text-lg font-semibold text-blue-800">
          {post.title}
        </h3>
        <p className="mb-3 text-sm text-gray-600">
          {new Date(post.date).toLocaleDateString()}
        </p>
        <p className="text-gray-800">{post.description}</p>
      </div>
    </Link>
  );
}
