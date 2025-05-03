// vite.config.js
export default {
  server: {
    host: true, // Allows access via local IP like 10.0.0.165
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true, // Optional (safe to include)
        secure: false       // Optional, skip for HTTPS targets
      }
    }
  }
}
