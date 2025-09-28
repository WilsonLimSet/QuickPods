import { getRequestConfig } from "next-intl/server";
import { cookies } from "next/headers";

// Priority languages for tech/startup content (high internet penetration + tech interest)
export const locales = [
  "en",
  "zh",
  "zh-TW",
  "ja",
  "ko",
  "id",
  "es",
  "pt",
  "hi",
  "fr",
  "de",
  "th",
  "vi",
];
export const defaultLocale = "en";

// Language names for AI translation prompts
export const languageNames = {
  en: "English",
  zh: "Simplified Chinese (简体中文)",
  "zh-TW": "Traditional Chinese (繁體中文)",
  ja: "Japanese (日本語)",
  ko: "Korean (한국어)",
  id: "Indonesian (Bahasa Indonesia)",
  es: "Spanish (Español)",
  pt: "Portuguese (Português)",
  hi: "Hindi (हिन्दी)",
  fr: "French (Français)",
  de: "German (Deutsch)",
  th: "Thai (ไทย)",
  vi: "Vietnamese (Tiếng Việt)",
};

// Language display names for UI
export const languageDisplayNames = {
  en: "English",
  zh: "简体中文",
  "zh-TW": "繁體中文",
  ja: "日本語",
  ko: "한국어",
  id: "Bahasa Indonesia",
  es: "Español",
  pt: "Português",
  hi: "हिन्दी",
  fr: "Français",
  de: "Deutsch",
  th: "ไทย",
  vi: "Tiếng Việt",
};

export default getRequestConfig(async () => {
  const cookieStore = await cookies();
  const locale = cookieStore.get("NEXT_LOCALE")?.value || defaultLocale;

  return {
    locale,
    messages: (await import(`../messages/${locale}.json`)).default,
  };
});
