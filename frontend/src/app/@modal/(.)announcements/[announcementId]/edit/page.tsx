// === GITHUB PAGES COMPATIBILITY ===
// When moving off static export go to EditAnnouncementModalView.tsx for detailed instructions

import EditAnnouncementModalView from "@/components/static_export/EditAnnouncementModalView";

export async function generateStaticParams() {
    return [];
}

export default async function EditAnnouncementPage({ params }: { params: Promise<{ announcementId: string }> }) {
    const { announcementId } = await params;
    return <EditAnnouncementModalView announcementId={announcementId} />;
}