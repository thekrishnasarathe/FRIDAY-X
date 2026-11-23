import { useState, useEffect } from 'react';
import { api } from '../services/api';

export default function SystemStatus() {
  const [stats, setStats] = useState({ cpu: 0, ram: 0, battery: 100, plugged: true });

  const fetch_ = async () => {
    try {
      const r = await api.fetchSystemStats();
      if (r) {
        const m = [...r.matchAll(/(\d+\.?\d*)%/g)].map(x => parseFloat(x[1]));
        if (m.length >= 3) setStats({ cpu: m[0], ram: m[1], battery: m[2], plugged: r.includes("plugged") });
      }
    } catch {}
  };

  useEffect(() => {
    fetch_();
    let i = setInterval(() => { if (!document.hidden) fetch_(); }, 60000);
    
    const handleVisibilityChange = () => {
      if (!document.hidden) {
        fetch_();
        clearInterval(i);
        i = setInterval(() => { if (!document.hidden) fetch_(); }, 60000);
      }
    };
    
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => {
      clearInterval(i);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, []);

  const Ring = ({ pct, color, label, icon }) => {
    const r = 32, c = 2 * Math.PI * r, off = c - (pct / 100) * c;
    return (
      <div className="ring-module">
        <svg width="80" height="80" viewBox="0 0 80 80">
          <circle cx="40" cy="40" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="5"/>
          <circle cx="40" cy="40" r={r} fill="none" stroke={color} strokeWidth="5"
            strokeDasharray={c} strokeDashoffset={off} strokeLinecap="round"
            transform="rotate(-90 40 40)" style={{transition:'stroke-dashoffset 1.2s ease'}}/>
        </svg>
        <div className="ring-center" style={{color}}>{icon}</div>
        <div className="ring-label">
          <span className="ring-value" style={{color}}>{pct}%</span>
          <span className="ring-name">{label}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="sys-status glass">
      <span className="hud-label">System Diagnostics</span>
      <div className="rings-row">
        <Ring pct={stats.cpu} color="var(--primary)" label="CPU" icon="⚙" />
        <Ring pct={stats.ram} color={stats.ram > 85 ? "var(--warning)" : "var(--accent)"} label="RAM" icon="◈" />
        <Ring pct={stats.battery} color={stats.battery < 20 ? "var(--warning)" : "var(--primary)"} label={stats.plugged ? "⚡Charge" : "Battery"} icon="⏻" />
      </div>
    </div>
  );
}
