'use client';

import { useState } from 'react';
import { parseQuery } from '@/lib/nl/parse';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatBotProps {
  onQuery?: (query: string) => void;
}

export function ChatBot({ onQuery }: ChatBotProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content:
        'Hi! Ask me about the simulation:\n• "Where is charisma most important?"\n• "Which region funds the most AI companies?"\n• "Compare Champion vs RevenueFirst"',
    },
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setInput('');
    setIsLoading(true);

    // Parse the query
    const parsed = parseQuery(userMessage);

    // Simple response based on intent
    let response = '';
    switch (parsed.intent) {
      case 'FEATURE_IMPORTANCE':
        response = `Great question! According to the simulation data, **${parsed.slots.feature || 'charisma'}** varies significantly across regions. Bay Area tends to value narrative-driven traits like charisma and vision, while NYC prioritizes revenue and traction.`;
        break;
      case 'FUNDING_LIKELIHOOD':
        response = `Based on your profile, your funding likelihood varies by region. Check the "Regional Funding Distribution" chart above to see which ecosystem is the best fit!`;
        break;
      case 'COMPARE':
        response = `Comparing **${parsed.slots.personaA}** vs **${parsed.slots.personaB}**: These personas have different trait profiles that appeal to different regional ecosystems. Navigate to the Founder page for detailed comparison charts.`;
        break;
      case 'DOMAIN_STAGE_MIX':
        response = `Looking at domain breakdown: AI and Enterprise dominate funding, with regional preferences varying significantly. See the "Funding by Domain" chart above!`;
        break;
      default:
        response =
          "I understand you're asking about the simulation, but I'm not sure exactly what you need. Try asking:\n• Where is [trait] most important?\n• What are my chances of getting funded?\n• Compare [persona] vs [persona]";
    }

    setTimeout(() => {
      setMessages((prev) => [...prev, { role: 'assistant', content: response }]);
      setIsLoading(false);
    }, 500);

    if (onQuery) {
      onQuery(userMessage);
    }
  };

  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <h3 className="text-lg font-semibold mb-4 section-title">Ask Questions</h3>

      <div className="space-y-4 mb-4 max-h-[400px] overflow-y-auto">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                msg.role === 'user'
                  ? 'bg-accent-egypt text-white'
                  : 'bg-muted text-foreground'
              }`}
            >
              <p className="text-sm whitespace-pre-line">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-muted rounded-lg px-4 py-2">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-accent-egypt rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-accent-egypt rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-accent-egypt rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about regions, traits, or funding..."
          className="flex-1 px-4 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent-egypt"
          disabled={isLoading}
        />
        <button
          type="submit"
          disabled={isLoading || !input.trim()}
          className="px-6 py-2 bg-accent-egypt text-white rounded-lg hover:bg-accent-egypt-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Send
        </button>
      </form>
    </div>
  );
}
