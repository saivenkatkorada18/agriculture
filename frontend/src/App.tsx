import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { VoiceAssistantWidget } from './components/VoiceAssistantWidget';
import { LandingPage } from './pages/LandingPage';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyzerPage } from './pages/AnalyzerPage';
import { ResultPage } from './pages/ResultPage';
import { HistoryPage } from './pages/HistoryPage';
import { AssistantPage } from './pages/AssistantPage';
import { EncyclopediaPage } from './pages/EncyclopediaPage';
import { AuthPage } from './pages/AuthPage';

export const App: React.FC = () => {
  const [darkMode, setDarkMode] = useState<boolean>(() => {
    return localStorage.getItem('agri_theme') === 'dark';
  });

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('agri_theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('agri_theme', 'light');
    }
  }, [darkMode]);

  return (
    <BrowserRouter>
      <div className="flex flex-col min-h-screen">
        <Navbar darkMode={darkMode} setDarkMode={setDarkMode} />

        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-6">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/analyze" element={<AnalyzerPage />} />
            <Route path="/results/:id" element={<ResultPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/assistant" element={<AssistantPage />} />
            <Route path="/encyclopedia" element={<EncyclopediaPage />} />
            <Route path="/auth/login" element={<AuthPage initialMode="login" />} />
            <Route path="/auth/signup" element={<AuthPage initialMode="signup" />} />
            <Route path="/auth/forgot-password" element={<AuthPage initialMode="forgot" />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>

        <Footer />
        <VoiceAssistantWidget />
      </div>
    </BrowserRouter>
  );
};

export default App;
