import { Camera, CheckCircle2, FileText, Sparkles } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const fields = [
  ["Product", "Galaxy Book4 Pro 14"],
  ["Brand", "Samsung"],
  ["Model", "NP940XGK"],
  ["Serial number", "Needs confirmation"],
  ["Purchase date", "18 Mar 2026"],
  ["Price", "INR 148,990"],
  ["GST", "INR 22,727"],
  ["Seller", "Amazon India"],
  ["Warranty", "12 months"],
  ["Return window", "7 days"],
  ["Payment", "HDFC credit card"]
];

export default function ScannerPage() {
  return (
    <div>
      <section className="mb-5 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="mb-1 text-xs font-bold uppercase text-primary">Capture</p>
          <h1 className="text-3xl font-extrabold tracking-normal md:text-4xl">AI receipt scanner</h1>
        </div>
        <Button>
          <Sparkles className="size-4" />
          Run scan
        </Button>
      </section>

      <section className="grid gap-3 xl:grid-cols-[1fr_0.9fr]">
        <Card className="grid min-h-[28rem] place-items-center border-dashed text-center">
          <div className="max-w-md">
            <span className="mx-auto grid size-16 place-items-center rounded-lg bg-primary/15 text-primary">
              <Camera className="size-7" />
            </span>
            <h2 className="mt-5 text-xl font-bold">Drop invoices, PDFs, screenshots, or email files</h2>
            <p className="mt-2 text-sm leading-6 text-muted-foreground">
              Ownly creates upload sessions, stores encrypted objects, runs OCR, and returns product candidates for confirmation.
            </p>
            <div className="mt-5 flex justify-center gap-2">
              <Button variant="secondary">
                <FileText className="size-4" />
                Choose files
              </Button>
              <Button>Start upload</Button>
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader>
            <div>
              <p className="mb-1 text-xs font-bold uppercase text-primary">Extraction</p>
              <CardTitle>Product candidate</CardTitle>
              <CardDescription>Field-level confidence is preserved for review and audit.</CardDescription>
            </div>
            <Badge tone="ok">94%</Badge>
          </CardHeader>
          <div className="mb-5 h-2 overflow-hidden rounded-full bg-muted">
            <span className="block h-full w-[94%] rounded-full bg-gradient-to-r from-primary to-accent" />
          </div>
          <dl className="grid gap-2 sm:grid-cols-2">
            {fields.map(([label, value]) => (
              <div key={label} className="rounded-lg border bg-muted/70 p-3">
                <dt className="text-xs font-bold text-muted-foreground">{label}</dt>
                <dd className="mt-1 font-bold">{value}</dd>
              </div>
            ))}
          </dl>
          <div className="mt-5 flex flex-wrap gap-2">
            <Button>
              <CheckCircle2 className="size-4" />
              Create product profile
            </Button>
            <Button variant="secondary">Review evidence</Button>
          </div>
        </Card>
      </section>
    </div>
  );
}

