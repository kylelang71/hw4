import { createContext, useContext, useState, type ReactNode } from "react";

interface ChatMatchContextValue {
  matchedProductIds: string[];
  setMatchedProductIds: (ids: string[]) => void;
}

const ChatMatchContext = createContext<ChatMatchContextValue | undefined>(
  undefined,
);

export function ChatMatchProvider({ children }: { children: ReactNode }) {
  const [matchedProductIds, setMatchedProductIds] = useState<string[]>([]);

  return (
    <ChatMatchContext.Provider value={{ matchedProductIds, setMatchedProductIds }}>
      {children}
    </ChatMatchContext.Provider>
  );
}

export function useChatMatches() {
  const context = useContext(ChatMatchContext);
  if (!context) {
    throw new Error("useChatMatches must be used within a ChatMatchProvider");
  }
  return context;
}
