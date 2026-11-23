import { useState, useEffect } from 'react';
import { api } from '../services/api';
import ChatPanel from '../components/ChatPanel';
import SystemStatus from '../components/SystemStatus';
import VoiceOrb from '../components/VoiceOrb';
import QuickActions from '../components/QuickActions';
import ModeSwitcher from '../components/ModeSwitcher';
import './Dashboard.css';

export default function Dashboard() {
  const [online, setOnline] = useState(false);
  const [info, setInfo] = useState(null);
  const [isChecking, setIsChecking] = useState(false);

  const checkConnection = async () => {
    setIsChecking(true);
    try {
      const h = await api.checkHealth();
      const isHealthy = h.status === 'healthy' || h.health === 'ok';
      setOnline(isHealthy);
      if (isHealthy) {
        const i = await api.getSystemInfo();
        setInfo(i);
      }
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkConnection();
    let iv = setInterval(() => {
      if (!document.hidden) {
        checkConnection();
      }
    }, 30000);

    const handleVis = () => {
      if (!document.hidden) {
        checkConnection();
      }
    };
    document.addEventListener("visibilitychange", handleVis);

    return () => {
      clearInterval(iv);
      document.removeEventListener("visibilitychange", handleVis);
    };
  }, []);

  if (!online) {
    return (
      <div className="offline-screen">
        <div className="offline-reactor"></div>
        <h1 className="glow">FRIDAY CORE OFFLINE</h1>
        <p className="hud-label">Connecting to {api.getBaseUrl()}...</p>
        <p style={{ color: '#64748b', fontSize: '0.85rem', marginTop: '0.5rem', maxWidth: '400px', textAlign: 'center' }}>
          Free-tier cloud hosts may take up to 45 seconds to spin up on initial load.
        </p>
        <button
          onClick={checkConnection}
          disabled={isChecking}
          style={{
            marginTop: '1.25rem',
            padding: '0.6rem 1.5rem',
            background: 'rgba(56, 189, 248, 0.15)',
            border: '1px solid #38bdf8',
            borderRadius: '6px',
            color: '#38bdf8',
            cursor: isChecking ? 'wait' : 'pointer',
            fontSize: '0.85rem',
            letterSpacing: '1px',
            textTransform: 'uppercase',
          }}
        >
          {isChecking ? 'Pinging Core...' : 'Retry Connection'}
        </button>
      </div>
    );
  }

  return (
    <div className="dashboard">
      {/* ─── Header ──────────────────────────────────────── */}
      <header className="dash-header">
        <div className="logo-area">
          <div className="logo-dot"></div>
          <h1>FRIDAY<span className="logo-x">-X</span></h1>
        </div>
        <div className="header-right">
          <ModeSwitcher />
          <div className="status-badge glass">
            <span className="dot-online"></span>
            <span className="hud-label">v{info?.version || '3.0'}</span>
          </div>
        </div>
      </header>

      {/* ─── Main Grid ───────────────────────────────────── */}
      <main className="dash-grid">
        <aside className="left-col">
          <VoiceOrb />
          <QuickActions />
        </aside>

        <section className="center-col">
          <ChatPanel />
        </section>

        <aside className="right-col">
          <SystemStatus />
        </aside>
      </main>
    </div>
  );
}
