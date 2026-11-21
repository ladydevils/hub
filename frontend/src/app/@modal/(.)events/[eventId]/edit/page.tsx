// === GITHUB PAGES COMPATIBILITY ===
// When moving off static export go to EditEventModalView.tsx for detailed instructions 

import EditEventModalView from "@/components/static_export/EditEventModalView";

export async function generateStaticParams() {
    return [];
}

export default async function EditEventPage({ params }: { params: Promise<{ eventId: string }> }) {
    const { eventId } = await params;
    return <EditEventModalView eventId={eventId} />;
}