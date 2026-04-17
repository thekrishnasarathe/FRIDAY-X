import { useState } from 'react';
import { api } from '../services/api';
import './VoicePanel.css';

export default function VoicePanel({ onSpeakResponse }) {
  const [isListening, setIsListening] = useState(false);
  const [statusText, setStatusText] = useState('Voice Interface Default');

  const handleMicClick = async () => {
    if (isListening) return; // Prevent multiple clicks
    
    setIsListening(true);
    setStatusText('Listening...');
    
    try {
      // Calls the /voice/listen endpoint causing Python microphone to activate
      const response = await api.voiceListen();
      setStatusText('Processing...');
      // Pass the transcription/response back up if needed
      if (onSpeakResponse && response) {
        onSpeakResponse(response);
      }
      
      setTimeout(() => {
        setStatusText('Voice Interface Default');
      }, 3000);
      
    } catch (err) {
      setStatusText('Connection Error');
      setTimeout(() => setStatusText('Voice Interface Default'), 3000);
    }
    
    setIsListening(false);
  };

  return (
    <div className="glass-panel voice-panel-container">
      <div className="voice-status-bar">
        <span className="hud-title">AUDIO PROTOCOL</span>
        <span className={`status-indicator ${isListening ? 'active' : ''}`}></span>
      </div>
      
      <div className="arc-reactor-wrapper" onClick={handleMicClick}>
        <div className={`arc-reactor-core ${isListening ? 'listening' : 'idle'}`}>
          <div className="core-inner"></div>
          {/* Inner ring elements */}
          <div className="ring ring-1"></div>
          <div className="ring ring-2"></div>
        </div>
        <div className="mic-icon">
           <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" x2="12" y1="19" y2="22"></line>
           </svg>
        </div>
      </div>
      
      <div className="voice-text-display">
        <p className="glow-text">{statusText}</p>
        <div className="audio-wave">
          {isListening && [1,2,3,4,5].map(i => <div key={i} className="wave-bar"></div>)}
        </div>
      </div>
    </div>
  );
}
