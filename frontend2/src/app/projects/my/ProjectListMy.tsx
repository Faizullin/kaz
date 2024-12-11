"use client"
import {useCallback, useEffect, useState} from "react";
import {useRouter} from "next/navigation";

import {Card, CardContent,} from "@/components/ui/card";
import {Button} from "@/components/ui/button";
import {Skeleton} from "@/components/ui/skeleton";
import {TypographyH4,} from "@/components/ui/typography";
import {Project} from "@/lib/types/project";
import {useUser} from "@/contexts/user/context";


export const ProjectListMy = () => {
    const [projects, setProjects] = useState<Project[]>([]);
    const router = useRouter();
    const {user} = useUser()


    useEffect(() => {
        if (user) {
            const fetchProjectListMy = async () => {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_BACKEND}/api/v1/projects/my/`,
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
                    setProjects(data);
                }
            };
            fetchProjectListMy();
        }
    }, [user]);

    const handleEdit = useCallback((productId: number) => {
        router.push(`/products/edit/${productId}`);
    }, [router])
    const handleOpen = useCallback((productId: number) => {
        router.push(`/projects/${productId}/dashboard`);
    }, [router])

    const handleDelete = useCallback(async (productId: number) => {
        const token = JSON.parse(localStorage.getItem("token") || "{}");
        if (token) {
            const response = await fetch(
                `${process.env.NEXT_PUBLIC_BACKEND}/products/${productId}`,
                {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        "ngrok-skip-browser-warning": "true",
                        Authorization: `Bearer ${token.access_token}`,
                    },
                }
            );
            if (response.ok) {
                setProjects(projects.filter((product) => product.id !== productId));
            }
        }

    }, [projects]);

    return (
        <section className="w-full flex flex-col items-center gap-4">
            {projects.length > 0 ? (
                projects.map((product) => (
                    <Card key={product.id} className="w-full max-w-3xl p-0 border border-gray-200 shadow-sm rounded-lg">
                        <CardContent className="flex flex-row gap-4 p-4 items-start">
                            <div className="w-2/3 flex flex-col justify-between gap-2">
                                <div>
                                    <TypographyH4 className="font-semibold">
                                        {product.title}
                                    </TypographyH4>
                                </div>
                                <div className="flex items-center justify-between mt-4">
                                    <div className="flex space-x-2">
                                        <Button variant="default" onClick={() => handleOpen(product.id)}>
                                            Open
                                        </Button>
                                        <Button variant="outline" onClick={() => handleEdit(product.id)}>
                                            Edit
                                        </Button>
                                        <Button variant="destructive" onClick={() => handleDelete(product.id)}>
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