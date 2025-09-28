import { GeistSans } from "geist/font/sans";
import "./globals.css";
import { Analytics } from "@vercel/analytics/react";
import { ThemeProvider } from "next-themes";
import LanguageSwitcher from "@/components/LanguageSwitcher";

const defaultUrl = process.env.VERCEL_URL
  ? `https://${process.env.VERCEL_URL}`
  : "http://localhost:3000";

export const metadata = {
  metadataBase: new URL(defaultUrl),
  title: "Podummary - Tech CEO & Founder Interviews",
  description:
    "Discover and explore interviews with top tech CEOs, founders, and innovators. AI-powered summaries and insights from the best business podcasts.",
  keywords: [
    "CEO interviews",
    "founder interviews",
    "tech podcasts",
    "business interviews",
    "startup founders",
  ],
  openGraph: {
    title: "Podummary - Tech CEO & Founder Interviews",
    description:
      "Discover and explore interviews with top tech CEOs, founders, and innovators.",
    type: "website",
    url: defaultUrl,
  },
  twitter: {
    card: "summary_large_image",
    title: "Podummary - Tech CEO & Founder Interviews",
    description:
      "Discover and explore interviews with top tech CEOs, founders, and innovators.",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={GeistSans.className} suppressHydrationWarning>
      <body className="flex min-h-screen flex-1 flex-col items-center bg-background text-foreground">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <main className="w-full">
            {children}
            <LanguageSwitcher />
            <Analytics />
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
