import { redirect } from "next/navigation";

// === GITHUB PAGES COMPATIBILITY ===
// Remove this export when moving off static export
export async function generateStaticParams() {
    return [{ announcementId: "placeholder" }];
};
// === END GITHUB PAGES COMPATIBILITY ===

export default function AnnouncementEditFallback(){
    redirect("/");
};