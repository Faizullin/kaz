import {Box, Container, Table, Text} from "@chakra-ui/react"
import {useEffect, useState} from "react";
import {IProject} from "@/core/types/models/IProject.ts";

const Home = () => {
    // const { user: currentUser } = useAuth()
    const [projects, setProjects] = useState<IProject[]>([])
    useEffect(() => {
        setProjects([])
    }, [])
    return (
        <>
            <Container maxW="full">
                <Box pt={12} m={4}>
                    {/*<Text fontSize="2xl">*/}
                    {/*    Hi, {currentUser?.full_name || currentUser?.email} 👋🏼*/}
                    {/*</Text>*/}
                    <Text>Welcome back, nice to see you again!</Text>
                </Box>
                <Table.Root size="sm" striped>
                    <Table.Header>
                        <Table.Row>
                            <Table.ColumnHeader>Id</Table.ColumnHeader>
                            <Table.ColumnHeader>Title</Table.ColumnHeader>
                        </Table.Row>
                    </Table.Header>
                    <Table.Body>
                        {projects.map((item) => (
                            <Table.Row key={item.id}>
                                <Table.Cell>{item.id}</Table.Cell>
                                <Table.Cell>{item.title}</Table.Cell>
                            </Table.Row>
                        ))}
                    </Table.Body>
                </Table.Root>
            </Container>
        </>
    )
}
export default Home;