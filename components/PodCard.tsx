import React from "react";
import Link from "next/link";
import Image from "next/image";
import { createClient } from "@/utils/supabase/client";
import { useTranslations } from "next-intl";

const incrementViews = async (id: number) => {
  const supabase = createClient();

  try {
    const { data: currentData, error: getError } = await supabase
      .from("podcasts")
      .select("views")
      .eq("id", id)
      .single();

    if (!currentData) {
      throw new Error("Current data is null.");
    }

    if (getError) throw getError;

    const newViews = currentData.views + 1;
    const { error: updateError } = await supabase
      .from("podcasts")
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
  total_views?: number;
}

const PodCard = ({
  id,
  thumbnail_url,
  interviewee,
  interviewer,
  publish_date,
  md_slug,
  views,
  total_views,
}: PodCardProps) => {
  const t = useTranslations("card");

  const handleCardClick = async (e: React.MouseEvent) => {
    if (!md_slug) {
      e.preventDefault();
    } else {
      await incrementViews(id);
    }
  };

  return (
    <Link href={md_slug ? `/blog/${md_slug}` : ""} passHref>
      <div
        className="flex cursor-pointer flex-col justify-between overflow-hidden rounded-lg bg-gray-900 text-white shadow-xl transition-opacity duration-500 hover:opacity-75"
        onClick={handleCardClick}
        style={{ maxWidth: "340px", height: "320px" }}
      >
        <Image
          src={thumbnail_url}
          alt={`Thumbnail for ${interviewee}`}
          width={340}
          height={160}
          className="h-40 w-full object-cover"
          priority={false}
        />
        <div className="flex flex-1 flex-col p-4">
          <h2 className="mb-2 text-lg font-bold">{interviewee}</h2>
          <h4 className="text-md flex-1 text-gray-300">
            {t("interviewedBy")} {interviewer}
          </h4>
          <div className="text-md mb-2 flex items-center text-gray-300">
            {publish_date} <span className="mx-2">•</span>{" "}
            {(total_views ?? views).toLocaleString()} {t("views")}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default PodCard;
