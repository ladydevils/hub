"use client"

import { useContext, useEffect } from "react";
import SidebarContent from "@/components/SidebarContent";
import { MobileSidebarContext } from "@/contexts/SidebarContext";
import useMediaQuery from "@/hooks/useMediaQuery";

import { usePathname } from "next/navigation";
import Link from "next/link";
import LadyDevilsLogo from "@/assets/LadyDevilsVectorFinal.svg";
import CrossIcon from "@/assets/icons/cross.svg";
import { Tooltip, TooltipContent, TooltipTrigger} from "@/components/ui/tooltip";


export default function MobileSidebar() {
    const mobile = useContext(MobileSidebarContext);

    const pathname = usePathname();
    const isDesktop = useMediaQuery("(min-width: 850px)")

    useEffect(() => {
        mobile.closeSidebar();
    }, [isDesktop, pathname])
    
    return (
        <>
            { mobile.isOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-100 sidebar:hidden transition-all duration-500"
                    onClick={mobile.closeSidebar}
                />
            )}

            <div className={` sidebar:hidden flex flex-col fixed h-screen z-200 bg-navigation items-center w-[192px] font-body shadow-sidebar transition-transform ${mobile.isOpen === true ? "translate-x-0" : "-translate-x-full"}`}>
                <div className="mt-2 flex flex-col w-full select-none">
                    <button className="sidebar:hidden mr-2 hover:bg-black/20 group pl-1 pb-1 hover:cursor-pointer ml-auto transition-all duration-100" onClick={mobile.closeSidebar}>
                        <CrossIcon className="text-foreground/20 mt-1 mr-1 group-hover:text-foreground/40"/>
                    </button>
                    <div className="flex flex-col items-center">
                    <Tooltip>
                        <TooltipTrigger delay={250}>
                            <Link href="/" onClick={mobile.closeSidebar} >
                                <LadyDevilsLogo className="w-[6rem] h-auto hover:scale-105 transition-transform mx-auto"/>
                            </Link>
                        </TooltipTrigger>
                        <TooltipContent side="right" className="text-sm" arrowClassName="border-b-1 border-l-1 border-primary/80 shadow-[-1px_1px_0_0_color-mix(in_srgb,var(--color-muted-1)_50%,transparent)] ">
                            <p>Home</p>
                        </TooltipContent>
 
                    </Tooltip>
                    </div>
                    
                </div>
                <SidebarContent/>
            </div>
        </>
    );
};
