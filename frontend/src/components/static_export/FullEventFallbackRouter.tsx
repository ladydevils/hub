// === GITHUB PAGES COMPATIBILITY — delete this entire file when off static export ===

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import FullEventView from "./FullEventView";

const BASE_PATH = "/hub";

export default function EventFallbackRouter({ notEventUrl }: { notEventUrl: () => void }) {
    const router = useRouter();
    const [eventId, setEventId] = useState<string | null>(null);

    useEffect(() => {
        let path = window.location.pathname;
        if (path.startsWith(BASE_PATH)) {
            path = path.slice(BASE_PATH.length);
        }

        const editMatch = path.match(/^\/events\/(\d+)\/edit\/?$/);
        if (editMatch) {
            router.replace(`/events/${editMatch[1]}`);
            return;
        }

        const viewMatch = path.match(/^\/events\/(\d+)\/?$/);
        if (viewMatch) {
            setEventId(viewMatch[1]);
            return;
        }

        notEventUrl();
    }, []);

    if (!eventId) {
        return null;
    }

    return <FullEventView eventId={eventId} />;
}