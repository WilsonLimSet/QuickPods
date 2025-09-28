import { type NextRequest, NextResponse } from "next/server";
import { updateSession } from "@/utils/supabase/middleware";
import { locales, defaultLocale } from "./i18n/request";

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (pathname.startsWith("/api") || pathname.startsWith("/_next")) {
    return await updateSession(request);
  }

  const pathnameHasLocale = locales.some(
    (locale) => pathname.startsWith(`/${locale}/`) || pathname === `/${locale}`
  );

  if (pathnameHasLocale) {
    const locale = pathname.split("/")[1];
    const response = await updateSession(request);
    response.cookies.set("NEXT_LOCALE", locale);
    return response;
  }

  const cookieLocale = request.cookies.get("NEXT_LOCALE")?.value;
  const acceptLanguage = request.headers.get("accept-language");

  let detectedLocale = defaultLocale;

  if (cookieLocale && locales.includes(cookieLocale)) {
    detectedLocale = cookieLocale;
  } else if (acceptLanguage) {
    const languages = acceptLanguage
      .split(",")
      .map((lang) => lang.split(";")[0].trim().toLowerCase());

    for (const lang of languages) {
      if (locales.includes(lang)) {
        detectedLocale = lang;
        break;
      }
      const langPrefix = lang.split("-")[0];
      if (locales.includes(langPrefix)) {
        detectedLocale = langPrefix;
        break;
      }
    }
  }

  const newUrl = new URL(`/${detectedLocale}${pathname}`, request.url);
  const response = NextResponse.redirect(newUrl);
  response.cookies.set("NEXT_LOCALE", detectedLocale);
  return response;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - images - .svg, .png, .jpg, .jpeg, .gif, .webp
     * Feel free to modify this pattern to include more paths.
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
