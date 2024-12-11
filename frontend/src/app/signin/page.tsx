import { Metadata } from "next";
import SigninPage from "./SigninPage";

export const metadata: Metadata = {
  title: "Sign In Page | Free Next.js Template for Startup and SaaS",
  description: "This is Sign In Page for Startup Nextjs Template",
  // other metadata
};

const Page = () => {
  return <SigninPage />;
};

export default Page;
