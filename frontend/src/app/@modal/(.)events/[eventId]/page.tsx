// === GITHUB PAGES COMPATIBILITY ===
// When moving off static export go to FullEventModalView.tsx for detailed instructions 

import FullEventModalView from "@/components/static_export/FullEventModalView";

export async function generateStaticParams() {
    return [{ eventId: "placeholder" }];
};

export default async function FullEventModalPage({ params }: { params: Promise<{ eventId: string }> }) {
    const { eventId } = await params;
    return <FullEventModalView eventId={eventId} />;
};