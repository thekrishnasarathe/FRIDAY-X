import { useState, useEffect } from 'react';
import { api } from '../services/api';
import './AuthPopup.css';

export default function AuthPopup({ onUnlock }) {
  const [passphrase, setPassphrase] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleUnlock = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      const response = await api.unlockAssitant(passphrase);
      if (response && response.toLowerCase().includes('unlocked')) {
        onUnlock();
      } else {
        setError(response || 'Incorrect passphrase.');
      }
    } catch (err) {
      setError('Connection to FRIDAY core failed.');
    }
    
    setIsLoading(false);
  };

  return (
    <div className="auth-overlay">
      <div className="glass-panel auth-panel">
        <div className="auth-header">
          <div className="arc-reactor-locked"></div>
          <h2 className="glow-text">SYSTEM LOCKED</h2>
          <p>FRIDAY Core Security Active</p>
        </div>
        
        <form onSubmit={handleUnlock} className="auth-form">
          <input
            type="password"
            value={passphrase}
            onChange={(e) => setPassphrase(e.target.value)}
            placeholder="Enter Override Passphrase..."
            autoFocus
            className="glow-input"
          />
          {error && <div className="auth-error">{error}</div>}
          <button type="submit" disabled={isLoading} className="glow-btn">
            {isLoading ? 'Verifying...' : 'Authenticate'}
          </button>
        </form>
      </div>
    </div>
  );
}
