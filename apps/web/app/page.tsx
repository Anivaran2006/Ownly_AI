import Image from "next/image";
import Link from "next/link";
import { Camera, FileText, Shield, Tag } from "lucide-react";
import { AiSearchCard } from "@/components/dashboard/ai-search-card";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { Badge } from "@/components/ui/badge";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";
import { metrics, products, upcomingActions, workspace } from "@/lib/sample-data";

export default function DashboardPage() {
  return (
    <div>
      <section className="mb-5 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="mb-1 text-xs font-bold uppercase text-primary">{workspace.name}</p>
          <h1 className="text-3xl font-extrabold tracking-normal md:text-4xl">Ownership command center</h1>
        </div>
        <div className="flex rounded-lg border bg-card/80 p-1">
          {["Month", "Quarter", "Year"].map((range, index) => (
            <button
              key={range}
              type="button"
              className={`min-h-8 rounded-md px-3 text-sm font-semibold ${index === 0 ? "bg-muted text-foreground" : "text-muted-foreground"}`}
            >
              {range}
            </button>
          ))}
        </div>
      </section>

      <section className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <KpiCard label="Total assets" value={String(metrics.totalAssets)} helper="12 added this month" />
        <KpiCard label="Purchase value" value={formatCurrency(metrics.purchaseValue)} helper={`${formatCurrency(metrics.indexedResaleValue)} indexed resale`} />
        <KpiCard label="Protected" value="87%" helper={`${metrics.activeWarranties} active warranties`} />
        <KpiCard label="Needs action" value={String(metrics.needsAction)} helper="4 returns, 5 renewals" tone="attention" />
      </section>

      <section className="mt-3 grid gap-3 xl:grid-cols-[1.2fr_0.8fr]">
        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">AI scanner</p>
              <CardTitle>Latest extraction</CardTitle>
              <CardDescription>Multi-field capture from invoice, screenshot, PDF, or email.</CardDescription>
            </div>
            <Link
              href="/scanner"
              className="inline-flex min-h-10 items-center justify-center gap-2 rounded-lg border bg-card px-4 text-sm font-semibold transition hover:bg-muted"
            >
              <Camera className="size-4" />
              Open
            </Link>
          </CardHeader>
          <div className="grid gap-4 md:grid-cols-[190px_1fr]">
            <div className="h-56 rounded-lg border bg-muted p-5">
              <div className="mb-3 h-5 rounded-full bg-card" />
              <div className="mb-8 h-3 w-2/3 rounded-full bg-card" />
              <div className="grid grid-cols-2 gap-3">
                <span className="h-12 rounded-lg bg-card" />
                <span className="h-12 rounded-lg bg-card" />
                <span className="h-12 rounded-lg bg-card" />
                <span className="h-12 rounded-lg bg-card" />
              </div>
            </div>
            <dl className="grid gap-2 sm:grid-cols-2">
              {[
                ["Product", "Galaxy Book4 Pro"],
                ["Seller", "Amazon India"],
                ["Warranty", "Ends 18 Mar 2027"],
                ["Confidence", "94%"],
                ["GST", "INR 22,727"],
                ["Payment", "HDFC credit card"]
              ].map(([label, value]) => (
                <div key={label} className="rounded-lg border bg-muted/60 p-3">
                  <dt className="text-xs font-bold text-muted-foreground">{label}</dt>
                  <dd className="mt-1 font-bold">{value}</dd>
                </div>
              ))}
            </dl>
          </div>
        </Card>

        <Card>
          <div className="overflow-hidden rounded-lg border bg-muted">
            <Image
              src="/assets/ownly-product-collection.png"
              alt="Owned electronics and appliance collection"
              width={1536}
              height={864}
              className="aspect-video object-cover"
              priority
            />
          </div>
          <div className="mt-4">
            <p className="mb-1 text-xs font-bold uppercase text-primary">AI insight</p>
            <h2 className="text-lg font-bold">4 high-value items need updated photos</h2>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              Better photos can raise resale confidence for your laptop, watch, camera lens, and headphones.
            </p>
          </div>
        </Card>
      </section>

      <section id="analytics" className="mt-3 grid gap-3 xl:grid-cols-3">
        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Analytics</p>
              <CardTitle>Category breakdown</CardTitle>
            </div>
          </CardHeader>
          <div className="grid items-center gap-5 sm:grid-cols-[170px_1fr]">
            <div className="aspect-square rounded-full border" style={{ background: "radial-gradient(circle, hsl(var(--card)) 0 48%, transparent 49%), conic-gradient(hsl(var(--primary)) 0 48%, hsl(var(--accent)) 48% 72%, hsl(var(--warning)) 72% 88%, hsl(var(--risk)) 88% 100%)" }} />
            <ul className="grid gap-3 text-sm">
              {["Electronics 48%", "Appliances 24%", "Furniture 16%", "Personal 12%"].map((item) => (
                <li key={item} className="flex justify-between border-b pb-2 text-muted-foreground last:border-b-0">
                  <span>{item.split(" ")[0]}</span>
                  <strong className="text-foreground">{item.split(" ")[1]}</strong>
                </li>
              ))}
            </ul>
          </div>
        </Card>

        <Card id="warranties">
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Warranty radar</p>
              <CardTitle>Upcoming actions</CardTitle>
            </div>
          </CardHeader>
          <div className="grid gap-2">
            {upcomingActions.map((item) => (
              <div key={item.label} className="flex items-center justify-between gap-3 rounded-lg border p-3">
                <div>
                  <strong className="block text-sm">{item.label}</strong>
                  <span className="text-xs text-muted-foreground">{item.date}</span>
                </div>
                <Badge tone={item.severity === "ok" ? "ok" : item.severity}>{item.severity}</Badge>
              </div>
            ))}
          </div>
        </Card>

        <AiSearchCard />
      </section>

      <section id="resale" className="mt-3 grid gap-3 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Product profiles</p>
              <CardTitle>Living asset identities</CardTitle>
            </div>
            <Link
              href="/products"
              className="inline-flex min-h-10 items-center justify-center rounded-lg border bg-card px-4 text-sm font-semibold transition hover:bg-muted"
            >
              View all
            </Link>
          </CardHeader>
          <div className="grid gap-2">
            {products.slice(0, 3).map((product) => (
              <div key={product.id} className="grid grid-cols-[2.5rem_1fr_auto] items-center gap-3 rounded-lg border p-3">
                <span className="grid size-10 place-items-center rounded-lg bg-primary/15 text-primary">
                  <FileText className="size-4" />
                </span>
                <div className="min-w-0">
                  <strong className="block truncate text-sm">{product.name}</strong>
                  <span className="block truncate text-xs text-muted-foreground">{product.sellerName}</span>
                </div>
                <span className="text-sm font-bold">{formatCurrency(product.purchasePrice ?? 0)}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Smart resale</p>
              <CardTitle>Marketplace draft ready</CardTitle>
              <CardDescription>Estimate value using age, condition, warranty left, accessories, and market signals.</CardDescription>
            </div>
            <Tag className="size-5 text-primary" />
          </CardHeader>
          <div className="rounded-lg bg-primary/10 p-5">
            <strong className="block text-3xl">{formatCurrency(74000)}</strong>
            <span className="mt-2 block text-sm text-muted-foreground">Suggested list price for MacBook Pro 14</span>
          </div>
          <p className="mt-4 rounded-lg border bg-muted p-4 text-sm leading-6">
            MacBook Pro 14 with invoice, warranty, and original accessories. Excellent condition, verified purchase invoice, and complete accessory set.
          </p>
        </Card>
      </section>

      <section id="family" className="mt-3">
        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Family workspace</p>
              <CardTitle>Shared household inventory</CardTitle>
              <CardDescription>Role-based access for owners, admins, members, viewers, and limited profiles.</CardDescription>
            </div>
            <Shield className="size-5 text-primary" />
          </CardHeader>
          <div className="grid gap-3 md:grid-cols-3">
            {["Aarav - Owner", "Nisha - Admin", "Ira - Viewer"].map((member) => (
              <div key={member} className="rounded-lg border bg-muted p-4 text-sm font-semibold">{member}</div>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}
