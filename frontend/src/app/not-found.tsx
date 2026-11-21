// === GITHUB PAGES COMPATIBILITY — delete, or strip down to just the "Page not found" div, when off static export ===

"use client";

import { useState } from "react";
import EventFallbackRouter from "@/components/static_export/FullEventFallbackRouter";

export default function NotFound() {
    const [isEventUrl, setIsEventUrl] = useState(true);

    if (isEventUrl) {
        return <EventFallbackRouter notEventUrl={() => setIsEventUrl(false)} />;
    }

    return (
        <div className="flex h-screen items-center justify-center text-xl">
            <span className="border-r-2 border-primary pr-4">
                404
            </span>
            <span className="pl-4">
                Page not found.
            </span>
            
        </div>
    );
}