def m001_initial(db):
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS withdraw_links (
            id TEXT PRIMARY KEY,
            wallet TEXT,
            title TEXT,
            key TEXT,
            amount INTEGER DEFAULT 1,
            used INTEGER DEFAULT 0,
        );
    """
    )

