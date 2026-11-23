import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import './VoiceOrb.css';

export default function VoiceOrb({ onTranscript, mode = 'assistant' }) {
  // states: 'idle' | 'listening' | 'thinking' | 'speaking'
  const [orbState, setOrbState] = useState('idle');
  const [statusText, setStatusText] = useState('VOICE PROTOCOL READY');
  const [micVolume, setMicVolume] = useState(0);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const animFrameRef = useRef(null);

  // Clean up audio context on unmount
  useEffect(() => {
    return () => {
      stopAudioMonitoring();
    };
  }, []);

  const startAudioMonitoring = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;

      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 64;
      analyserRef.current = analyser;

      const source = audioCtx.createMediaStreamSource(stream);
      source.connect(analyser);

      const dataArray = new Uint8Array(analyser.frequencyBinCount);
      const updateVolume = () => {
        analyser.getByteFrequencyData(dataArray);
        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
        }
        const avg = sum / dataArray.length;
        setMicVolume(Math.min(100, Math.round((avg / 128) * 100)));
        animFrameRef.current = requestAnimationFrame(updateVolume);
      };
      updateVolume();
    } catch {
      setMicVolume(35); // fallback animated simulation
    }
  };

  const stopAudioMonitoring = () => {
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach(t => t.stop());
      mediaStreamRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
    setMicVolume(0);
  };

  const handleOrbClick = async () => {
    if (orbState === 'listening' || orbState === 'thinking') return;

    setOrbState('listening');
    setStatusText('LISTENING TO COMMAND...');
    startAudioMonitoring();

    // Use browser SpeechRecognition if available for instantaneous local capture
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRec) {
      const recognition = new SpeechRec();
      recognition.lang = 'en-US';
      recognition.interimResults = false;
      recognition.maxAlternatives = 1;

      recognition.onresult = async (event) => {
        stopAudioMonitoring();
        const spoken = event.results[0][0].transcript;
        setOrbState('thinking');
        setStatusText(`PROCESSING: "${spoken}"`);

        if (onTranscript) {
          onTranscript(spoken);
        }

        setTimeout(() => {
          setOrbState('idle');
          setStatusText('VOICE PROTOCOL READY');
        }, 3000);
      };

      recognition.onerror = async () => {
        stopAudioMonitoring();
        fallbackBackendListen();
      };

      try {
        recognition.start();
      } catch {
        fallbackBackendListen();
      }
    } else {
      fallbackBackendListen();
    }
  };

  const fallbackBackendListen = async () => {
    setOrbState('thinking');
    setStatusText('ROUTING TO NEURAL SERVER...');
    try {
      const res = await api.voiceListen();
      stopAudioMonitoring();
      if (res?.command && onTranscript) {
        onTranscript(res.command);
        setOrbState('speaking');
        setStatusText(`EXECUTED: "${res.command}"`);
      } else {
        setStatusText(res?.response || 'NO AUDIO DETECTED');
      }
    } catch {
      stopAudioMonitoring();
      setStatusText('MIC HARDWARE UNAVAILABLE');
    }
    setTimeout(() => {
      setOrbState('idle');
      setStatusText('VOICE PROTOCOL READY');
    }, 3500);
  };

  return (
    <div className="voice-core-card tactical-panel tactical-corner">
      <div className="voice-core-header">
        <span className="hud-title">VOICE CORE</span>
        <span className={`voice-state-pill ${orbState}`}>
          {orbState.toUpperCase()}
        </span>
      </div>

      <div className="reactor-stage">
        {/* Holographic Arc Reactor */}
        <div
          className={`arc-reactor-core ${orbState}`}
          onClick={handleOrbClick}
          title="Click to activate Voice Command"
        >
          {/* Rotating outer compass ticks */}
          <div className="reactor-ticks"></div>
          {/* Conic spinning ring */}
          <div className="reactor-conic-ring"></div>
          {/* Inner pulse ring */}
          <div
            className="reactor-inner-ring"
            style={{
              transform: orbState === 'listening' ? `scale(${1 + micVolume * 0.005})` : undefined,
              boxShadow: orbState === 'listening' ? `0 0 ${15 + micVolume * 0.3}px var(--cyan)` : undefined,
            }}
          ></div>

          {/* Central Holographic Icon */}
          <div className="reactor-center-node">
            {orbState === 'idle' && <Mic className="reactor-icon idle" size={24} />}
            {orbState === 'listening' && <Mic className="reactor-icon listening" size={26} />}
            {orbState === 'thinking' && <Loader2 className="reactor-icon spinning" size={26} />}
            {orbState === 'speaking' && <Volume2 className="reactor-icon speaking" size={26} />}
          </div>
        </div>

        {/* Ambient audio visualizer bars */}
        <div className="audio-cadence-bars">
          {[18, 42, 65, 95, 75, 45, 20].map((h, i) => (
            <span
              key={i}
              className={`cadence-bar ${orbState}`}
              style={{
                height: orbState === 'listening'
                  ? `${Math.max(4, Math.round(h * (micVolume / 100)))}px`
                  : orbState === 'thinking' || orbState === 'speaking'
                  ? `${Math.max(6, (h % 30) + 8)}px`
                  : '4px',
              }}
            />
          ))}
        </div>
      </div>

      <div className="voice-status-bar">
        <div className="status-signal-dot"></div>
        <span className="voice-status-text">{statusText}</span>
      </div>
    </div>
  );
}
