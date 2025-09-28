import { MetadataRoute } from "next";
import { createClient } from "@/utils/supabase/server";
import { locales } from "@/i18n/request";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = process.env.NEXT_PUBLIC_SITE_URL || "https://quickpods.io";
  const supabase = await createClient();

  const { data: podcasts } = await supabase
    .from("podcasts")
    .select("md_slug, publish_date, locale")
    .eq("locale", "en");

  const routes: MetadataRoute.Sitemap = [];

  for (const locale of locales) {
    routes.push({
      url: `${baseUrl}/${locale}`,
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 1.0,
      alternates: {
        languages: Object.fromEntries(
          locales.map((l) => [l, `${baseUrl}/${l}`]),
        ),
      },
    });
  }

  if (podcasts) {
    for (const podcast of podcasts) {
      for (const locale of locales) {
        routes.push({
          url: `${baseUrl}/${locale}/blog/${podcast.md_slug}`,
          lastModified: podcast.publish_date
            ? new Date(podcast.publish_date)
            : new Date(),
          changeFrequency: "weekly",
          priority: 0.8,
          alternates: {
            languages: Object.fromEntries(
              locales.map((l) => [
                l,
                `${baseUrl}/${l}/blog/${podcast.md_slug}`,
              ]),
            ),
          },
        });
      }
    }
  }

  return routes;
}
