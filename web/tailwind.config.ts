import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/data/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        aeroblue: {
          50: "#f0f7ff",
          100: "#e0effe",
          200: "#b9ddfd",
          300: "#7cc2fb",
          400: "#36a3f7",
          500: "#0c87eb",
          600: "#026ac9",
          700: "#0354a3",
          800: "#074786",
          900: "#0c3c6f",
          950: "#082649",
        },
        technical: {
          slate: "#0f172a",
          charcoal: "#1e293b",
          steel: "#334155",
          muted: "#64748b",
          border: "#e2e8f0",
          paper: "#fcfbf9",
          subtle: "#f8fafc",
          darkBg: "#090d16",
          darkCard: "#0f172a",
          darkBorder: "#1e293b",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        serif: ["Merriweather", "Georgia", "Cambria", "serif"],
        mono: ["JetBrains Mono", "Fira Code", "Consolas", "monospace"],
      },
      aspectRatio: {
        "16/9": "16 / 9",
      },
      boxShadow: {
        subtle: "0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px 0 rgba(0, 0, 0, 0.03)",
        elevation: "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)",
      },
    },
  },
  plugins: [],
};
export default config;
