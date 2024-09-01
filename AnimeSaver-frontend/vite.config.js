import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: "0.0.0.0", // Allow access from any network interface
    // port: 3000, // Set the port to 3000 or any other port you prefer
    // strictPort: true, // Ensure Vite uses the specified port and fails if it's not available
  },
});
