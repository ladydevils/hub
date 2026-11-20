import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // added for exporting frontend to GitLab
  // Next.js needs a server to optimize images which GitLab doesn't support. MIght result in larger page load
  output: "export",
  images: {
    unoptimized: true,
  },
  basePath: "/hub",
  assetPrefix: "/hub/",

  devIndicators: false,
  allowedDevOrigins: ["192.168.68.78", "172.20.10.2", "10.0.0.20", "192.168.1.8", "10.197.28.231", "10.197.255.102"],
  /* config options here */

  turbopack: {
    rules: {
      "*.svg": {
        loaders: [
          {
            loader: "@svgr/webpack",
            options: {
              icon: true,
            },
          },
        ],
        as: "*.js",
      },
    },
  },
};

export default nextConfig;
