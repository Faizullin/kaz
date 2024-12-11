import {useState} from "react";
import {Flex, Spinner} from "@chakra-ui/react";
import {Outlet} from "react-router";

const RootLayout = () => {
    const [rootLoading] = useState<boolean>(false);

    // const { loading } = useAppSelector((state) => state.auth);
    return (

        // <NiceModal.Provider>
        <Flex maxW="large" h="auto" position="relative">
            {rootLoading ? (
                <Flex justify="center" align="center" height="100vh" width="full">
                    <Spinner size="xl" color="ui.main"/>
                </Flex>
            ) : (
                <Outlet/>
            )}
        </Flex>
        // </NiceModal.Provider>
    );
}
export default RootLayout;