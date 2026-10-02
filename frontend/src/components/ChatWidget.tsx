import { useState, type FormEvent } from "react";
import { sendChatMessage } from "../api";
import { useAuth } from "../context/AuthContext";
import { useChatMatches } from "../context/ChatMatchContext";
import "./ChatWidget.css";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

const WELCOME_MESSAGE: ChatMessage = {
  role: "assistant",
  content: "Welcome to Yale Campus Customs! How can I help you?",
};

function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [hasOpened, setHasOpened] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([WELCOME_MESSAGE]);
  const [isSending, setIsSending] = useState(false);
  const { setMatchedProductIds } = useChatMatches();
  const { user } = useAuth();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isSending) return;

    setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
    setInput("");
    setIsSending(true);

    const pageHtml = document.querySelector(".page")?.outerHTML;

    try {
      const { reply, products } = await sendChatMessage(
        trimmed,
        user?.id,
        pageHtml,
      );
      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
      setMatchedProductIds(products.map((p) => p.product_id));
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Something went wrong";
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Sorry, I couldn't reply: ${message}` },
      ]);
    } finally {
      setIsSending(false);
    }
  }

  return (
    <div className="chat-widget">
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>Campus Customs Chat</span>
            <button
              className="chat-close-button"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              &times;
            </button>
          </div>
          <div className="chat-messages">
            {messages.map((m, i) => (
              <div key={i} className={`chat-message chat-message-${m.role}`}>
                {m.content}
              </div>
            ))}
          </div>
          <form className="chat-input-row" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
              disabled={isSending}
            />
            <button type="submit" disabled={isSending}>
              Send
            </button>
          </form>
        </div>
      )}
      <button
        className={
          hasOpened ? "chat-toggle-button" : "chat-toggle-button chat-toggle-attention"
        }
        onClick={() => {
          setIsOpen((prev) => !prev);
          setHasOpened(true);
        }}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? "✕" : "Chat"}
      </button>
    </div>
  );
}

export default ChatWidget;
