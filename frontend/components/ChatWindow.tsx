"use client";

interface Message {
  role: string;
  content: string;
}

interface ChatWindowProps {
  messages: Message[];
}

export default function ChatWindow({ messages }: ChatWindowProps) {
  return (
    <div className="h-[500px] overflow-y-auto border rounded-lg p-4 bg-gray-50">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`mb-4 flex ${
            message.role === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`max-w-[80%] p-3 rounded-lg ${
              message.role === "user"
                ? "bg-blue-600 text-white"
                : "bg-white border"
            }`}
          >
            {message.content}
          </div>
        </div>
      ))}
    </div>
  );
}
