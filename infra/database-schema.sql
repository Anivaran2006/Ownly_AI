-- Ownly PostgreSQL schema starter
-- Target: PostgreSQL 16+ with pgvector and pgcrypto extensions.

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS citext;

CREATE TYPE workspace_role AS ENUM ('owner', 'admin', 'member', 'viewer', 'limited');
CREATE TYPE document_kind AS ENUM ('invoice', 'warranty', 'manual', 'receipt', 'photo', 'service_record', 'insurance', 'other');
CREATE TYPE document_status AS ENUM ('uploaded', 'processing', 'processed', 'failed', 'archived');
CREATE TYPE product_status AS ENUM ('active', 'returned', 'sold', 'lost', 'disposed', 'archived');
CREATE TYPE reminder_kind AS ENUM ('warranty_expiry', 'return_deadline', 'replacement_deadline', 'amc_renewal', 'insurance_renewal', 'service_due', 'custom');
CREATE TYPE reminder_status AS ENUM ('scheduled', 'sent', 'dismissed', 'failed', 'cancelled');
CREATE TYPE extraction_status AS ENUM ('queued', 'running', 'needs_review', 'completed', 'failed');
CREATE TYPE timeline_event_kind AS ENUM ('purchased', 'delivered', 'return_deadline', 'warranty_started', 'repair', 'service', 'battery_changed', 'insurance_added', 'amc_added', 'sold', 'transferred', 'note');

