"use client"
import {useCallback, useEffect, useState} from "react";
import {useParams, useRouter} from "next/navigation";

import {Card, CardContent,} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Skeleton} from "@/components/ui/skeleton";
import {TypographyH4,} from "@/components/ui/typography";
import {ProjectDatabase} from "@/lib/types/project_database";


export const ProjectDashboard = () => {
    const [projectTables, setProjectTables] = useState<ProjectDatabase[]>([]);
    const {project_id} = useParams()
    const router = useRouter();


    useEffect(() => {
        if (project_id) {
            const fetchProjectTableList = async () => {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_BACKEND}/api/v1/projects/${project_id}/databases/`,
                    {
                        method: "GET",
                        headers: {
                            "Content-Type": "application/json",
                            "ngrok-skip-browser-warning": "true",
                        },
                    }
                );
                if (response.ok) {
                    const data = await response.json();
                    setProjectTables(data);
                }
            };
            fetchProjectTableList();
        }
    }, [project_id]);


    const handleEdit = useCallback((item: ProjectDatabase) => {
        console.log(item);
    }, [])
    const handleOpen = useCallback((item: ProjectDatabase) => {
        router.push(`/projects/${item.project_id}/databases/${item.id}`);
    }, [router])
    const handleDelete = useCallback((item: ProjectDatabase) => {
        console.log(item);
    }, [])

    return (
        <section className="w-full flex flex-col items-center gap-4">
            {projectTables.length > 0 ? (
                projectTables.map((item) => (
                    <Card key={item.id} className="w-full max-w-3xl p-0 border border-gray-200 shadow-sm rounded-lg">
                        <CardContent className="flex flex-row gap-4 p-4 items-start">
                            <div className="w-2/3 flex flex-col justify-between gap-2">
                                <div>
                                    <TypographyH4 className="font-semibold">
                                        {item.title}
                                    </TypographyH4>
                                </div>
                                <div className="flex items-center justify-between mt-4">
                                    <div className="flex space-x-2">
                                        <Button variant="default" onClick={() => handleOpen(item)}>
                                            Open
                                        </Button>
                                        <Button variant="outline" onClick={() => handleEdit(item)}>
                                            Edit
                                        </Button>
                                        <Button variant="destructive" onClick={() => handleDelete(item)}>
                                            Delete
                                        </Button>
                                    </div>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))
            ) : (
                <Skeleton className="w-full max-w-md h-64 rounded-md"/>
            )}
        </section>
    );
};