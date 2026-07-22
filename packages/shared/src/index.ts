export type WorkspaceRole = "owner" | "admin" | "member" | "viewer" | "limited";

export type ProductStatus = "active" | "returned" | "sold" | "lost" | "disposed" | "archived";

export type DocumentKind =
  | "invoice"
  | "warranty"
  | "manual"
  | "receipt"
  | "photo"
  | "service_record"
  | "insurance"
  | "other";

export type ReminderKind =
  | "warranty_expiry"
  | "return_deadline"
  | "replacement_deadline"
  | "amc_renewal"
  | "insurance_renewal"
  | "service_due"
  | "custom";

export interface Workspace {
  id: string;
  name: string;
  role: WorkspaceRole;
  plan: string;
  defaultCurrency: string;
}

export interface Product {
  id: string;
  workspaceId: string;
  name: string;
  brand?: string;
  model?: string;
  category?: string;
  status: ProductStatus;
  purchaseDate?: string;
  purchasePrice?: number;
  purchaseCurrency: string;
  sellerName?: string;
  warrantyEndDate?: string;
  returnDeadline?: string;
  estimatedResaleValue?: number;
  aiSummary?: string;
}

export interface UploadSession {
  uploadId: string;
  documentId: string;
  uploadUrl: string;
  headers: Record<string, string>;
  expiresAt: string;
}

export interface ExtractionField {
  fieldName: string;
  value: string | number | boolean | null;
  confidence: number;
  evidence?: string;
}

export interface ProductCandidate {
  name: string;
  confidence: number;
  fields: ExtractionField[];
}

export interface Scan {
  id: string;
  workspaceId: string;
  documentId: string;
  status: "queued" | "running" | "needs_review" | "completed" | "failed";
  averageConfidence?: number;
  productCandidates: ProductCandidate[];
}

export interface SearchResult {
  type: "product" | "document" | "timeline_event" | "reminder";
  id: string;
  title: string;
  snippet: string;
  score: number;
  citations: Array<Record<string, unknown>>;
}

export interface SearchResponse {
  query: string;
  interpretedIntent?: string;
  results: SearchResult[];
}

