import { redirect } from "next/navigation";
import { use } from "react";

// === GITHUB PAGES COMPATIBILITY ===
// Remove this export when moving off static export
export async function generateStaticParams() {
    return [];
}
// === END GITHUB PAGES COMPATIBILITY ===

export default function EventEditFallback({ params }: { params: Promise<{ eventId: string }> }){
    const { eventId } = use(params);
    redirect(`/events/${eventId}`);
}