import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@transitpulse/ui", "@transitpulse/shared-types"]
};

export default nextConfig;
