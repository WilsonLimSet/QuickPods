import React from "react";
import Link from "next/link";
import { createClient } from "@/utils/supabase/client"; // Ensure this path is correct

const incrementViews = async (id: number) => {
  const supabase = createClient();

  try {
    // First, get the current views
    let { data: currentData, error: getError } = await supabase
      .from("Podcasts")
      .select("views")
      .eq("id", id)
      .single();

    if (!currentData) {
      throw new Error("Current data is null.");
    }

    if (getError) throw getError;

    // Now increment the views
    const newViews = currentData.views + 1;
    const { error: updateError } = await supabase
      .from("Podcasts")
      .update({ views: newViews })
      .match({ id: id });

    if (updateError) throw updateError;
  } catch (error) {
    console.error("Error incrementing views:", error);
  }
};
interface PodCardProps {
  id: number;
  thumbnail_url: string;
  interviewee: string;
  interviewer: string;
  publish_date: string;
  md_slug: string;
  views: number;
}

const PodCard = ({
  id,
  thumbnail_url,
  interviewee,
  interviewer,
  publish_date,
  md_slug,
  views,
}: PodCardProps) => {
  const handleButtonClick = (
    e: React.MouseEvent<HTMLAnchorElement, MouseEvent>
  ) => {
    e.stopPropagation(); // Prevent navigation when the button is clicked
  };

  const handleCardClick = async (e: React.MouseEvent) => {
    if (!md_slug) {
      e.preventDefault(); // Prevent navigation if no valid slug
    } else {
      await incrementViews(id); // Call the increment function with the podcast's ID
    }
  };

  return (
    <Link href={md_slug ? `/blog/${md_slug}` : ""} passHref>
      <div
        className="bg-gray-900 rounded-lg overflow-hidden text-white shadow-xl flex flex-col justify-between cursor-pointer transition-opacity duration-500 hover:opacity-75"
        onClick={handleCardClick}
        style={{ maxWidth: "340px", height: "320px" }}
      >
        <img
          src={thumbnail_url}
          alt={`Thumbnail for ${interviewee}`}
          className="w-full h-40 object-cover"
        />
        <div className="p-4 flex flex-1 flex-col">
          <h2 className="text-lg font-bold mb-2">{interviewee}</h2>
          <h4 className="text-md text-gray-300 flex-1">
            Interviewed by {interviewer}
          </h4>
          <div className="text-md text-gray-300 flex items-center mb-2">
            {publish_date} <span className="mx-2">•</span>{" "}
            {views.toLocaleString()} views
          </div>
        </div>
      </div>
    </Link>
  );
};

export default PodCard;
