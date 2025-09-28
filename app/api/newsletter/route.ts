import { createClient } from "@/utils/supabase/server";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json();

    if (!email || !email.includes("@")) {
      return NextResponse.json(
        { error: "Invalid email address" },
        { status: 400 },
      );
    }

    const supabase = await createClient();

    const { error } = await supabase
      .from("newsletter_subscribers")
      .insert([{ email, subscribed_at: new Date().toISOString() }]);

    if (error) {
      if (error.code === "23505") {
        return NextResponse.json(
          { error: "Email already subscribed" },
          { status: 409 },
        );
      }
      throw error;
    }

    return NextResponse.json(
      { message: "Successfully subscribed!" },
      { status: 200 },
    );
  } catch (error) {
    console.error("Newsletter subscription error:", error);
    return NextResponse.json({ error: "Failed to subscribe" }, { status: 500 });
  }
}
