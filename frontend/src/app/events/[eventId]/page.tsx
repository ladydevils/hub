// === GITHUB PAGES COMPATIBILITY ===
// When moving off static export go to FullEventView.tsx for detailed instructions 

import FullEventView from "@/components/static_export/FullEventView";

export async function generateStaticParams() {
    return [];
}

export default async function FullEventPage({ params }: { params: Promise<{ eventId: string }> }) {
    const { eventId } = await params;
    return <FullEventView eventId={eventId} />;
}