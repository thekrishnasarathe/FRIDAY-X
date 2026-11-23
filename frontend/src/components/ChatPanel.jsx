import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import {
  Send,
  Mic,
  Sparkles,
  Zap,
  Terminal,
  Activity,
  CheckCircle2,
  ChevronDown,
  ChevronRight,
  Code2,
} from 'lucide-react';
import { api } from '../services/api';
import CodeCard from './CodeCard';
import './ChatPanel.css';

const CONTEXT_CHIPS = {
  assistant: [
    { label: 'System status & telemetry', prompt: 'run system status check' },
    { label: 'Morning briefing & news', prompt: 'give me morning briefing and top news' },
    { label: 'FRIDAY capability audit', prompt: 'what are your active capabilities?' },
  ],
  coding: [
    { label: 'print star pattern in python', prompt: 'print star pattern in python' },
    { label: 'QuickSort with Big-O complexity', prompt: 'write quicksort in python and explain time complexity' },
    { label: 'Debug React async useEffect', prompt: 'how to safely use async cleanup in React useEffect?' },
  ],
  study: [
    { label: 'Explain Quantum Entanglement', prompt: 'explain quantum entanglement in simple terms' },
    { label: 'Active recall quiz: CS concepts', prompt: 'give me a 3-question active recall quiz on OS scheduling' },
    { label: 'Spaced repetition revision', prompt: 'summarize Bayes theorem with real world intuition' },
  ],
};

