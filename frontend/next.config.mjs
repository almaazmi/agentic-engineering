/** @type {import('next').NextConfig} */
const nextConfig = {
  // Produce a self-contained server bundle for a small container image.
  output: "standalone",
  reactStrictMode: true,
};

export default nextConfig;
