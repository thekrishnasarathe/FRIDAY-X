import { useState, useRef, useEffect } from 'react';
import { api } from '../services/api';

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { id: 1, from: 'friday', text: 'Systems online. Ready for your command, Boss. 🟢' }
  ]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const endRef = useRef(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages, typing]);

  const send = async (e) => {
    e?.preventDefault();
    if (!input.trim()) return;
    const txt = input.trim();
    setInput('');
    setMessages(p => [...p, { id: Date.now(), from: 'user', text: txt }]);
    setTyping(true);

    try {
      const res = await api.sendMessage(txt, false);
      setMessages(p => [...p, { id: Date.now()+1, from: 'friday', text: res.friday_response || 'Error.' }]);
    } catch {
      setMessages(p => [...p, { id: Date.now()+1, from: 'friday', text: 'Connection lost to core server.' }]);
    }
    setTyping(false);
  };

  return (
    <div className="chat-panel glass">
      <div className="chat-head">
        <span className="hud-label">⚡ Communication Link</span>
        <span className="online-dot"></span>
      </div>

      <div className="chat-messages">
        {messages.map(m => (
          <div key={m.id} className={`msg ${m.from}`}>
            <div className={`bubble ${m.from}`}>{m.text}</div>
          </div>
        ))}
        {typing && (
          <div className="msg friday">
            <div className="bubble friday typing"><span/><span/><span/></div>
          </div>
        )}
        <div ref={endRef} />
      </div>

      <form onSubmit={send} className="chat-bar">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a command or talk to FRIDAY..."
          className="chat-input"
        />
        <button type="submit" disabled={!input.trim()} className="send-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="m22 2-7 20-4-9-9-4Z"/><path d="m22 2-11 11"/></svg>
        </button>
      </form>
    </div>
  );
}
