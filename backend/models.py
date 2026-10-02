from __future__ import annotations

from pydantic import BaseModel, Field


class SizeStock(BaseModel):
    """Stock quantity for one size of a product."""

    size: str
    quantity: int


class Product(BaseModel):
    """One row of the catalogue, with its sizes/stock attached."""

    product_id: str
    name: str
    garment_type: str
    description: str
    colors: list[str]
    search_tags: list[str]
    image_file_path: str
    price: float
    sizes: list[SizeStock] = Field(default_factory=list)


class ProductCard(BaseModel):
    """A catalogue match, returned by the product search tool.

    Shaped for the frontend to render directly as a product card: image,
    name, price, and a short description.
    """

    product_id: str
    name: str
    garment_type: str
    price: float
    image_file_path: str
    short_description: str


class ProductDetails(BaseModel):
    """Description and price for one product, returned by the product lookup tool."""

    product_id: str
    name: str
    garment_type: str
    description: str
    price: float


class UserAccount(BaseModel):
    """A row of the users table, returned by the account lookup tool.

    password_hash is deliberately never included here — the agent may know
    who it's chatting with, but no credential, for any account, should ever
    reach it.
    """

    id: int
    first_name: str | None
    last_name: str | None
    email: str
    created_at: str


class ChatMessageRecord(BaseModel):
    """A row of the chat_messages table, returned by the chat history tool."""

    id: int
    user_id: int
    role: str
    content: str
    created_at: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    user_id: int | None = None
    page_html: str | None = None


class ChatResponse(BaseModel):
    reply: str
    tools_used: list[str] = Field(default_factory=list)
    products: list[ProductCard] = Field(default_factory=list)


class AgentResult(BaseModel):
    """What run_agent returns; main.py reads reply, tools_used, and products."""

    reply: str
    tools_used: list[str] = Field(default_factory=list)
    products: list[ProductCard] = Field(default_factory=list)


class ToolCallAudit(BaseModel):
    """One tool invocation within an agent run, for the audit trail."""

    name: str
    args: str
    result: str


class AuditEntry(BaseModel):
    """One full agent loop (one chat turn), appended to output/audit_trail.json."""

    time: str
    tool_calls: list[ToolCallAudit] = Field(default_factory=list)
    stop_reason: str
