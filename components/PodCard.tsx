import React from "react";
import Link from "next/link"; // Import the Link component from next/link

interface PodCardProps {
  id: string;
  thumbnail_url: string;
  interviewee: string;
  interviewer: string;
  publish_date: string;
  youtube_url: string;
  md_slug: string;
}

const PodCard = ({
  id,
  thumbnail_url,
  interviewee,
  interviewer,
  publish_date,
  youtube_url,
  md_slug,
}: PodCardProps) => {
  // Prevent event propagation to stop card click when button is clicked
  const handleButtonClick = (
    e: React.MouseEvent<HTMLAnchorElement, MouseEvent>
  ) => {
    e.stopPropagation(); // Stop propagation to prevent Link from triggering
  };

  // Card Click Handler: Only redirect if md_slug is valid
  const handleCardClick = (e: React.MouseEvent) => {
    if (!md_slug) {
      e.preventDefault(); // Prevent navigation if slug is invalid
      return; // Optionally display an error message or log this issue
    }
  };

  return (
    <Link href={md_slug ? `/blog/${md_slug}` : ""} passHref>
      <div
        className="card"
        style={{
          backgroundColor: "#343a40",
          borderRadius: "8px",
          overflow: "hidden",
          color: "white",
          maxWidth: "340px",
          height: "350px",
          boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          cursor: md_slug ? "pointer" : "default",
        }}
        onClick={handleCardClick}
      >
        <div style={{ overflow: "hidden", height: "155px" }}>
          <img
            src={thumbnail_url}
            alt={`Thumbnail for ${interviewee}`}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </div>
        <div
          style={{
            padding: "16px",
            flex: "1",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <h2
            style={{ fontSize: "18px", fontWeight: "bold", margin: "0 0 8px" }}
          >
            {interviewee}
          </h2>
          <h4
            style={{
              fontSize: "16px",
              fontWeight: "normal",
              color: "#adb5bd",
              margin: "0",
              flex: "1",
            }}
          >
            Interviewed by {interviewer}
          </h4>
          {/* <span style={{ fontSize: "14px", color: "#adb5bd" }}>
            {publish_date}
          </span> */}
          <span
            style={{ fontSize: "15px", color: "#adb5bd", marginBottom: "8px" }}
          >
            {/* Published on {publish_date} */}
            {publish_date}
          </span>
          <a
            href={youtube_url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ textDecoration: "none", marginTop: "auto" }}
            onClick={handleButtonClick}
          >
            <button
              style={{
                backgroundColor: "#e93d83",
                color: "white",
                border: "none",
                padding: "10px 16px",
                cursor: "pointer",
                borderRadius: "4px",
                fontSize: "16px",
              }}
            >
              Watch podcast
            </button>
          </a>
        </div>
      </div>
    </Link>
  );
};
export default PodCard;
