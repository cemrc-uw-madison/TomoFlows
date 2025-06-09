import axios from 'axios';

// Handle CSRF better
axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.withCredentials = true;

// Automatically determine base path from current location
const prefix = window.location.pathname.split("/").slice(0, 4).join("/"); // "/node/<host>/<port>"

const api = axios.create({
  baseURL: `${prefix}/api/`,  // e.g., "/node/myhost/8000/api/"
});

export default api;

