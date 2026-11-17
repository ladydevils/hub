"use client"

import SidebarContent from "@/components/SidebarContent";
import Link from "next/link";
import LadyDevilsLogo from "@/assets/LadyDevilsVectorFinal.svg";
import { Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip";

export default function DesktopSidebar() {

    return (
        <div className=" hidden sidebar:flex flex-col fixed h-screen bg-navigation items-center sidebar:w-[min(17%,192px)] font-body shadow-sidebar select-none">
            <Tooltip>
                <TooltipTrigger delay={250}>
                    <Link href="/">
                        <LadyDevilsLogo className="w-[6.5rem] h-auto pt-3 hover:scale-105 transition-transform"/>
                    </Link>
                </TooltipTrigger>
                <TooltipContent side="right" className="text-sm" alignOffset={10}arrowClassName="border-b-1 border-l-1 border-primary/80 shadow-[-1px_1px_0_0_color-mix(in_srgb,var(--color-muted-1)_50%,transparent)] ">
                    <p>Home</p>
                </TooltipContent>
                
            </Tooltip>
            <SidebarContent/>
        </div>
    );
};
