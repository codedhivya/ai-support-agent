"use client";

import { useEffect, useState } from "react";

import ChatWindow from "@/components/ChatWindow";

import { createSession, askQuestion } from "@/services/chat";

interface Message {
  role: string;
  content: string;
}

export default function ChatPage() {
  const [sessionId, setSessionId] = useState("");

  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState<Message[]>([]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    initializeSession();
  }, []);

  const initializeSession = async () => {
    try {
      const session = await createSession();

      setSessionId(session.session_id);

      console.log("Session:", session.session_id);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentQuestion = question;

    setQuestion("");

    try {
      setLoading(true);

      const response = await askQuestion(sessionId, currentQuestion);

      const aiMessage = {
        role: "assistant",
        content: response.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-6">AI Support Assistant</h1>

        <ChatWindow messages={messages} />

        <div className="mt-4 flex gap-2">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask a question..."
            className="flex-1 border rounded-lg p-3"
          />

          <button
            onClick={handleSend}
            disabled={loading}
            className="bg-blue-600 text-white px-6 rounded-lg"
          >
            {loading ? "Sending..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
