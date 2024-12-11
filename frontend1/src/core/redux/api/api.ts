import {createApi,} from '@reduxjs/toolkit/query/react';
import {baseQueryWithReAuth} from "@/core/redux/api/auth/auth.baseQuery.ts";

export const api = createApi({
    reducerPath: 'api',
    baseQuery: baseQueryWithReAuth,
    tagTypes: ['Product', 'Auth'],
    endpoints: () => ({}),
});