import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('FRIDAY Core UI Exception caught by boundary:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'radial-gradient(circle at center, #0f172a 0%, #020617 100%)',
          color: '#38bdf8',
          fontFamily: "'Inter', sans-serif",
          padding: '2rem',
          textAlign: 'center',
        }}>
          <div style={{
            width: '60px',
            height: '60px',
            borderRadius: '50%',
            border: '2px solid #ef4444',
            boxShadow: '0 0 20px rgba(239, 68, 68, 0.4)',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ef4444',
            fontSize: '1.5rem',
            fontWeight: 'bold',
          }}>
            !
          </div>
          <h1 style={{
            fontSize: '1.75rem',
            letterSpacing: '2px',
            textTransform: 'uppercase',
            color: '#f87171',
            margin: '0 0 0.5rem 0',
          }}>
            SYSTEM DIAGNOSTIC ANOMALY
          </h1>
          <p style={{
            color: '#94a3b8',
            maxWidth: '450px',
            lineHeight: '1.5',
            marginBottom: '1.5rem',
            fontSize: '0.95rem',
          }}>
            FRIDAY encountered an unexpected interface fault. Diagnostic protocols have engaged.
          </p>
          <button
            onClick={this.handleReset}
            style={{
              padding: '0.75rem 1.75rem',
              background: 'rgba(56, 189, 248, 0.1)',
              border: '1px solid #38bdf8',
              borderRadius: '8px',
              color: '#38bdf8',
              fontWeight: '600',
              letterSpacing: '1px',
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            REINITIALIZE CORE
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
