// components/PostCard.tsx
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

export default function PostCard({ post }: PostCardProps): JSX.Element {
  return (
    <Link href={`/blog/${post.slug}`} passHref>
      <div className="block p-4 mb-4 border rounded-lg hover:shadow-lg transition-shadow cursor-pointer">
        <h3 className="text-lg text-blue-800 font-semibold mb-2">
          {post.title}
        </h3>
        <p className="text-sm text-gray-600 mb-3">
          {new Date(post.date).toLocaleDateString()}
        </p>
        <p className="text-gray-800">{post.description}</p>
      </div>
    </Link>
  );
}
