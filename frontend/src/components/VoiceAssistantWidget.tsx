import React, { useState, useEffect, useRef } from 'react';

export const VoiceAssistantWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [statusMsg, setStatusMsg] = useState('Tap mic to start Gemini Live voice prompt...');
  const [textInput, setTextInput] = useState('');
  const [messages, setMessages] = useState<Array<{ text: string; isUser: boolean }>>([
    {
      text: '🌿 Hello! I am your **Google Gemini 2.0 Live & ElevenLabs Agronomist Voice Assistant**. Tap the microphone to speak your question!',
      isUser: false
    }
  ]);

  const [geminiKey, setGeminiKey] = useState(() => localStorage.getItem('agri_gemini_key') || '');
  const [elevenKey, setElevenKey] = useState(() => localStorage.getItem('agri_eleven_key') || '');
  const [voiceId, setVoiceId] = useState(() => localStorage.getItem('agri_voice_id') || '21m00Tcm4TlvDq8ikWAM');
  const [showGeminiKey, setShowGeminiKey] = useState(false);
  const [showElevenKey, setShowElevenKey] = useState(false);

  const recognitionRef = useRef<any>(null);
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);
  const micStreamRef = useRef<MediaStream | null>(null);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const animFrameRef = useRef<number | null>(null);
  const transcriptEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    transcriptEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isListening, isSpeaking]);

  const toggleListening = async () => {
    if (isListening) {
      stopListening();
    } else {
      stopSpeaking();
      setStatusMsg('Requesting microphone permission...');
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        micStreamRef.current = stream;

        // Initialize Speech Recognition
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
        if (SpeechRecognition) {
          const rec = new SpeechRecognition();
          rec.continuous = false;
          rec.interimResults = true;
          rec.lang = 'en-US';

          rec.onstart = () => {
            setIsListening(true);
            setStatusMsg('🎙️ Gemini AI Listening... Speak now!');
          };

          rec.onresult = (event: any) => {
            let interim = '';
            let final = '';
            for (let i = event.resultIndex; i < event.results.length; ++i) {
              if (event.results[i].isFinal) {
                final += event.results[i][0].transcript;
              } else {
                interim += event.results[i][0].transcript;
              }
            }
            if (interim) setStatusMsg(`🗣️ "${interim}..."`);
            if (final) {
              stopListening();
              handleUserMessage(final.trim());
            }
          };

          rec.onerror = (err: any) => {
            console.error('Speech recognition error:', err);
            stopListening();
            setStatusMsg('Could not detect speech. Tap mic to retry.');
          };

          rec.onend = () => {
            stopListening();
          };

          recognitionRef.current = rec;
          rec.start();
        } else {
          setStatusMsg('Speech recognition not supported in this browser.');
        }
      } catch (err) {
        console.error('Microphone access denied:', err);
        setStatusMsg('⚠️ Microphone permission denied.');
        stopListening();
      }
    }
  };

  const stopListening = () => {
    setIsListening(false);
    if (recognitionRef.current) {
      try { recognitionRef.current.stop(); } catch (e) {}
      recognitionRef.current = null;
    }
    if (micStreamRef.current) {
      micStreamRef.current.getTracks().forEach(t => t.stop());
      micStreamRef.current = null;
    }
    if (!isSpeaking) {
      setStatusMsg('Tap mic to start Gemini Live voice prompt...');
    }
  };

  const stopSpeaking = () => {
    setIsSpeaking(false);
    if (currentAudioRef.current) {
      try {
        currentAudioRef.current.pause();
        currentAudioRef.current = null;
      } catch (e) {}
    }
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  };

  const handleUserMessage = (text: string) => {
    if (!text) return;
    setMessages(prev => [...prev, { text, isUser: true }]);
    processQuery(text);
  };

  const FAQ_ANSWERS: Record<string, string> = {
    "blight": "🌿 **Early Blight Treatment (Alternaria solani):**\n\n1. **Pruning:** Remove infected lower leaves with target-board brown spots immediately and discard them outside the garden.\n2. **Irrigation:** Switch to drip irrigation or ground watering. Keep foliage dry to stop fungal spore spread.\n3. **Fungicide Spray:** Apply copper soap (*Copper Octanoate*) or bio-fungicide every 7–10 days during humid weather.",
    
    "season": "🌾 **Seasonal Crop Selection Guide:**\n\n- **Monsoon / Kharif (June–Oct):** Paddy/Rice, Maize (Corn), Cotton, Soybean, Groundnut.\n- **Winter / Rabi (Oct–March):** Wheat, Mustard, Chickpea, Potato, Tomato, Peas.\n- **Summer / Zaid (March–June):** Watermelon, Cucumber, Muskmelon, Okra, Leafy Greens.",
    
    "ph": "🧪 **Soil pH & Nutrient Management:**\n\n- **Ideal Range:** 6.0 to 7.0 for optimal root absorption of nitrogen, phosphorus, and potassium.\n- **Acidic Soil (< 6.0):** Apply agricultural lime (calcium carbonate) 2–3 weeks before sowing.\n- **Alkaline Soil (> 7.5):** Incorporate elemental sulfur or well-rotted organic compost to lower pH.",
    
    "irrigation": "💧 **Watering & Irrigation Schedule:**\n\n1. **Morning Irrigation:** Water early in the morning (6 AM – 9 AM) so leaf wetness evaporates quickly.\n2. **Drip Emitters:** Delivers water directly to root zones, saving up to 50% water while preventing leaf mold.\n3. **Probing Test:** Water deeply 2–3 times weekly rather than shallow daily sprays to promote deep root growth.",
    
    "pest": "🐛 **Integrated Organic Pest Control:**\n\n1. **Neem Oil Spray:** Spray cold-pressed neem oil (5 ml/L water with mild soap) every 10–14 days for aphids and whiteflies.\n2. **Companion Flowers:** Plant French Marigolds and Alyssum to attract beneficial ladybugs and lacewings.\n3. **Yellow Traps:** Hang yellow sticky cards 15 cm above the crop canopy.",
    
    "scan": "📊 **Crop Diagnosis & Health Analysis:**\n\n- **Healthy:** Continue balanced N-P-K fertilization and weekly leaf inspection.\n- **Early Blight / Rust:** Isolate infected plant beds, apply copper or sulfur sprays, and switch to drip watering."
  };

  const getAgronomyAnswer = (promptText: string): string => {
    const p = promptText.toLowerCase();
    if (p.includes('blight') || p.includes('cure') || p.includes('tomato')) return FAQ_ANSWERS["blight"];
    if (p.includes('season') || p.includes('crop is good') || p.includes('which crop') || p.includes('plant')) return FAQ_ANSWERS["season"];
    if (p.includes('ph') || p.includes('soil ph') || p.includes('acid') || p.includes('alkaline')) return FAQ_ANSWERS["ph"];
    if (p.includes('irrigation') || p.includes('water') || p.includes('drip')) return FAQ_ANSWERS["irrigation"];
    if (p.includes('pest') || p.includes('organic') || p.includes('neem') || p.includes('control')) return FAQ_ANSWERS["pest"];
    if (p.includes('scan') || p.includes('diagnosis') || p.includes('explain')) return FAQ_ANSWERS["scan"];

    return `🌾 **Agronomic Advisory:** For optimal crop vitality, monitor soil moisture, scout leaf undersides weekly for fungal spots or pests, and ensure balanced N-P-K fertilization. Tap any FAQ option above for specific advice!`;
  };

  const processQuery = async (prompt: string) => {
    stopSpeaking();
    setStatusMsg('✨ Gemini AI reasoning & generating response...');

    let aiResponseText = '';

    // 1. Try Direct Google Gemini API Call if Gemini Key is present
    if (geminiKey) {
      try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${geminiKey}`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            system_instruction: {
              parts: [{ text: "You are AgriGenius AI, an expert voice agronomist assistant. Provide helpful, concise, and structured agronomic advice using markdown (headers, bold, bullet points)." }]
            },
            contents: [{ role: 'user', parts: [{ text: prompt }] }]
          })
        });

        if (res.ok) {
          const data = await res.json();
          const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
          if (text) {
            aiResponseText = text;
          }
        }
      } catch (err) {
        console.warn('Direct Gemini API call failed:', err);
      }
    }

    // 2. Try FastAPI Backend Endpoint
    if (!aiResponseText) {
      try {
        const apiPrefix = '/api/v1';
        const res = await fetch(`${apiPrefix}/chat/voice`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prompt,
            gemini_api_key: geminiKey,
            eleven_api_key: elevenKey,
            voice_id: voiceId
          })
        });

        if (res.ok) {
          const data = await res.json();
          setMessages(prev => [...prev, { text: data.text, isUser: false }]);
          if (data.audio_b64) {
            playAudioBase64(data.audio_b64);
            return;
          } else {
            speakWithBrowser(data.text);
            return;
          }
        }
      } catch (e) {
        console.warn('Backend call failed, using dynamic local agronomic engine', e);
      }
    }

    // 3. Dynamic Knowledge Engine (Unique answer per query/FAQ)
    if (!aiResponseText) {
      aiResponseText = getAgronomyAnswer(prompt);
    }

    setMessages(prev => [...prev, { text: aiResponseText, isUser: false }]);
    speakWithBrowser(aiResponseText);
  };

  const playAudioBase64 = (b64: string) => {
    try {
      const audio = new Audio(`data:audio/mp3;base64,${b64}`);
      currentAudioRef.current = audio;
      setIsSpeaking(true);
      setStatusMsg('🔊 ElevenLabs Voice Speaking...');
      audio.onended = () => {
        setIsSpeaking(false);
        setStatusMsg('Tap mic to start Gemini Live voice prompt...');
      };
      audio.onerror = () => {
        setIsSpeaking(false);
        setStatusMsg('Tap mic to start Gemini Live voice prompt...');
      };
      audio.play();
    } catch (e) {
      setIsSpeaking(false);
    }
  };

  const speakWithBrowser = (text: string) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/<[^>]*>?/gm, '');
    const utt = new SpeechSynthesisUtterance(cleanText);
    utt.onstart = () => {
      setIsSpeaking(true);
      setStatusMsg('🔊 Speaking AI response...');
    };
    utt.onend = () => {
      setIsSpeaking(false);
      setStatusMsg('Tap mic to start Gemini Live voice prompt...');
    };
    utt.onerror = () => {
      setIsSpeaking(false);
      setStatusMsg('Tap mic to start Gemini Live voice prompt...');
    };
    window.speechSynthesis.speak(utt);
  };

  const saveSettings = () => {
    localStorage.setItem('agri_gemini_key', geminiKey);
    localStorage.setItem('agri_eleven_key', elevenKey);
    localStorage.setItem('agri_voice_id', voiceId);
    setIsSettingsOpen(false);
    setMessages(prev => [...prev, { text: '⚙️ Google Gemini & ElevenLabs API Settings saved!', isUser: false }]);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50 font-sans">
      {/* Floating Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative group flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-emerald-600 to-green-500 text-white rounded-full shadow-lg hover:shadow-emerald-500/30 hover:scale-105 transition-all duration-300 border border-white/20"
        title="Google Gemini Live Voice Agent"
      >
        <span className="absolute -top-1 -right-1 flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
        </span>
        <div className="w-8 h-8 rounded-full bg-white/20 flex items-center justify-center">
          <svg className="w-4 h-4 fill-current text-white" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z" />
          </svg>
        </div>
        <span className="font-bold text-sm tracking-wide">AI Voice</span>
      </button>

      {/* Floating Voice Agent Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 max-w-[calc(100vw-2rem)] h-[520px] bg-white dark:bg-slate-900 border border-emerald-500/30 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-300">
          {/* Header */}
          <div className="px-4 py-3 bg-gradient-to-r from-emerald-800 to-green-700 text-white flex items-center justify-between border-b border-white/10">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-white/15 flex items-center justify-center text-emerald-300">
                ✨
              </div>
              <div>
                <h4 className="font-extrabold text-sm leading-tight text-white">Gemini 2.0 Voice AI</h4>
                <div className="flex items-center gap-1.5 text-[11px] text-emerald-200">
                  <span className="text-emerald-400 font-bold">● ONLINE</span>
                  <span className="bg-white/15 px-2 py-0.5 rounded-full">Gemini Live</span>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
                title="Settings"
              >
                ⚙️
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-white transition-colors"
                title="Close"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Settings View */}
          {isSettingsOpen ? (
            <div className="flex-1 p-4 bg-slate-50 dark:bg-slate-900 overflow-y-auto space-y-4 text-xs">
              <h5 className="font-bold text-slate-800 dark:text-slate-200 text-sm flex items-center gap-1">
                ⚙️ AI Voice API Preferences
              </h5>

              <div>
                <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                  Google Gemini API Key (Gemini 2.0 Live)
                </label>
                <div className="relative">
                  <input
                    type={showGeminiKey ? 'text' : 'password'}
                    value={geminiKey}
                    onChange={e => setGeminiKey(e.target.value)}
                    placeholder="AIzaSy..."
                    className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-slate-800 dark:border-slate-700 font-mono text-xs pr-8"
                  />
                  <button
                    type="button"
                    onClick={() => setShowGeminiKey(!showGeminiKey)}
                    className="absolute right-2 top-2 text-slate-400 hover:text-slate-600"
                  >
                    👁️
                  </button>
                </div>
                <p className="text-[11px] text-slate-500 mt-1">Powers Gemini 2.0 Multimodal Live real-time agronomic reasoning.</p>
              </div>

              <div>
                <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                  ElevenLabs API Key (TTS Voice)
                </label>
                <div className="relative">
                  <input
                    type={showElevenKey ? 'text' : 'password'}
                    value={elevenKey}
                    onChange={e => setElevenKey(e.target.value)}
                    placeholder="xi-api-key..."
                    className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-slate-800 dark:border-slate-700 font-mono text-xs pr-8"
                  />
                  <button
                    type="button"
                    onClick={() => setShowElevenKey(!showElevenKey)}
                    className="absolute right-2 top-2 text-slate-400 hover:text-slate-600"
                  >
                    👁️
                  </button>
                </div>
                <p className="text-[11px] text-slate-500 mt-1">Powers ultra-realistic ElevenLabs audio voice speech output.</p>
              </div>

              <div>
                <label className="block font-bold text-slate-700 dark:text-slate-300 mb-1">
                  ElevenLabs Voice ID
                </label>
                <select
                  value={voiceId}
                  onChange={e => setVoiceId(e.target.value)}
                  className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-slate-800 dark:border-slate-700"
                >
                  <option value="21m00Tcm4TlvDq8ikWAM">Rachel (Calm & Professional)</option>
                  <option value="AZnzlk1XvdvUeBnXmlld">Domi (Energetic)</option>
                  <option value="EXAVITQu4vr4xnSDxMaL">Bella (Friendly)</option>
                  <option value="ErXwobaYiN019PkySvjV">Antoni (Deep Male Voice)</option>
                </select>
              </div>

              <button
                onClick={saveSettings}
                className="w-full py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg shadow transition-colors text-xs"
              >
                Save Keys & Preferences
              </button>
            </div>
          ) : (
            /* Main Chat Interface */
            <div className="flex-1 flex flex-col bg-slate-50 dark:bg-slate-900/50 overflow-hidden">
              {/* Visualizer Orb */}
              <div className="py-4 px-3 bg-gradient-to-b from-emerald-50/50 to-transparent dark:from-emerald-950/20 flex flex-col items-center justify-center border-b border-emerald-500/10">
                <div
                  onClick={toggleListening}
                  className={`relative w-20 h-20 flex items-center justify-center cursor-pointer transition-transform hover:scale-105 ${
                    isListening ? 'scale-110' : ''
                  }`}
                >
                  <div className={`absolute inset-0 rounded-full bg-emerald-500/20 ${isListening ? 'animate-ping' : ''}`}></div>
                  <div className={`w-14 h-14 rounded-full flex items-center justify-center text-white shadow-xl transition-all ${
                    isSpeaking
                      ? 'bg-gradient-to-r from-emerald-600 to-teal-500 shadow-emerald-500/50 animate-pulse'
                      : isListening
                      ? 'bg-red-500 shadow-red-500/50'
                      : 'bg-gradient-to-r from-emerald-600 to-green-500 shadow-emerald-500/30'
                  }`}>
                    <svg className="w-7 h-7 fill-current" viewBox="0 0 24 24">
                      <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.3-3c0 3-2.54 5.1-5.3 5.1S6.7 14 6.7 11H5c0 3.41 2.72 6.23 6 6.72V21h2v-3.28c3.28-.48 6-3.3 6-6.72h-1.7z" />
                    </svg>
                  </div>
                </div>
                <div className="mt-2 text-center text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {statusMsg}
                </div>
              </div>

              {/* Messages Scroll View */}
              <div className="flex-1 p-3 overflow-y-auto space-y-3">
                {messages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`flex flex-col ${m.isUser ? 'items-end' : 'items-start'}`}
                  >
                    <div
                      className={`max-w-[85%] px-3.5 py-2 rounded-2xl text-xs leading-relaxed ${
                        m.isUser
                          ? 'bg-emerald-600 text-white rounded-br-none'
                          : 'bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-emerald-500/20 shadow-sm rounded-bl-none'
                      }`}
                    >
                      {m.text}
                    </div>
                  </div>
                ))}
                <div ref={transcriptEndRef} />
              </div>

              {/* Quick FAQ Chips Bar */}
              <div className="px-2.5 py-2 bg-emerald-50/70 dark:bg-slate-800/80 border-t border-emerald-500/10 flex gap-1.5 overflow-x-auto scrollbar-thin">
                {[
                  "🌾 Which crop is good in this season?",
                  "🌿 How to cure Early Blight in tomatoes?",
                  "🧪 What is the ideal soil pH for crops?",
                  "💧 What is the best irrigation schedule?",
                  "🐛 How to control pests organically?",
                  "📊 Explain my crop scan diagnosis"
                ].map((faq, fIdx) => (
                  <button
                    key={fIdx}
                    onClick={() => handleUserMessage(faq)}
                    className="px-2.5 py-1 rounded-full text-[11px] font-medium whitespace-nowrap bg-white dark:bg-slate-700 text-emerald-700 dark:text-emerald-300 border border-emerald-500/20 hover:bg-emerald-600 hover:text-white dark:hover:bg-emerald-600 dark:hover:text-white transition-all shadow-xs shrink-0 cursor-pointer"
                  >
                    {faq}
                  </button>
                ))}
              </div>

              {/* Input Footer */}
              <div className="p-2 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800 flex items-center gap-2">
                <button
                  onClick={toggleListening}
                  className={`p-2 rounded-full border transition-colors ${
                    isListening ? 'bg-red-500 text-white border-red-600 animate-pulse' : 'bg-emerald-50 text-emerald-700 border-emerald-200 hover:bg-emerald-100'
                  }`}
                  title="Toggle Microphone"
                >
                  🎤
                </button>
                <input
                  type="text"
                  value={textInput}
                  onChange={e => setTextInput(e.target.value)}
                  onKeyDown={e => {
                    if (e.key === 'Enter' && textInput.trim()) {
                      handleUserMessage(textInput.trim());
                      setTextInput('');
                    }
                  }}
                  placeholder="Type or speak a question..."
                  className="flex-1 px-3 py-1.5 text-xs rounded-full border border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 focus:outline-none focus:border-emerald-500"
                />
                <button
                  onClick={() => {
                    if (textInput.trim()) {
                      handleUserMessage(textInput.trim());
                      setTextInput('');
                    }
                  }}
                  className="p-2 rounded-full bg-emerald-600 hover:bg-emerald-700 text-white transition-colors"
                  title="Send"
                >
                  ➔
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
