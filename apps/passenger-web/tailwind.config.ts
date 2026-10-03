import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "../../packages/ui/src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        background: "#090d16",
        surface: "#111827",
        primary: "#4f46e5",
        accent: "#06b6d4"
      }
    }
  },
  plugins: []
};

export default config;