CREATE TABLE users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email citext UNIQUE NOT NULL,
    full_name text,
    avatar_url text,
    locale text NOT NULL DEFAULT 'en-IN',
    default_currency char(3) NOT NULL DEFAULT 'INR',
    password_hash text,
    google_sub text UNIQUE,
    mfa_enabled boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE workspaces (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL,
    slug text,
    home_country char(2) NOT NULL DEFAULT 'IN',
    default_currency char(3) NOT NULL DEFAULT 'INR',
    plan text NOT NULL DEFAULT 'free',
    private_ai_mode boolean NOT NULL DEFAULT false,
    created_by uuid REFERENCES users(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE workspace_members (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id uuid NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role workspace_role NOT NULL DEFAULT 'member',
    display_name text,
    invited_by uuid REFERENCES users(id),
    joined_at timestamptz NOT NULL DEFAULT now(),
    revoked_at timestamptz,
    UNIQUE (workspace_id, user_id)
);

CREATE TABLE encryption_keys (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    key_version integer NOT NULL,
    provider text NOT NULL DEFAULT 'kms',
    key_ref text NOT NULL,
    purpose text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    retired_at timestamptz,
    UNIQUE (workspace_id, key_version, purpose)
);

CREATE TABLE products (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    created_by uuid REFERENCES users(id),
    primary_document_id uuid,
    name text NOT NULL,
    brand text,
    model text,
    category text,
    subcategory text,
    status product_status NOT NULL DEFAULT 'active',
    condition_grade text NOT NULL DEFAULT 'good',
    purchase_date date,
    purchase_price numeric(14,2),
    purchase_currency char(3) NOT NULL DEFAULT 'INR',
    tax_amount numeric(14,2),
    tax_label text DEFAULT 'GST',
    seller_name text,
    seller_domain text,
    payment_method text,
    order_id text,
    invoice_number text,
    estimated_resale_value numeric(14,2),
    resale_currency char(3),
    image_object_key text,
    ai_summary text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE INDEX idx_products_workspace ON products(workspace_id, status, purchase_date DESC);
CREATE INDEX idx_products_category ON products(workspace_id, category);
CREATE INDEX idx_products_seller ON products(workspace_id, seller_name);
CREATE INDEX idx_products_price ON products(workspace_id, purchase_price);

CREATE TABLE product_identifiers (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    kind text NOT NULL,
    value_encrypted bytea NOT NULL,
    value_hash text NOT NULL,
    confidence numeric(4,3),
    source_document_id uuid,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, kind, value_hash)
);

CREATE TABLE documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    uploaded_by uuid REFERENCES users(id),
    kind document_kind NOT NULL DEFAULT 'other',
    status document_status NOT NULL DEFAULT 'uploaded',
    original_filename text NOT NULL,
    mime_type text NOT NULL,
    byte_size bigint NOT NULL,
    checksum_sha256 text NOT NULL,
    object_key text NOT NULL,
    encrypted_dek bytea,
    key_version integer,
    source_channel text NOT NULL DEFAULT 'upload',
    source_uri text,
    language_hint text,
    page_count integer,
    ocr_text text,
    ocr_layout jsonb,
    error_message text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE INDEX idx_documents_workspace_kind ON documents(workspace_id, kind, created_at DESC);
CREATE INDEX idx_documents_checksum ON documents(workspace_id, checksum_sha256);

ALTER TABLE products
    ADD CONSTRAINT fk_products_primary_document
    FOREIGN KEY (primary_document_id) REFERENCES documents(id);

CREATE TABLE document_pages (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    page_number integer NOT NULL,
    text text,
    layout jsonb,
    preview_object_key text,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (document_id, page_number)
);

CREATE TABLE product_documents (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    relationship document_kind NOT NULL,
    is_primary boolean NOT NULL DEFAULT false,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (product_id, document_id, relationship)
);

CREATE TABLE extraction_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    status extraction_status NOT NULL DEFAULT 'queued',
    ocr_provider text,
    model_provider text,
    model_name text,
    prompt_version text,
    schema_version text NOT NULL DEFAULT 'ownership-extraction-v1',
    raw_output jsonb,
    normalized_output jsonb,
    average_confidence numeric(4,3),
    started_at timestamptz,
    completed_at timestamptz,
    error_message text,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_extraction_runs_document ON extraction_runs(document_id, created_at DESC);

CREATE TABLE extracted_fields (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    extraction_run_id uuid NOT NULL REFERENCES extraction_runs(id) ON DELETE CASCADE,
    document_id uuid NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    product_id uuid REFERENCES products(id) ON DELETE SET NULL,
    field_name text NOT NULL,
    field_value jsonb NOT NULL,
    normalized_value text,
    confidence numeric(4,3) NOT NULL,
    evidence jsonb NOT NULL DEFAULT '{}'::jsonb,
    accepted_by uuid REFERENCES users(id),
    accepted_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_extracted_fields_lookup ON extracted_fields(workspace_id, field_name, normalized_value);

CREATE TABLE warranties (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    kind text NOT NULL DEFAULT 'manufacturer',
    provider_name text,
    policy_number_encrypted bytea,
    start_date date,
    end_date date NOT NULL,
    duration_months integer,
    source_document_id uuid REFERENCES documents(id),
    confidence numeric(4,3),
    is_extended boolean NOT NULL DEFAULT false,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_warranties_expiry ON warranties(workspace_id, end_date);

CREATE TABLE return_windows (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    seller_name text,
    return_deadline date,
    replacement_deadline date,
    policy_source text,
    confidence numeric(4,3),
    status text NOT NULL DEFAULT 'open',
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_return_windows_deadlines ON return_windows(workspace_id, return_deadline, replacement_deadline);

CREATE TABLE timeline_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    actor_user_id uuid REFERENCES users(id),
    kind timeline_event_kind NOT NULL,
    title text NOT NULL,
    description text,
    event_date date NOT NULL,
    amount numeric(14,2),
    currency char(3),
    provider_name text,
    document_id uuid REFERENCES documents(id),
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_timeline_events_product_date ON timeline_events(product_id, event_date DESC);

CREATE TABLE service_records (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    service_date date NOT NULL,
    provider_name text,
    issue text,
    resolution text,
    cost numeric(14,2),
    currency char(3) DEFAULT 'INR',
    document_id uuid REFERENCES documents(id),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE accessories (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    name text NOT NULL,
    brand text,
    model text,
    purchase_price numeric(14,2),
    currency char(3) DEFAULT 'INR',
    document_id uuid REFERENCES documents(id),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE product_photos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    uploaded_by uuid REFERENCES users(id),
    object_key text NOT NULL,
    encrypted_dek bytea,
    caption text,
    captured_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE notes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    author_user_id uuid REFERENCES users(id),
    body_encrypted bytea,
    body_preview text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    deleted_at timestamptz
);

CREATE TABLE resale_estimates (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    estimate_value numeric(14,2) NOT NULL,
    currency char(3) NOT NULL DEFAULT 'INR',
    low_value numeric(14,2),
    high_value numeric(14,2),
    confidence numeric(4,3),
    method text NOT NULL,
    listing_title text,
    listing_body text,
    market_signals jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_resale_estimates_latest ON resale_estimates(product_id, created_at DESC);

CREATE TABLE reminders (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    product_id uuid REFERENCES products(id) ON DELETE CASCADE,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    kind reminder_kind NOT NULL,
    status reminder_status NOT NULL DEFAULT 'scheduled',
    title text NOT NULL,
    due_at timestamptz NOT NULL,
    send_at timestamptz NOT NULL,
    channel text NOT NULL DEFAULT 'email',
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    sent_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_reminders_due ON reminders(status, send_at);
CREATE INDEX idx_reminders_workspace ON reminders(workspace_id, due_at);

CREATE TABLE search_embeddings (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    entity_type text NOT NULL,
    entity_id uuid NOT NULL,
    chunk_kind text NOT NULL,
    chunk_text text NOT NULL,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    embedding vector(1536) NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_search_embeddings_entity ON search_embeddings(workspace_id, entity_type, entity_id);
CREATE INDEX idx_search_embeddings_vector ON search_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

CREATE TABLE integrations (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    provider text NOT NULL,
    status text NOT NULL DEFAULT 'connected',
    scopes text[] NOT NULL DEFAULT ARRAY[]::text[],
    external_account_hash text,
    access_token_encrypted bytea,
    refresh_token_encrypted bytea,
    last_sync_at timestamptz,
    cursor_encrypted bytea,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE (workspace_id, provider, external_account_hash)
);

CREATE TABLE notifications (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    reminder_id uuid REFERENCES reminders(id) ON DELETE SET NULL,
    channel text NOT NULL,
    destination_hash text,
    subject text,
    body text,
    status text NOT NULL DEFAULT 'queued',
    provider_message_id text,
    error_message text,
    sent_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE audit_logs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_id uuid REFERENCES workspaces(id) ON DELETE CASCADE,
    actor_user_id uuid REFERENCES users(id) ON DELETE SET NULL,
    action text NOT NULL,
    entity_type text,
    entity_id uuid,
    ip_hash text,
    user_agent_hash text,
    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_audit_logs_workspace_time ON audit_logs(workspace_id, created_at DESC);
CREATE INDEX idx_audit_logs_entity ON audit_logs(workspace_id, entity_type, entity_id);

-- Suggested row-level security activation.
-- Application connections should set app.current_workspace_id and app.current_user_id.

ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE warranties ENABLE ROW LEVEL SECURITY;
ALTER TABLE reminders ENABLE ROW LEVEL SECURITY;
ALTER TABLE search_embeddings ENABLE ROW LEVEL SECURITY;

CREATE POLICY products_workspace_isolation ON products
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));

CREATE POLICY documents_workspace_isolation ON documents
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));

CREATE POLICY product_documents_workspace_isolation ON product_documents
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));

CREATE POLICY warranties_workspace_isolation ON warranties
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));

CREATE POLICY reminders_workspace_isolation ON reminders
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));

CREATE POLICY search_embeddings_workspace_isolation ON search_embeddings
    USING (workspace_id::text = current_setting('app.current_workspace_id', true));
