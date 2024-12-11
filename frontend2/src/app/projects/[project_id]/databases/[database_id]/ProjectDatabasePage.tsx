"use client"
import {useEffect, useState} from "react";
import {useParams} from "next/navigation";
import {ProjectDatabase} from "@/lib/types/project_database";
import {Chat, Message} from "@/lib/types/chat";
import {useUser} from "@/contexts/user/context";
import {TypographyH3, TypographyP} from "@/components/ui/typography";
import {Input} from "@/components/ui/input";
import {Button} from "@/components/ui/button";


export const ProjectDatabasePage = () => {
    const [projectDatabase, setProjectDatabase] = useState<ProjectDatabase | null>(null);
    const {project_id, database_id} = useParams()


    useEffect(() => {
        if (project_id && database_id) {
            const fetchProjectDatabase = async () => {
                const response = await fetch(
                    `${process.env.NEXT_PUBLIC_BACKEND}/api/v1/projects/${project_id}/databases/${database_id}`,
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
                    setProjectDatabase(data);
                }
            };
            fetchProjectDatabase();
        }
    }, [project_id, database_id]);

    const {user} = useUser()
    const [chat, setChat] = useState<Chat | null>(null);
    const [socket, setSocket] = useState<WebSocket | null>(null);
    const [messages, setMessages] = useState<Message[]>([]);
    const [newMessage, setNewMessage] = useState<string>("");
    useEffect(() => {
        const token = JSON.parse(localStorage.getItem('token') || '{}');
        const wsUrl = `${process.env.NEXT_PUBLIC_BACKEND}/ws/chat/1?token=${token.access_token}`;
        const newSocket = new WebSocket(wsUrl);

        newSocket.onopen = () => {
            console.log('WebSocket connected');
        };

        newSocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            console.log("onmessage: ",data);
            if (data.type === 'history') {
                setMessages(data.messages);
            } else {
                if (data.sender_id !== user.id) setMessages((prevMessages) => [...prevMessages, data]);
            }
        };

        newSocket.onclose = () => {
            console.log('WebSocket disconnected');
        };

        setSocket(newSocket);

        return () => {
            newSocket.close();
        };
    }, [user]);

    const handleSendMessage = () => {
        if (!socket || !user || !newMessage.trim()) return;

        socket.send(JSON.stringify({
            content: newMessage
        }));
        setNewMessage('');
        setMessages((prevMessages) => [...prevMessages, {
            sender_id: user.id,
            content: newMessage
        }]);

    };

    if(!user ) {
        return "Loading..."
    }

    return (
        <main
            className="m-auto w-full max-w-[500px] h-[calc(100dvh-90px)] relative border flex flex-col items-center justify-between gap-2">
            <div className="w-full flex items-center justify-center border-b py-2">
                <TypographyH3>{`Chat ${1}`}</TypographyH3>
            </div>

            <div className="flex flex-col h-full  gap-2 w-full p-4">
                {messages &&
                    messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex flex-col gap-1 ${
                                message.sender_id === user.id ? "items-end" : "items-start"
                            }`}
                        >
                            <TypographyP>{message.content}</TypographyP>
                        </div>
                    ))}
            </div>

            <div className="flex w-full items-center gap-2 sticky bottom-0 py-4 px-2 border-t left-0">
                <Input
                    placeholder="Type a message"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            handleSendMessage();
                        }
                    }}
                />
                <Button onClick={handleSendMessage}>Send</Button>
            </div>
        </main>
    );
};