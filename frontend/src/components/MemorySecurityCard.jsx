import React, { useState, useEffect } from 'react';
import { ShieldCheck, Lock, Database, Sparkles, KeyRound } from 'lucide-react';
import { api } from '../services/api';
import './MemorySecurityCard.css';

export default function MemorySecurityCard({ onOpenSecurity, onOpenMemory }) {
  const [securityStatus, setSecurityStatus] = useState('ACTIVE');
  const [memoryCount, setMemoryCount] = useState(0);

  useEffect(() => {
    const checkState = async () => {
      try {
        const sec = await api.getSecurityStatus();
        setSecurityStatus(sec || 'ACTIVE');
        const mem = await api.getMemoryList();
        setMemoryCount(mem?.count || 0);
      } catch {}
    };
    checkState();
    const interval = setInterval(checkState, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="memory-sec-card tactical-panel tactical-corner">
      <div className="memsec-header">
        <span className="hud-title">MEMORY & SECURITY</span>
        {/* Segmented signal level bar */}
        <div className="signal-level-bars">
          <span className="bar active"></span>
          <span className="bar active"></span>
          <span className="bar active"></span>
          <span className="bar active"></span>
          <span className="bar active"></span>
        </div>
      </div>

      <div className="memsec-rows">
        <div className="memsec-row">
          <div className="memsec-row-left">
            <span className="indicator-dot emerald"></span>
            <span className="row-text">Status</span>
          </div>
          <span className="badge-pill emerald">STATUS</span>
        </div>

        <div className="memsec-row">
          <div className="memsec-row-left">
            <Lock size={13} className="row-icon emerald" />
            <span className="row-text">Secure Encryption Keys</span>
          </div>
          <span className="badge-pill emerald">SECURE</span>
        </div>

        <div className="memsec-row">
          <div className="memsec-row-left">
            <ShieldCheck size={13} className="row-icon emerald" />
            <span className="row-text">Security Network Levels</span>
          </div>
          <span className="badge-pill emerald">ACTIVE</span>
        </div>
      </div>

      {/* Action Footer for Memory Vault & Security Protocol */}
      <div className="memsec-footer">
        <button
          className="memsec-action-btn"
          onClick={onOpenMemory}
          title="Open Memory Vault to view or manage stored facts"
        >
          <Database size={13} className="btn-icon" />
          <span>VAULT: {memoryCount} FACTS</span>
        </button>

        <button
          className="memsec-action-btn lock-btn"
          onClick={onOpenSecurity}
          title="Open Security Clearance / Lockdown Protocol"
        >
          <KeyRound size={13} className="btn-icon" />
          <span>SECURITY</span>
        </button>
      </div>
    </div>
  );
}
