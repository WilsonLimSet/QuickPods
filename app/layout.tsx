import { GeistSans } from "geist/font/sans";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react";

const defaultUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : "http://localhost:3000";

export const metadata = {
  metadataBase: new URL(defaultUrl),
  title: "CEO Insights",
  description: "Effortless Podcast Discovery",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={GeistSans.className}>
      <body className="flex min-h-screen flex-1 flex-col items-center bg-background text-foreground">
        <main className="w-full">
          {children}
          <Analytics />
        </main>
      </body>
    </html>
  );
}
