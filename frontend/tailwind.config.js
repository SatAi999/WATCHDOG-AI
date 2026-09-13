/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./features/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: "#08090d",
          surface: "#10121a",
          card: "#161924",
          border: "#212638",
          muted: "#8b949e",
        },
        brand: {
          primary: "#10b981", // Electric emerald
          secondary: "#6366f1", // Deep indigo
          accent: "#00f2fe", // Cyber cyan
          warning: "#f59e0b",
          danger: "#ef4444",
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace']
      }
    },
  },
  plugins: [],
}
