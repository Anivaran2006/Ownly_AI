import type { Product } from "@ownly/shared";

export const workspace = {
  id: "workspace-mehta-family",
  name: "Mehta Family",
  role: "owner" as const,
  plan: "family",
  defaultCurrency: "INR"
};

export const products: Product[] = [
  {
    id: "prod-macbook",
    workspaceId: workspace.id,
    name: "MacBook Pro 14",
    brand: "Apple",
    model: "M3 Pro",
    category: "Electronics",
    status: "active",
    purchaseDate: "2026-01-12",
    purchasePrice: 182900,
    purchaseCurrency: "INR",
    sellerName: "Apple Store",
    warrantyEndDate: "2027-01-11",
    estimatedResaleValue: 74000,
    aiSummary: "Protected item with complete invoice, manual, warranty, and accessory set."
  },
  {
    id: "prod-tv",
    workspaceId: workspace.id,
    name: "Samsung Frame TV 55",
    brand: "Samsung",
    model: "LS03D",
    category: "Electronics",
    status: "active",
    purchaseDate: "2025-11-02",
    purchasePrice: 94990,
    purchaseCurrency: "INR",
    sellerName: "Croma",
    warrantyEndDate: "2026-11-01",
    estimatedResaleValue: 51000,
    aiSummary: "Invoice, installation note, and manual are linked."
  },
  {
    id: "prod-purifier",
    workspaceId: workspace.id,
    name: "Dyson Air Purifier",
    brand: "Dyson",
    model: "TP10",
    category: "Appliances",
    status: "active",
    purchaseDate: "2026-07-13",
    purchasePrice: 39900,
    purchaseCurrency: "INR",
    sellerName: "Croma",
    warrantyEndDate: "2028-07-12",
    returnDeadline: "2026-07-29",
    estimatedResaleValue: 29500,
    aiSummary: "Return window is still active and a filter reminder is scheduled."
  },
  {
    id: "prod-lens",
    workspaceId: workspace.id,
    name: "Sony Camera Lens",
    brand: "Sony",
    model: "FE 24-70 GM",
    category: "Photography",
    status: "active",
    purchaseDate: "2024-08-30",
    purchasePrice: 164990,
    purchaseCurrency: "INR",
    sellerName: "Amazon India",
    warrantyEndDate: "2026-08-13",
    estimatedResaleValue: 108000,
    aiSummary: "Warranty expires soon. Service history is clean."
  }
];

export const upcomingActions = [
  { label: "Air purifier return window", date: "2026-07-29", severity: "warning" },
  { label: "Camera lens warranty", date: "2026-08-13", severity: "ok" },
  { label: "Router AMC renewal", date: "2026-08-19", severity: "risk" }
] as const;

export const metrics = {
  totalAssets: 134,
  purchaseValue: 3240000,
  activeWarranties: 63,
  needsAction: 9,
  indexedResaleValue: 1870000
};

