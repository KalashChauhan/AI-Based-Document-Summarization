import React from 'react';
export default class ErrorBoundary extends React.Component {
  constructor(props) { 
    super(props); 
    this.state = { error: null }; 
  }
  static getDerivedStateFromError(error) { 
    return { error }; 
  }
  render() {
    if (this.state.error) {
      return <main>
        <h1>Something went wrong</h1>
        <p>The frontend could not render. Refresh the page and ensure the Vite terminal is still running.</p>
        <pre className="error">{this.state.error.message}</pre>
        </main>;
    }
    return this.props.children;
  }
}
