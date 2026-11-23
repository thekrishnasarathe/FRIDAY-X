import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import TopTacticalBar from '../components/TopTacticalBar';
import VoiceOrb from '../components/VoiceOrb';
import QuickActions from '../components/QuickActions';
import ChatPanel from '../components/ChatPanel';
import SystemStatus from '../components/SystemStatus';
import MemorySecurityCard from '../components/MemorySecurityCard';
import MemoryVaultModal from '../components/MemoryVaultModal';
import AuthPopup from '../components/AuthPopup';
import './Dashboard.css';

export default function Dashboard() {
  const [online, setOnline] = useState(false);
  const [healthInfo, setHealthInfo] = useState(null);
  const [isChecking, setIsChecking] = useState(false);
  const [activeMode, setActiveMode] = useState('assistant');
  const [voiceInput, setVoiceInput] = useState('');
  const [isSecurityOpen, setIsSecurityOpen] = useState(false);
  const [isMemoryOpen, setIsMemoryOpen] = useState(false);

  const checkConnection = async () => {
    setIsChecking(true);
    try {
      const h = await api.checkHealth();
      const isHealthy = h.status === 'healthy' || h.health === 'ok';
      setOnline(isHealthy);
      if (isHealthy) {
        setHealthInfo(h);
      }
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkConnection();
    const iv = setInterval(() => {
      if (!document.hidden) checkConnection();
    }, 25000);

    const handleVis = () => {
      if (!document.hidden) checkConnection();
    };
    document.addEventListener('visibilitychange', handleVis);
    return () => {
      clearInterval(iv);
      document.removeEventListener('visibilitychange', handleVis);
    };
  }, []);

  const handleModeChange = async (newMode) => {
    setActiveMode(newMode);
    try {
      await api.sendMessage(`switch to ${newMode} mode`, false, newMode);
    } catch {}
  };

  const handleVoiceTranscript = (transcript) => {
    setVoiceInput(transcript);
  };

  const handleQuickAction = (cmd) => {
    setVoiceInput(cmd);
  };

  if (!online) {
    return (
      <div className="offline-screen">
        <div className="offline-reactor"></div>
        <h1 className="glow-cyan">FRIDAY CORE OFFLINE</h1>
        <p className="hud-label">Connecting to {api.getBaseUrl()}...</p>
        <p className="offline-note">
          Free-tier cloud hosts may take up to 45 seconds to spin up on initial load.
        </p>
        <button
          onClick={checkConnection}
          disabled={isChecking}
          className="offline-retry-btn"
        >
          {isChecking ? 'Pinging Core...' : 'Retry Connection'}
        </button>
      </div>
    );
  }

  return (
    <div className="tactical-hud-container">
      {/* ─── Top Tactical Navigation Bar ───────────────── */}
      <TopTacticalBar
        activeMode={activeMode}
        onModeChange={handleModeChange}
        healthInfo={healthInfo}
        onOpenSecurity={() => setIsSecurityOpen(true)}
        onOpenMemory={() => setIsMemoryOpen(true)}
      />

      {/* ─── 3-Column Tactical HUD Grid ─────────────────── */}
      <main className="hud-three-col-grid">
        {/* Left Column (280px rail): Voice Core & Quick Launch */}
        <aside className="hud-rail left-rail">
          <VoiceOrb
            onTranscript={handleVoiceTranscript}
            mode={activeMode}
          />
          <QuickActions onExecute={handleQuickAction} />
        </aside>

        {/* Center Workspace (1fr): Agent Execution Stream */}
        <section className="hud-center-workspace">
          <ChatPanel
            activeMode={activeMode}
            voiceInput={voiceInput}
            onClearVoiceInput={() => setVoiceInput('')}
            onTriggerVoice={() => {}}
          />
        </section>

        {/* Right Column (300px rail): Telemetry & Memory */}
        <aside className="hud-rail right-rail">
          <SystemStatus />
          <MemorySecurityCard
            onOpenSecurity={() => setIsSecurityOpen(true)}
            onOpenMemory={() => setIsMemoryOpen(true)}
          />
        </aside>
      </main>

      {/* ─── Modals ────────────────────────────────────── */}
      <MemoryVaultModal
        isOpen={isMemoryOpen}
        onClose={() => setIsMemoryOpen(false)}
      />

      {isSecurityOpen && (
        <AuthPopup
          onUnlock={() => {
            setIsSecurityOpen(false);
            checkConnection();
          }}
        />
      )}
    </div>
  );
}
