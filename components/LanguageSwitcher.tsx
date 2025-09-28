"use client";

import { useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { languageDisplayNames } from "@/i18n/locales";
import { Globe, ChevronDown } from "lucide-react";

export default function LanguageSwitcher() {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();
  const pathname = usePathname();

  // Extract current locale from pathname
  const currentLocale = pathname.split("/")[1] || "en";

  const handleLanguageChange = (locale: string) => {
    // Replace the current locale in the pathname with the new one
    const segments = pathname.split("/");
    segments[1] = locale;
    const newPath = segments.join("/");

    // Set locale cookie
    document.cookie = `NEXT_LOCALE=${locale}; path=/; max-age=31536000; SameSite=Lax`;

    router.push(newPath);
    setIsOpen(false);
  };

  return (
    <div className="fixed bottom-4 right-4 z-50">
      <div className="relative">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-2 rounded-lg border border-gray-200 bg-white/90 px-3 py-2 text-sm text-gray-700 shadow-lg backdrop-blur-sm transition-all duration-200 hover:bg-white hover:shadow-xl"
        >
          <Globe size={16} />
          <span>
            {
              languageDisplayNames[
                currentLocale as keyof typeof languageDisplayNames
              ]
            }
          </span>
          <ChevronDown
            size={14}
            className={`transition-transform duration-200 ${isOpen ? "rotate-180" : ""}`}
          />
        </button>

        {isOpen && (
          <>
            {/* Backdrop */}
            <div
              className="fixed inset-0 z-[-1]"
              onClick={() => setIsOpen(false)}
            />

            {/* Dropdown */}
            <div className="absolute bottom-full right-0 mb-2 max-h-64 w-48 overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-xl">
              <div className="p-2">
                {Object.entries(languageDisplayNames).map(
                  ([locale, displayName]) => (
                    <button
                      key={locale}
                      onClick={() => handleLanguageChange(locale)}
                      className={`w-full rounded-md px-3 py-2 text-left text-sm transition-colors ${
                        currentLocale === locale
                          ? "bg-blue-50 font-medium text-blue-600"
                          : "text-gray-700 hover:bg-gray-50"
                      }`}
                    >
                      {displayName}
                    </button>
                  )
                )}
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
