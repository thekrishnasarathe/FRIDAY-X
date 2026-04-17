import { useState, useEffect } from 'react';
import { api } from '../services/api';

const MODES = [
  { id: 'assistant', label: 'General', icon: '🤖' },
  { id: 'coding',    label: 'Coding',  icon: '💻' },
  { id: 'study',     label: 'Study',   icon: '📚' },
];

export default function ModeSwitcher() {
  const [active, setActive] = useState('assistant');

  const switchMode = async (mode) => {
    setActive(mode);
    try { await api.sendMessage(`switch to ${mode} mode`, false); } catch {}
  };

  return (
    <div className="mode-bar glass">
      <span className="hud-label">Mode</span>
      <div className="mode-pills">
        {MODES.map(m => (
          <button key={m.id}
            className={`mode-pill ${active === m.id ? 'active' : ''}`}
            onClick={() => switchMode(m.id)}>
            <span>{m.icon}</span>
            <span>{m.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
