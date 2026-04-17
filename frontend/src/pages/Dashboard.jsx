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

  useEffect(() => {
    const boot = async () => {
      const h = await api.checkHealth();
      setOnline(h.status === 'healthy');
      const i = await api.getSystemInfo();
      setInfo(i);
    };
    boot();
    const iv = setInterval(async () => {
      const h = await api.checkHealth();
      setOnline(h.status === 'healthy');
    }, 15000);
    return () => clearInterval(iv);
  }, []);

  if (!online) {
    return (
      <div className="offline-screen">
        <div className="offline-reactor"></div>
        <h1 className="glow">FRIDAY CORE OFFLINE</h1>
        <p className="hud-label">Waiting for backend at localhost:8000...</p>
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
