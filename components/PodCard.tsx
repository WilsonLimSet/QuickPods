import React from 'react';

interface PodCardProps {
  id: string;
  thumbnail_url: string;
  interviewee: string;
  interviewer: string;
  publishDate: string;
  youtubeUrl: string;
}

const PodCard = ({
  id,
  thumbnail_url,
  interviewee,
  interviewer,
  publishDate,
  youtubeUrl
}: PodCardProps) => {
  return (
    <div className="card" style={{ backgroundColor: '#adb5bd', borderRadius: '11px', overflow: 'hidden' }}>
      <div style={{ overflow: 'hidden', height: '12em' }}>
        <img src={thumbnail_url} alt={`Thumbnail for ${interviewee}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div style={{ padding: '1em', height: '23em', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2>{interviewee}</h2>
        <h4>Interviewed by {interviewer}</h4>
        <span>{publishDate}</span>
        <a href={youtubeUrl} target="_blank" style={{ textDecoration: 'none' }}>
          <button style={{ backgroundColor: '#e93d83', color: '#343a40' }}>Watch podcast</button>
        </a>
      </div>
    </div>
  );
};

export default PodCard;
