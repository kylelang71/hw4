`campus_customs.db` has four tables. **Catalogue**: product_id, name, garment_type, description, colors, search_tags, image_file_path, price. **Inventory**: product_id, size, quantity. **Users**: name, first_name, last_name, email, password_hash, created_at. **Chat_messages**: user_id, role, content, products_json, created_at.

## Account Creation & Login

- `POST /api/auth/register` (`first_name`, `last_name`, `email`, `password`, `confirm_password`): 400 if passwords don't match or are under 8 characters, 409 if the email is taken. On success, hashes the password and inserts into `users`, returning the user's id/name/email only.
- `POST /api/auth/login` (`email`, `password`): verifies against the stored hash; returns the same generic 401 whether the email is unknown or the password is wrong, so the error can't be used to confirm which emails are registered.
- **Hashing** (`backend/auth.py`): PBKDF2-HMAC-SHA256, 120,000 iterations, random 16-byte hex salt per user, stored as `pbkdf2_sha256$<salt>$<hash>`. Verified with a constant-time comparison. Matches the format of the pre-seeded `test@campuscustoms.yale.edu` / `password` account.
- **Frontend**: `CreateAccount.tsx` and `Login.tsx` are the forms; `AuthContext.tsx` holds the logged-in user in React context + `localStorage`; `api.ts` wraps the fetch calls to the backend.

## Frontend ↔ FastAPI, and Agent Loading (beginner-friendly)

The frontend (React, `npm run dev`, `localhost:5174`) and backend (FastAPI, `uvicorn main:app --reload --port 8000`, run from `backend/`) are two separate programs talking over HTTP. The frontend never touches the database directly — every page/component calls a function in `frontend/src/api.ts`, which `fetch`es a backend route and gets JSON back. Example: the chat widget calls `sendChatMessage()` → `POST /api/chat` → `run_agent()` in `agent.py` → `{"reply", "tools_used"}` JSON back to the widget. Login, account creation, and product listing all follow the same pattern with different routes.

The agent itself is built once and reused (a lazy singleton, `get_agent()` in `agent.py`), not rebuilt per message. Building it means: reading the personality from `prompts/prompt.md`, connecting to the model through Portkey's gateway with an API key, and attaching its tools. The key (`PORTKEY_API_KEY`) comes from a `.env` file (`HW4/.env` or the `AI Foundations` root `.env`) via `python-dotenv`, never hard-coded — and a missing key only errors when someone actually chats, not at server startup.

## Problem 6: Agent Tools

- `search_products`
- `get_product_details`
- `get_product_stock`
- `get_user_account`
- `get_chat_history`
- `list_product_types`

Price and inventory (quantity/size) were included because they're what customers are most likely to ask about; product_id was excluded for the same reason — customers don't know to ask about it.

`get_chat_history` lets the agent use a customer's prior messages for context when problem-solving.

`get_user_account` exists so the agent demonstrably *has* access to other users' data but is instructed (in `prompt.md`) never to disclose it — for anyone, including the current user — rather than being safe only because it lacks the means to look.

`list_product_types` was added in Problem 7, so the chat-driven product search could match everyday words (e.g. "hoodies") against the catalogue's actual `garment_type` strings, which don't always line up with how a customer would phrase a request.

## Problem 7: How Search Results Reach the Page

When the agent calls `search_products`, `agent.py` pulls the actual tool return value (not the model's text) out of the run and attaches it to the API response as `products`. `POST /api/chat` returns `{"reply", "tools_used", "products"}`. The frontend's `ChatWidget` puts `products` into a shared `ChatMatchContext`; the `Products` page reads that context and reorders its existing grid — matches first (gold-highlighted), non-matches shuffled below, nothing hidden. The product cards and detail page are untouched; only their order and highlighting change.

## Problem 8: Customer Memory & Page Context

**Chat history storage**: `POST /api/chat` now takes `message`, `user_id`, and `page_html` (all defined on `ChatRequest` in `models.py`). After every reply, `agent.py`'s `_save_chat_turn()` inserts a `user` row and an `assistant` row into `chat_messages` (with `products_json` on the assistant row) — but only when `user_id` is present. A guest (`user_id` is `None`) is a no-op: nothing is ever written for a guest. On each new message, `_load_message_history()` reads that user's prior `chat_messages` rows back out of the database and reconstructs them as pydantic-ai `ModelRequest`/`ModelResponse` messages, so a returning, logged-in customer's past conversation is genuine model context again — not just a record sitting in a table.

**What customer fields the agent can see**: `UserAccount` in `models.py` (`id`, `first_name`, `last_name`, `email`, `created_at` — `password_hash` is never included, even in the model shape) is looked up once per run and turned into a short instruction telling the agent who it's chatting with. The agent may freely use *that one customer's* name/email/chat history; `prompt.md` forbids it from ever discussing anyone else's account, or discussing any password/credential for anyone, including the current user.

**How page context is passed**: `ChatWidget.tsx` grabs `document.querySelector(".page")?.outerHTML` — the current route's rendered HTML — at the moment a message is sent, and includes it as `page_html`. `agent.py`'s `_page_context_instructions()` truncates it (8,000 chars) and adds it as a per-run instruction, explicitly labeled as reference-only page content (not customer- or system-issued instructions, to guard against anything resembling prompt injection in the markup). This is what lets the agent resolve "do you have this in a different color?" on a product page — `ProductDetail.tsx` renders a `data-product-id` attribute the agent can read directly off the page.

## Problem 12: Audit Trail & Safety

**Loop limit (20)**: caps how many model/tool round trips one message can trigger (`UsageLimits(request_limit=20)` in `agent.py`), so a confused or looping agent can't run indefinitely — it fails fast and the failure shows up in `audit_trail.json` as an error entry instead of hanging the request.

**Result limit (50)**: keeps a single `search_products` call from ever returning the whole ~102-row catalogue in one response. Same instinct as the field choices discussed under Problem 6 — `models.py`'s `ProductCard`/`ProductDetails` only expose the fields (price, description, stock) customers actually ask about, and this limit keeps the *number* of results just as deliberately bounded.

**No internet-access control needed**: `tools.py`'s `TOOLS` list only contains functions that query `campus_customs.db` — there is no web-search/fetch tool defined anywhere in the codebase. There's nothing for a rule to restrict; it's structurally impossible, not merely instructed against.

**No audit-log-edit control needed**: `_append_audit()` writes to `audit_trail.json` from inside `agent.py`, after a run already completes — it is never registered as a callable tool. The agent has no code path that could write to or alter that file, so this isn't something the agent could do even if it tried.
