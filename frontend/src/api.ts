export const API_BASE_URL = "http://127.0.0.1:8000";

export interface AuthUser {
  id: number;
  first_name: string | null;
  last_name: string | null;
  email: string;
}

async function parseJsonOrThrow(response: Response) {
  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const message = data?.detail ?? "Something went wrong";
    throw new Error(message);
  }
  return data;
}

export async function registerUser(input: {
  first_name: string;
  last_name: string;
  email: string;
  password: string;
  confirm_password: string;
}): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  return parseJsonOrThrow(response);
}

export async function loginUser(input: {
  email: string;
  password: string;
}): Promise<AuthUser> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  return parseJsonOrThrow(response);
}

export interface ChatProductCard {
  product_id: string;
  name: string;
  garment_type: string;
  price: number;
  image_file_path: string;
  short_description: string;
}

export interface ChatReply {
  reply: string;
  tools_used: string[];
  products: ChatProductCard[];
}

export async function sendChatMessage(
  message: string,
  userId?: number,
  pageHtml?: string,
): Promise<ChatReply> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message,
      user_id: userId ?? null,
      page_html: pageHtml ?? null,
    }),
  });
  return parseJsonOrThrow(response);
}
