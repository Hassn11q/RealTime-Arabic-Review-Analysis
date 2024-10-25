CREATE TABLE IF NOT EXISTS arabic_reviews (
    id SERIAL PRIMARY KEY,
    review TEXT,
    sentiment TEXT,
    score FLOAT
);