export default function ChatPanel({
  activeMode = 'assistant',
  onTriggerVoice,
  voiceInput,
  onClearVoiceInput,
}) {
  const [messages, setMessages] = useState([
    {
      id: 1,
      from: 'friday',
      text: 'Systems online. Ready for your command, Boss. 🟢',
      toolCalls: [],
    },
  ]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [activeToolPill, setActiveToolPill] = useState(null); // { tool, label, status }
  const endRef = useRef(null);

  // Auto-scroll when messages or stream changes
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, activeToolPill]);

  // Handle external voice input from VoiceCore
  useEffect(() => {
    if (voiceInput) {
      handleSend(voiceInput);
      if (onClearVoiceInput) onClearVoiceInput();
    }
  }, [voiceInput]);

  const handleSend = async (messageText) => {
    const textToSend = (messageText || input).trim();
    if (!textToSend || isStreaming) return;

    setInput('');
    const userMsgId = Date.now();
    const assistantMsgId = userMsgId + 1;

    // Append user message
    setMessages((prev) => [
      ...prev,
      { id: userMsgId, from: 'user', text: textToSend },
    ]);

    setIsStreaming(true);
    setActiveToolPill(null);

    // Initial placeholder for assistant message
    setMessages((prev) => [
      ...prev,
      {
        id: assistantMsgId,
        from: 'friday',
        text: '',
        toolCalls: [],
        streaming: true,
      },
    ]);

    let accumulatedText = '';
    const executedTools = [];

    // Stream from backend agent
    await api.streamMessage({
      message: textToSend,
      mode: activeMode,
      history: messages.slice(-6).map((m) => ({
        role: m.from === 'user' ? 'user' : 'assistant',
        text: m.text,
      })),
      onStatus: (statusText) => {
        // e.g. "INITIALIZING NEURAL LINK..."
      },
      onTool: (toolEvent) => {
        if (toolEvent.status === 'active') {
          setActiveToolPill({
            tool: toolEvent.tool,
            label: toolEvent.label || `EXECUTING ${toolEvent.tool.toUpperCase()}...`,
            status: 'ACTIVE',
          });
        } else if (toolEvent.status === 'completed') {
          executedTools.push(toolEvent);
          setActiveToolPill({
            tool: toolEvent.tool,
            label: toolEvent.label || `${toolEvent.tool.toUpperCase()} COMPLETED`,
            status: 'COMPLETED',
          });
          setTimeout(() => setActiveToolPill(null), 2500);
        }
      },
      onToken: (token) => {
        accumulatedText += token;
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? { ...msg, text: accumulatedText, toolCalls: [...executedTools] }
              : msg
          )
        );
      },
      onMeta: (meta) => {
        // e.g. latency, model name
      },
      onDone: () => {
        setIsStreaming(false);
        setActiveToolPill(null);
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === assistantMsgId
              ? { ...msg, streaming: false, toolCalls: [...executedTools] }
              : msg
          )
        );
      },
      onError: (err) => {
        setIsStreaming(false);
        setActiveToolPill(null);
      },
    });
  };

  const handleChipClick = (prompt) => {
    handleSend(prompt);
  };

  const chips = CONTEXT_CHIPS[activeMode] || CONTEXT_CHIPS.assistant;

  return (
    <div className="chat-workspace-panel tactical-panel tactical-corner">
      {/* ─── Communication Link Header ───────────────────── */}
      <div className="chat-link-header">
        <div className="link-title-group">
          <Zap size={14} className="link-bolt-icon glow-cyan" />
          <span className="hud-title">COMMUNICATION LINK</span>
        </div>
        <div className="link-status-dot glow-emerald"></div>
      </div>

      {/* ─── Messages Execution Stream ───────────────────── */}
      <div className="chat-stream-viewport">
        {messages.map((m) => {
          const isUser = m.from === 'user';
          return (
            <div key={m.id} className={`stream-row ${isUser ? 'user-row' : 'friday-row'}`}>
              <div className={`stream-bubble ${isUser ? 'user-bubble' : 'friday-bubble'}`}>
                {/* Render tools run before this message */}
                {m.toolCalls && m.toolCalls.length > 0 && (
                  <div className="message-tools-badges">
                    {m.toolCalls.map((tc, idx) => (
                      <div key={idx} className="tool-executed-badge">
                        <CheckCircle2 size={12} className="tool-done-icon" />
                        <span>{tc.label || tc.tool.toUpperCase()}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Markdown text with custom code renderer */}
                {isUser ? (
                  <p className="user-plain-text">{m.text}</p>
                ) : (
                  <div className="markdown-prose">
                    <ReactMarkdown
                      components={{
                        code({ node, inline, className, children, ...props }) {
                          const match = /language-(\w+)/.exec(className || '');
                          if (!inline) {
                            return (
                              <CodeCard language={match ? match[1] : 'code'}>
                                {children}
                              </CodeCard>
                            );
                          }
                          return (
                            <code className="inline-code" {...props}>
                              {children}
                            </code>
                          );
                        },
                      }}
                    >
                      {m.text || (m.streaming ? '▍' : '')}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* ─── Active Tool Execution Pill (Golden/Amber loader) ── */}
        {activeToolPill && (
          <div className="active-tool-execution-pill">
            <div className="tool-pill-left">
              <Sparkles size={14} className="tool-spark-icon" />
              <div className="tool-pill-text">
                <span className="tool-pill-title">{activeToolPill.label}</span>
                <span className="tool-pill-status">STATUS: {activeToolPill.status}</span>
              </div>
            </div>
            <div className="tool-pill-spinner"></div>
          </div>
        )}

        <div ref={endRef} />
      </div>

      {/* ─── Contextual Prompt Chips ─────────────────────── */}
      <div className="context-chips-bar">
        {chips.map((chip, i) => (
          <button
            key={i}
            className="context-chip-btn"
            onClick={() => handleChipClick(chip.prompt)}
            disabled={isStreaming}
          >
            <span>{chip.label}</span>
          </button>
        ))}
      </div>

      {/* ─── Input Bar ───────────────────────────────────── */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="chat-command-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a command or talk to FRIDAY..."
          className="command-hud-input"
          disabled={isStreaming}
        />

        <div className="command-bar-actions">
          <button
            type="button"
            className="action-mic-btn"
            onClick={onTriggerVoice}
            title="Voice Command"
          >
            <Mic size={16} />
          </button>
          <button
            type="submit"
            disabled={!input.trim() || isStreaming}
            className="action-send-btn"
            title="Transmit Command"
          >
            <Send size={15} />
          </button>
        </div>
      </form>
    </div>
  );
}
