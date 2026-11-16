import Link from "next/link";
import SearchBar from "@/components/SearchBar";
import { StatusPill, StatusPillSuspense } from "@/components/StatusPill";
import UpcomingPast from "./UpcomingPast";
import EventFilter from "./EventFilter";
import AddIcon from "@/assets/icons/add.svg";

type ToolBarProps = {
    past: boolean;
    setPast: (past: boolean) => void;

    activeFilter: string;
    setActiveFilter: (filter: string) => void;

    eventCount: number | null // null here until i incorporate suspense
};

export default function EventToolBar({ past, setPast, activeFilter, setActiveFilter, eventCount }: ToolBarProps) {

    return (
        <div className="py-3 overflow-visible flex gap-x-5 flex flex-col flex-wrap">
            <div>
                <UpcomingPast past={ past } setPast={ setPast }/>
            </div>

            <div className="flex flex-wrap gap-3 mt-5 items-end justify-between">
                <EventFilter activeFilter={ activeFilter } setActiveFilter={ setActiveFilter }/>


                <div className="flex items-end gap-2">
                    { eventCount === null && <StatusPillSuspense/>}
                    <StatusPill display={` ${ eventCount } ${ eventCount === 1 ? "Event" : "Events"}`}/>
                    <Link href="/executive-tools/create-event" className="flex gap-2 bg-white rounded-[5px] items-center justify-center px-3 py-1 text-primary font-semibold hover:bg-primary-light hover:text-card">
                        <AddIcon className="text-sm"/>
                        <span className="text-lg ">Add Event</span>
                    </Link>
                </div>
                
            </div>
        </div>
    )
};