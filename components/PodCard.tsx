import React from 'react';

interface PodCardProps {
  id: string;
  thumbnail_url: string;
  interviewee: string;
  interviewer: string;
  publishDate: string;
  youtube_url: string;
}

const PodCard = ({
  id,
  thumbnail_url,
  interviewee,
  interviewer,
  publishDate,
  youtube_url
}: PodCardProps) => {
  return (
    <div className="card" style={{
      backgroundColor: '#343a40', 
      borderRadius: '8px', 
      overflow: 'hidden',
      color: 'white',
      maxWidth: '340px', // Consistent max width
      boxShadow: '0 4px 6px rgba(0,0,0,0.1)', // subtle shadow
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      <div style={{ overflow: 'hidden', height: '155px' }}>
        {/* Adjust objectFit here */}
        <img src={thumbnail_url} alt={`Thumbnail for ${interviewee}`} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </div>
      <div style={{ padding: '16px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 'bold', margin: '0 0 8px' }}>{interviewee}</h2>
        <h4 style={{ fontSize: '16px', fontWeight: 'normal', color: '#adb5bd', margin: '0 0 16px' }}>Interviewed by {interviewer}</h4>
        <span style={{ fontSize: '14px', color: '#adb5bd' }}>{publishDate}</span>
        <a href={youtube_url} target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none', marginTop: 'auto' }}>
          <button style={{ backgroundColor: '#e93d83', color: 'white', border: 'none', padding: '10px 16px', cursor: 'pointer', borderRadius: '4px', fontSize: '16px', marginTop: '8px' }}>
            Watch podcast
          </button>
        </a>
      </div>
    </div>
  );
};

export default PodCard;