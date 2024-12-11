import {StrictMode} from 'react'
import {createRoot} from 'react-dom/client'
import {ChakraProvider} from "@chakra-ui/react";
import {chakraSystem} from "./theme/appTheme.ts";
import {RouterProvider} from "react-router";
import router from "./router/router.tsx";
import './index.css'

createRoot(document.getElementById('root')!).render(
    <StrictMode>
        <ChakraProvider value={chakraSystem}>
            <RouterProvider router={router}></RouterProvider>
        </ChakraProvider>
    </StrictMode>,
)
