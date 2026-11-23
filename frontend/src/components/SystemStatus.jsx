import React, { useState, useEffect } from 'react';
import { api } from '../services/api';
import './SystemStatus.css';

export default function SystemStatus() {
  const [telemetry, setTelemetry] = useState({
    cpu: 38,
    ram: 47,
    latency: 14,
    sparklines: {
      cpu: [32, 36, 42, 38, 44, 39, 36, 38],
      ram: [45, 46, 47, 48, 47, 47, 46, 47],
      latency: [12, 14, 13, 16, 14, 15, 13, 14],
    },
    status: 'online',
  });

  const fetchMetrics = async () => {
    try {
      const data = await api.fetchTelemetry();
      if (data && data.cpu !== undefined) {
        setTelemetry(data);
      }
    } catch {}
  };

  useEffect(() => {
    fetchMetrics();
    let timer = setInterval(() => {
      if (!document.hidden) fetchMetrics();
    }, 15000);

    const onVis = () => {
      if (!document.hidden) {
        fetchMetrics();
      }
    };
    document.addEventListener('visibilitychange', onVis);
    return () => {
      clearInterval(timer);
      document.removeEventListener('visibilitychange', onVis);
    };
  }, []);

  // Gauge component with smooth SVG circle and no-clipping label
  const RadialGauge = ({ value, max = 100, unit = '%', label, color = 'var(--cyan)', sparkline = [] }) => {
    const radius = 26;
    const circumference = 2 * Math.PI * radius;
    const clampedVal = Math.min(max, Math.max(0, value));
    const offset = circumference - (clampedVal / max) * circumference;

    // Build SVG sparkline polyline points
    const sparkW = 68;
    const sparkH = 18;
    const pts = sparkline.map((pt, idx) => {
      const x = (idx / (sparkline.length - 1 || 1)) * sparkW;
      const y = sparkH - ((pt % 50) / 50) * (sparkH - 4) - 2;
      return `${x},${y}`;
    }).join(' ');

    return (
      <div className="gauge-column">
        <div className="gauge-circle-wrap">
          <svg className="gauge-svg" width="66" height="66" viewBox="0 0 66 66">
            <circle
              className="gauge-bg"
              cx="33"
              cy="33"
              r={radius}
              fill="none"
              stroke="rgba(0, 240, 255, 0.08)"
              strokeWidth="4"
            />
            <circle
              className="gauge-progress"
              cx="33"
              cy="33"
              r={radius}
              fill="none"
              stroke={color}
              strokeWidth="4"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              strokeLinecap="round"
              transform="rotate(-90 33 33)"
              style={{ transition: 'stroke-dashoffset 1s ease-out' }}
            />
          </svg>

          <div className="gauge-inner-val">
            <span className="gauge-number" style={{ color }}>{value}</span>
            <span className="gauge-unit">{unit}</span>
          </div>
        </div>

        <span className="gauge-label">{label}</span>

        {/* Mini ECG Sparkline Waveform */}
        <div className="gauge-sparkline-box">
          <svg width={sparkW} height={sparkH} className="sparkline-svg">
            <polyline
              fill="none"
              stroke={color}
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              points={pts || `0,9 10,6 20,12 30,5 40,11 50,7 68,9`}
              opacity="0.85"
            />
          </svg>
        </div>
      </div>
    );
  };

  return (
    <div className="telemetry-card tactical-panel tactical-corner">
      <div className="telemetry-card-header">
        <span className="hud-title">SYSTEM TELEMETRY</span>
        <span className="telemetry-live-dot"></span>
      </div>

      <div className="gauges-row">
        <RadialGauge
          value={telemetry.cpu}
          unit="%"
          label="CPU"
          color="var(--cyan)"
          sparkline={telemetry.sparklines?.cpu}
        />
        <RadialGauge
          value={telemetry.ram}
          unit="%"
          label="RAM"
          color={telemetry.ram > 80 ? 'var(--amber)' : 'var(--cyan)'}
          sparkline={telemetry.sparklines?.ram}
        />
        <RadialGauge
          value={telemetry.latency}
          unit="ms"
          max={60}
          label="LATENCY"
          color="var(--cyan)"
          sparkline={telemetry.sparklines?.latency}
        />
      </div>
    </div>
  );
}
