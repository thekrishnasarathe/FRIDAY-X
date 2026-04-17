import { api } from '../services/api';

const ACTIONS = [
  { id: 'morning',    label: 'Morning',     icon: '☀', cmd: 'open whatsapp' },
  { id: 'youtube',    label: 'YouTube',     icon: '▶', cmd: 'open youtube' },
  { id: 'code',       label: 'VS Code',     icon: '⟨⟩', cmd: 'open vscode' },
  { id: 'screenshot', label: 'Screenshot',  icon: '📸', cmd: 'take a screenshot' },
  { id: 'chrome',     label: 'Chrome',      icon: '🌐', cmd: 'open chrome' },
  { id: 'github',     label: 'GitHub',      icon: '⚙', cmd: 'open github' },
  { id: 'calc',       label: 'Calculator',  icon: '🧮', cmd: 'open calculator' },
  { id: 'notepad',    label: 'Notepad',     icon: '📝', cmd: 'open notepad' },
  { id: 'spotify',    label: 'Spotify',     icon: '🎵', cmd: 'open spotify' },
];

export default function QuickActions() {
  const run = async (cmd) => {
    try { await api.executeCommand(cmd); } catch {}
  };

  return (
    <div className="quick-panel glass">
      <span className="hud-label">Quick Launch</span>
      <div className="qa-grid">
        {ACTIONS.map(a => (
          <button key={a.id} className="qa-tile" onClick={() => run(a.cmd)}>
            <span className="qa-icon">{a.icon}</span>
            <span className="qa-name">{a.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
