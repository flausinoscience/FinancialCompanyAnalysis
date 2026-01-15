CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS "Country" (
	code CHAR(2) PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Currency" (
	id SMALLINT PRIMARY KEY,
	name CHAR(3) UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Risk_Profile" (
	id SMALLINT PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Customer" (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	email VARCHAR(255) UNIQUE NOT NULL,
	first_name VARCHAR(255) NOT NULL,
	surname VARCHAR(255) NOT NULL,
	sign_up_at TIMESTAMP NOT NULL,
	country_code CHAR(2) REFERENCES public."Country"(code) NOT NULL,
	birth_date DATE NOT NULL,
	risk_profile SMALLINT REFERENCES public."Risk_Profile"(id) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Brokerage" (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	name VARCHAR(255) NOT NULL,
	country_code CHAR(2) REFERENCES public."Country"(code) NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Account_Status" (
	id SMALLINT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Account_Type" (
	id SMALLINT PRIMARY KEY,
	name VARCHAR(255) NOT NULL UNIQUE,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Account" (
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	customer_id UUID REFERENCES public."Customer"(id) ON DELETE CASCADE NOT NULL,
	brokerage_id UUID REFERENCES public."Brokerage"(id),
	type_id SMALLINT REFERENCES public."Account_Type"(id) NOT NULL,
	currency_id SMALLINT REFERENCES public."Currency"(id) NOT NULL DEFAULT 1,
	balance NUMERIC(18, 4) NOT NULL DEFAULT 0 CHECK(balance >= 0),
	opened_at TIMESTAMP NOT NULL,
	status_id SMALLINT REFERENCES public."Account_Status"(id) NOT NULL DEFAULT 1,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Asset_Type" (
	id SMALLINT PRIMARY KEY,
	name TEXT UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Asset" (
-- Catalog of assets people can trade.
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	ticker TEXT UNIQUE NOT NULL,
	name TEXT NOT NULL,
	type_id SMALLINT REFERENCES public."Asset_Type"(id) NOT NULL,
	currency_id SMALLINT REFERENCES public."Currency"(id) NOT NULL DEFAULT 1,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Market_Price" (
-- This is price history over time. One asset can have many price records over time.
	id BIGSERIAL PRIMARY KEY,
	asset_id UUID REFERENCES public."Asset"(id) NOT NULL,
	price_at TIMESTAMP NOT NULL,
	price NUMERIC(18, 6) NOT NULL CHECK (price >= 0),
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP,

	UNIQUE(asset_id, price_at)
);

CREATE TABLE IF NOT EXISTS "Trade_Type" (
	id SMALLINT PRIMARY KEY,
	name VARCHAR(255) UNIQUE NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Trade" (
-- This table logs each transaction executed by accounts — what they bought or sold.
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	asset_id UUID REFERENCES public."Asset"(id) NOT NULL,
	account_id UUID REFERENCES public."Account"(id) NOT NULL ,
	type_id SMALLINT REFERENCES public."Trade_Type"(id) NOT NULL,
	quantity NUMERIC(18,6) CHECK (quantity > 0), 
	price NUMERIC(18,6) CHECK (price >= 0), 
	traded_at TIMESTAMP NOT NULL, 
	commission NUMERIC(18,6) DEFAULT 0 CHECK (commission >= 0), 
	is_flagged BOOLEAN NOT NULL DEFAULT FALSE, 
	reason_flag TEXT,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Position" (
-- This table shows what an account currently owns.
	id UUID PRIMARY KEY DEFAULT gen_random_uuid(), 
	account_id UUID REFERENCES public."Account"(id) NOT NULL, 
	asset_id UUID REFERENCES public."Asset"(id) NOT NULL, 
	quantity NUMERIC(18,6) DEFAULT 0, 
	avg_price NUMERIC(18,6) DEFAULT 0, 
	created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
	deleted_at TIMESTAMP, 
	
	UNIQUE(account_id, asset_id)
);


