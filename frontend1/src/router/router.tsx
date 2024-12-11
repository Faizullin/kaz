import {createBrowserRouter, createRoutesFromElements, Route} from "react-router";
import RootLayout from "../shared/layouts/RootLayout.tsx";
import DefaultLayout from "../shared/layouts/DefaultLayout.tsx";
import Home from "../features/home/Home.tsx";

const router = createBrowserRouter(
    createRoutesFromElements(
        <Route path="/" element={<RootLayout/>}>
            <Route path="/" element={<DefaultLayout/>}>
                <Route path="/" element={<Home/>}/>
            </Route>
        </Route>
    )
);

export default router;