import { useState } from 'react';
import { api } from '../services/api';

export default function VoiceOrb() {
  const [active, setActive] = useState(false);
  const [status, setStatus] = useState('Tap to speak');

  const handleClick = async () => {
    if (active) return;
    setActive(true);
    setStatus('Listening...');
    try {
      const res = await api.voiceListen();
      setStatus(res?.text || res?.friday_response || 'Done');
      setTimeout(() => setStatus('Tap to speak'), 4000);
    } catch {
      setStatus('Mic error');
      setTimeout(() => setStatus('Tap to speak'), 3000);
    }
    setActive(false);
  };

  return (
    <div className="voice-section glass">
      <span className="hud-label">Audio Protocol</span>
      <div className={`orb-wrapper ${active ? 'active' : ''}`} onClick={handleClick}>
        <div className="orb-glow"></div>
        <div className={`orb ${active ? 'listening' : ''}`}>
          <div className="orb-ring r1"></div>
          <div className="orb-ring r2"></div>
          <svg className="mic-svg" width="28" height="28" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" x2="12" y1="19" y2="22"/>
          </svg>
        </div>
      </div>
      <p className="voice-status glow">{status}</p>
      {active && <div className="wave-bars">{[1,2,3,4,5].map(i=><span key={i}/>)}</div>}
    </div>
  );
}
