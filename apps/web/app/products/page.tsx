import Image from "next/image";
import { FileText, Shield, Tag } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { products } from "@/lib/sample-data";
import { formatCurrency } from "@/lib/utils";

export default function ProductsPage() {
  const selected = products[0];

  return (
    <div>
      <section className="mb-5 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="mb-1 text-xs font-bold uppercase text-primary">Inventory</p>
          <h1 className="text-3xl font-extrabold tracking-normal md:text-4xl">Product profiles</h1>
        </div>
        <Button>Add asset</Button>
      </section>

      <section className="grid gap-3 xl:grid-cols-[0.9fr_1.1fr]">
        <Card>
          <div className="mb-4 flex flex-wrap gap-2">
            {["All", "Electronics", "Appliances", "Returns"].map((label, index) => (
              <button
                key={label}
                type="button"
                className={`min-h-8 rounded-lg border px-3 text-xs font-bold ${index === 0 ? "bg-muted text-foreground" : "text-muted-foreground"}`}
              >
                {label}
              </button>
            ))}
          </div>
          <div className="grid gap-2">
            {products.map((product) => (
              <div key={product.id} className="grid grid-cols-[2.75rem_1fr_auto] items-center gap-3 rounded-lg border p-3">
                <span className="grid size-11 place-items-center rounded-lg bg-primary/15 text-primary">
                  <FileText className="size-4" />
                </span>
                <div className="min-w-0">
                  <strong className="block truncate text-sm">{product.name}</strong>
                  <span className="block truncate text-xs text-muted-foreground">
                    {product.brand} {product.model} - {product.sellerName}
                  </span>
                </div>
                <span className="text-sm font-bold">{formatCurrency(product.purchasePrice ?? 0)}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <div className="grid gap-5 md:grid-cols-[180px_1fr]">
            <div className="overflow-hidden rounded-lg border bg-muted">
              <Image
                src="/assets/ownly-product-collection.png"
                alt={selected.name}
                width={600}
                height={600}
                className="aspect-square object-cover"
              />
            </div>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">{selected.category}</p>
              <h2 className="text-2xl font-extrabold">{selected.name}</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                {selected.brand} {selected.model}
              </p>
              <div className="mt-4 flex flex-wrap gap-2">
                <Badge tone="ok">
                  <Shield className="mr-1 size-3" />
                  Protected
                </Badge>
                <Badge tone="info">
                  <Tag className="mr-1 size-3" />
                  {formatCurrency(selected.estimatedResaleValue ?? 0)}
                </Badge>
              </div>
            </div>
          </div>

          <dl className="mt-5 grid gap-2 sm:grid-cols-2">
            {[
              ["Purchase date", selected.purchaseDate ?? "Unknown"],
              ["Purchase price", formatCurrency(selected.purchasePrice ?? 0)],
              ["Seller", selected.sellerName ?? "Unknown"],
              ["Warranty ends", selected.warrantyEndDate ?? "Unknown"],
              ["Return window", selected.returnDeadline ?? "Closed"],
              ["Estimated resale", formatCurrency(selected.estimatedResaleValue ?? 0)]
            ].map(([label, value]) => (
              <div key={label} className="rounded-lg border bg-muted/70 p-3">
                <dt className="text-xs font-bold text-muted-foreground">{label}</dt>
                <dd className="mt-1 font-bold">{value}</dd>
              </div>
            ))}
          </dl>

          <CardHeader className="mt-5 px-0">
            <div>
              <CardTitle>AI insights</CardTitle>
              <CardDescription>{selected.aiSummary}</CardDescription>
            </div>
          </CardHeader>
          <div className="flex flex-wrap gap-2">
            {["Invoice", "Warranty", "Manual", "Photos", "Service history"].map((doc) => (
              <span key={doc} className="inline-flex min-h-8 items-center gap-2 rounded-lg border bg-muted px-3 text-xs font-bold">
                <FileText className="size-3" />
                {doc}
              </span>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}

