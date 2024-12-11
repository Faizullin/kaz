import {configureStore} from "@reduxjs/toolkit";
import {authSlice} from "./reducers/authSlice";
import {rootLayoutControllerSlice} from "./reducers/rootLayoutControllerSlice";
import {api} from "@/core/redux/api/api.ts";
import {filterSlice} from "@/core/redux/reducers/filter/filter.slice.ts";
import {cartSlice} from "@/core/redux/reducers/cartSlice.ts";
import {wishlistSlice} from "@/core/redux/reducers/wishlistSlice.ts";

const store = configureStore({
    reducer: {
        auth: authSlice.reducer,
        rootLayoutController: rootLayoutControllerSlice.reducer,
        filter: filterSlice.reducer,
        wishlist: wishlistSlice.reducer,
        cart: cartSlice.reducer,
        [api.reducerPath]: api.reducer,
    },
    middleware: (getDefaultMiddleware) => getDefaultMiddleware().concat(api.middleware),
    devTools: import.meta.env.NODE_ENV !== "production",
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
export default store;