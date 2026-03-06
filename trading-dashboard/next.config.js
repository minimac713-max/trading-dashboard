/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  env: {
    NEXT_PUBLIC_KRAKEN_API_URL: process.env.NEXT_PUBLIC_KRAKEN_API_URL || 'https://api.kraken.com/0/public',
  },
}

module.exports = nextConfig
