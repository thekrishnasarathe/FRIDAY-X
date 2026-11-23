import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  Database,
  Cpu,
  Lock,
  Clock,
  Sparkles,
  Terminal,
  BookOpen,
} from 'lucide-react';
import './TopTacticalBar.css';

const MODES = [
  { id: 'assistant', label: 'GENERAL', icon: Cpu },
  { id: 'coding',    label: 'CODING',  icon: Terminal },
  { id: 'study',     label: 'STUDY',   icon: BookOpen },
];

export default function TopTacticalBar({
  activeMode,
  onModeChange,
  healthInfo,
  onOpenSecurity,
  onOpenMemory,
}) {
  const [timeStr, setTimeStr] = useState('00:00:00');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setTimeStr(now.toTimeString().split(' ')[0]);
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  const isOnline = healthInfo?.status === 'healthy' || healthInfo?.health === 'ok';
  const provider = (healthInfo?.llm_provider || 'ONLINE').toUpperCase();

  return (
    <header className="tactical-navbar tactical-panel">
      {/* ─── Left: Brand & Status Pulse ─────────────────── */}
      <div className="nav-brand-group">
        <div className="nav-reactor-dot"></div>
        <h1 className="nav-logo-text">
          FRIDAY<span className="logo-x-glow">-X</span>
        </h1>
      </div>

      {/* ─── Center: Segmented Mode Switcher Pills ──────── */}
      <div className="nav-mode-segment">
        {MODES.map((m) => {
          const Icon = m.icon;
          const isActive = activeMode === m.id;
          return (
            <button
              key={m.id}
              className={`mode-tab-btn ${isActive ? 'active' : ''}`}
              onClick={() => onModeChange(m.id)}
            >
              <Icon size={14} className="tab-icon" />
              <span>{m.label}</span>
              {isActive && <div className="tab-active-glow"></div>}
            </button>
          );
        })}
      </div>

      {/* ─── Right: Telemetry & Controls ───────────────── */}
      <div className="nav-right-cluster">
        {/* Secondary Mode Pill Tag */}
        <div className="submode-badge">
          <span className="submode-label">MODE</span>
          <div className="submode-tags">
            {MODES.map((m) => (
              <span
                key={m.id}
                className={`submode-tag ${activeMode === m.id ? 'active' : ''}`}
                onClick={() => onModeChange(m.id)}
              >
                {m.label.charAt(0) + m.label.slice(1).toLowerCase()}
              </span>
            ))}
          </div>
          <span className="submode-version">v{healthInfo?.version || '3.0.0'}</span>
        </div>

        {/* Neural Engine Health Pill */}
        <div className={`health-status-pill ${isOnline ? 'online' : 'offline'}`}>
          <span className="health-dot"></span>
          <span className="health-label">
            {isOnline ? (provider === 'GROQ' ? 'ONLINE' : provider) : 'OFFLINE'}
          </span>
        </div>

        {/* Live Digital Clock */}
        <div className="nav-clock-display">
          <Clock size={12} className="clock-icon" />
          <span className="clock-digits">{timeStr}</span>
        </div>

        {/* Quick Trigger Tool Buttons */}
        <div className="nav-quick-triggers">
          <button
            className="nav-trigger-btn"
            onClick={onOpenMemory}
            title="Open Memory Vault"
          >
            <Database size={15} />
          </button>
          <button
            className="nav-trigger-btn lock"
            onClick={onOpenSecurity}
            title="Security Protocol Override"
          >
            <Lock size={15} />
          </button>
        </div>
      </div>
    </header>
  );
}
