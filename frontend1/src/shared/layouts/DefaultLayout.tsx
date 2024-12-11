import {Box} from "@chakra-ui/react";
import {Outlet} from "react-router";
import Sidebar from "../components/common/sidebar/Sidebar.tsx";

const DefaultLayout = () => {
    return (

        <Box w="100%">
            <Sidebar/>
            <Outlet/>
        </Box>
    )
}
export default DefaultLayout;