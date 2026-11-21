"use client";

import { use, useState, useEffect } from "react";
import { PracticeDetails, ExtendedPracticeProps } from "@/components/PracticeCard";
import { TournamentDetails, ExtendedTournamentProps } from "@/components/TournamentCard";
import { EventDetails, ExtendedEventProps } from "@/components/GenericEventCard";

import api from "@/lib/api";

type ExtendedEvent = ExtendedPracticeProps | ExtendedTournamentProps | ExtendedEventProps

export default function FullEvent({ params }: { params: Promise<{ eventId: string }> }) {
    const { eventId } = use(params);

    const [event, setEvent] = useState<ExtendedEvent | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string>("");

    const fetchEvent = async () => {
            try {
                const response = await api.get(`/events/${eventId}`)
                setEvent(response.data)
            } catch (err) {
                console.error(err)
                setError("Could not load this event.")
            } finally {
                setIsLoading(false)
            }
        };

    useEffect(() => {
        fetchEvent()
    }, [eventId]);

    if (isLoading) {
        return <div className="flex h-full items-center justify-center">Loading...</div>;
    }

    if (error || !event) {
        return <div className="flex h-full items-center justify-center">{error || "Event not found."}</div>;
    }

    return (
        <div className="flex h-full contents">
            <div className="flex flex-1 min-w-0 h-full items-center py-12 px-8">
            
            { event.category === "practice" && 
                <PracticeDetails { ...(event as ExtendedPracticeProps) } onRefetch={fetchEvent} /> 
            }

            { event.category === "tournament" && 
                <TournamentDetails { ...(event as ExtendedTournamentProps) } onRefetch={fetchEvent}/>  
            }

            { (event.category !== "practice" && event.category !== "tournament") &&
                <EventDetails { ...(event as ExtendedEventProps)  } onRefetch={fetchEvent}/>  
            }
            
            </div>
        </div>
        
    )
};