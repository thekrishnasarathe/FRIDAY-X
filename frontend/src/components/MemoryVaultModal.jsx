import React, { useState, useEffect } from 'react';
import { Database, Plus, Trash2, X, Search, ShieldCheck } from 'lucide-react';
import { api } from '../services/api';
import './MemoryVaultModal.css';

export default function MemoryVaultModal({ isOpen, onClose }) {
  const [facts, setFacts] = useState({});
  const [search, setSearch] = useState('');
  const [newKey, setNewKey] = useState('');
  const [newVal, setNewVal] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadMemories();
    }
  }, [isOpen]);

  const loadMemories = async () => {
    try {
      const data = await api.getMemoryList();
      setFacts(data?.facts || {});
    } catch {}
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!newKey.trim() || !newVal.trim()) return;
    setIsSaving(true);
    try {
      await api.addMemory(newKey.trim(), newVal.trim());
      setNewKey('');
      setNewVal('');
      await loadMemories();
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (key) => {
    try {
      await api.deleteMemory(key);
      await loadMemories();
    } catch {}
  };

  if (!isOpen) return null;

  const factEntries = Object.entries(facts).filter(([k, v]) =>
    k.toLowerCase().includes(search.toLowerCase()) ||
    String(v).toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="vault-overlay">
      <div className="vault-modal tactical-panel tactical-corner">
        <div className="vault-modal-header">
          <div className="vault-title-wrap">
            <Database className="vault-header-icon" size={20} />
            <h2>MEMORY VAULT // PERSISTENT CONTEXT</h2>
          </div>
          <button className="vault-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Add Fact Form */}
        <form onSubmit={handleAdd} className="vault-add-form">
          <input
            className="vault-input"
            placeholder="Fact Key (e.g. preferred_stack)..."
            value={newKey}
            onChange={(e) => setNewKey(e.target.value)}
          />
          <input
            className="vault-input"
            placeholder="Detail (e.g. FastAPI + React)..."
            value={newVal}
            onChange={(e) => setNewVal(e.target.value)}
          />
          <button type="submit" disabled={isSaving || !newKey.trim()} className="vault-save-btn">
            <Plus size={16} />
            <span>STORE</span>
          </button>
        </form>

        {/* Search */}
        <div className="vault-search-box">
          <Search size={15} className="search-icon" />
          <input
            className="vault-search-input"
            placeholder="Search stored memory..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        {/* Facts List */}
        <div className="vault-facts-list">
          {factEntries.length === 0 ? (
            <div className="vault-empty-state">
              <ShieldCheck size={32} className="empty-icon" />
              <p>NO MEMORY RECORDS MATCH QUERY</p>
            </div>
          ) : (
            factEntries.map(([k, v]) => (
              <div key={k} className="vault-fact-item">
                <div className="vault-fact-content">
                  <span className="fact-key">{k}</span>
                  <span className="fact-val">{String(v)}</span>
                </div>
                <button
                  className="fact-delete-btn"
                  onClick={() => handleDelete(k)}
                  title="Delete from memory"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
