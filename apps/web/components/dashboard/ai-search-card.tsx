"use client";

import { Sparkles } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const answers: Record<string, string> = {
  "Which warranties expire next month?":
    "Three warranties expire next month: Sony Camera Lens, TP-Link Router AMC, and Bose Headphones.",
  "Find my Samsung TV invoice.":
    "Found the Samsung Frame TV invoice from Croma, purchased on 02 Nov 2025 for INR 94,990.",
  "Items worth more than INR 50,000.":
    "You have 18 high-value items. The top matches are MacBook Pro 14, Sony Camera Lens, Samsung Frame TV, iPhone 16 Pro, and LG Refrigerator."
};

export function AiSearchCard() {
  const [answer, setAnswer] = useState(
    "Total household purchase value is INR 32.4L. Electronics account for INR 15.6L."
  );

  return (
    <Card>
      <CardHeader>
        <div>
          <p className="mb-1 text-xs font-bold uppercase text-primary">Ownly AI</p>
          <CardTitle>Ask your inventory</CardTitle>
          <CardDescription>Search products, invoices, warranties, documents, and timelines.</CardDescription>
        </div>
      </CardHeader>
      <div className="rounded-lg border bg-accent/10 p-4">
        <div className="flex gap-3">
          <Sparkles className="mt-1 size-4 shrink-0 text-accent" />
          <p className="m-0 text-sm leading-6">{answer}</p>
        </div>
      </div>
      <div className="mt-4 flex flex-wrap gap-2">
        {Object.keys(answers).map((prompt) => (
          <Button key={prompt} type="button" variant="secondary" className="min-h-8 px-3 text-xs" onClick={() => setAnswer(answers[prompt])}>
            {prompt}
          </Button>
        ))}
      </div>
    </Card>
  );
}

