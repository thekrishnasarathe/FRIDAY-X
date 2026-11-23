import React from 'react';
import {
  Sun,
  Play,
  Code2,
  Camera,
  Globe,
  GitBranch,
  Calculator,
  FileText,
  Music,
} from 'lucide-react';
import './QuickActions.css';

const ACTIONS = [
  { id: 'morning', label: 'MORNING', icon: Sun, cmd: 'give me a morning briefing and top news' },
  { id: 'youtube', label: 'YOUTUBE', icon: Play, cmd: 'open youtube' },
  { id: 'code', label: 'VS CODE', icon: Code2, cmd: 'open vscode' },
  { id: 'screenshot', label: 'SCREENSHOT', icon: Camera, cmd: 'take screenshot' },
  { id: 'chrome', label: 'CHROME', icon: Globe, cmd: 'open chrome' },
  { id: 'github', label: 'GITHUB', icon: GitBranch, cmd: 'open github' },
  { id: 'calc', label: 'CALCULATOR', icon: Calculator, cmd: 'open calculator' },
  { id: 'notepad', label: 'NOTEPAD', icon: FileText, cmd: 'open notepad' },
  { id: 'spotify', label: 'SPOTIFY', icon: Music, cmd: 'open spotify' },
];

export default function QuickActions({ onExecute }) {
  const handleClick = (cmd) => {
    if (onExecute) {
      onExecute(cmd);
    }
  };

  return (
    <div className="quick-actions-card tactical-panel tactical-corner">
      <div className="qa-card-header">
        <span className="hud-title">QUICK ACTIONS</span>
        <span className="qa-count-badge">9/9 ACTIVE</span>
      </div>

      <div className="qa-tactical-grid">
        {ACTIONS.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className="qa-tile-btn"
              onClick={() => handleClick(item.cmd)}
              title={`Execute: ${item.cmd}`}
            >
              <div className="qa-tile-icon-box">
                <Icon size={18} className="qa-icon" />
              </div>
              <span className="qa-tile-label">{item.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
