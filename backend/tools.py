"""Tools available to the Campus Customs agent.

Every one of these reads directly from campus_customs.db — the agent must
never answer a price, description, or stock question from memory.
"""

from __future__ import annotations

from db import get_connection, release_connection
from models import ChatMessageRecord, ProductCard, ProductDetails, SizeStock, UserAccount


def list_product_types() -> list[str]:
    """List every distinct garment_type value used in the catalogue.

    Not an agent tool — called once at agent build time so the category
    list can be baked into the static instructions instead of costing a
    model round trip on every product question.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT DISTINCT garment_type FROM catalogue ORDER BY garment_type"
        ).fetchall()
        return [row["garment_type"] for row in rows]
    finally:
        release_connection(conn)


def search_products(query: str) -> list[ProductCard]:
    """Search the product catalogue by name, garment type, or tag keywords.

    Call this to find matching products, whether the customer named a
    specific item or asked about a category (e.g. "what hoodies do you
    have?"). Returns up to 50 matches ordered by name, shaped as product
    cards (image, name, price, short description) for display on the site.
    """
    conn = get_connection()
    try:
        needle = f"%{query.lower()}%"
        rows = conn.execute(
            """
            SELECT product_id, name, garment_type, price, image_file_path, description
            FROM catalogue
            WHERE lower(name) LIKE ?
               OR lower(garment_type) LIKE ?
               OR lower(search_tags) LIKE ?
            ORDER BY name
            LIMIT 50
            """,
            (needle, needle, needle),
        ).fetchall()
        return [
            ProductCard(
                product_id=row["product_id"],
                name=row["name"],
                garment_type=row["garment_type"],
                price=row["price"],
                image_file_path=row["image_file_path"],
                short_description=row["description"],
            )
            for row in rows
        ]
    finally:
        release_connection(conn)


def get_product_details(product_id: str) -> ProductDetails | str:
    """Look up a product's description and price by product_id.

    Always call this instead of guessing or recalling a price or
    description — prices and descriptions must come from the database.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM catalogue WHERE product_id = ?", (product_id,)
        ).fetchone()
        if row is None:
            return f"No product found with product_id '{product_id}'."
        return ProductDetails(
            product_id=row["product_id"],
            name=row["name"],
            garment_type=row["garment_type"],
            description=row["description"],
            price=row["price"],
        )
    finally:
        release_connection(conn)


def get_product_stock(product_id: str, size: str | None = None) -> list[SizeStock] | str:
    """Look up live inventory quantity for a product, by size.

    Always call this instead of guessing whether a size is in stock. Pass a
    size (e.g. "M", "XL") to check just that size, or omit it to list every
    size. A quantity of 0 means that size is out of stock — report that
    plainly rather than suggesting it might be available.
    """
    conn = get_connection()
    try:
        exists = conn.execute(
            "SELECT 1 FROM catalogue WHERE product_id = ?", (product_id,)
        ).fetchone()
        if exists is None:
            return f"No product found with product_id '{product_id}'."

        if size:
            rows = conn.execute(
                "SELECT size, quantity FROM inventory WHERE product_id = ? AND size = ?",
                (product_id, size),
            ).fetchall()
            if not rows:
                return f"No size '{size}' found for product_id '{product_id}'."
        else:
            rows = conn.execute(
                "SELECT size, quantity FROM inventory WHERE product_id = ? ORDER BY id",
                (product_id,),
            ).fetchall()

        return [SizeStock(size=row["size"], quantity=row["quantity"]) for row in rows]
    finally:
        release_connection(conn)


def get_user_account(user_id: int) -> UserAccount | str:
    """Look up a row of the users table by id.

    This exists for completeness of database access, but the agent must
    never share anything this returns with anyone, for any account,
    including the account of the person currently chatting. See prompt.md.
    """
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT id, first_name, last_name, email, created_at FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        if row is None:
            return f"No user found with id {user_id}."
        return UserAccount(
            id=row["id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            created_at=row["created_at"],
        )
    finally:
        release_connection(conn)


def get_chat_history(user_id: int, limit: int = 20) -> list[ChatMessageRecord] | str:
    """Look up a user's past chat_messages rows, most recent last.

    This exists for completeness of database access, but the agent must
    never share anything this returns with anyone, for any account,
    including the account of the person currently chatting. See prompt.md.
    """
    conn = get_connection()
    try:
        rows = conn.execute(
            """
            SELECT id, user_id, role, content, created_at
            FROM chat_messages
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        if not rows:
            return f"No chat history found for user id {user_id}."
        return [
            ChatMessageRecord(
                id=row["id"],
                user_id=row["user_id"],
                role=row["role"],
                content=row["content"],
                created_at=row["created_at"],
            )
            for row in reversed(rows)
        ]
    finally:
        release_connection(conn)


TOOLS = [
    search_products,
    get_product_details,
    get_product_stock,
    get_user_account,
    get_chat_history,
]
