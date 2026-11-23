import React, { useState } from 'react';
import { Copy, Check, Terminal } from 'lucide-react';

export default function CodeCard({ language = 'python', children }) {
  const [copied, setCopied] = useState(false);

  const codeText = String(children).replace(/\n$/, '');
  const lines = codeText.split('\n');

  const handleCopy = () => {
    navigator.clipboard.writeText(codeText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="tactical-code-card">
      <div className="code-card-header">
        <div className="code-card-lang">
          <Terminal size={13} className="lang-icon" />
          <span>{language.toUpperCase()}</span>
        </div>
        <button className="code-copy-btn" onClick={handleCopy}>
          {copied ? (
            <>
              <Check size={13} className="copy-icon check" />
              <span>COPIED</span>
            </>
          ) : (
            <>
              <Copy size={13} className="copy-icon" />
              <span>COPY CODE</span>
            </>
          )}
        </button>
      </div>

      <div className="code-card-body">
        <div className="code-gutter">
          {lines.map((_, i) => (
            <span key={i} className="line-num">{i + 1}</span>
          ))}
        </div>
        <pre className="code-pre">
          <code>{codeText}</code>
        </pre>
      </div>
    </div>
  );
}
