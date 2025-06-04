import axios from 'axios';

// Automatically determine base path from current location
const prefix = window.location.pathname.split("/").slice(0, 4).join("/"); // "/node/<host>/<port>"

const api = axios.create({
  baseURL: `${prefix}/api/`,  // e.g., "/node/myhost/8000/api/"
});

export default api;

