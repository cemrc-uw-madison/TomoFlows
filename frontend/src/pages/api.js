import axios from 'axios';

// Handle CSRF better
axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = "csrftoken"
axios.defaults.withCredentials = true;

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift().replace(/"/g, '');
    return null;
  }

// Automatically determine base path from current location
export const BASE_PREFIX = getCookie("BASE_PREFIX") || "/";
// const prefix = window.location.pathname.split("/").slice(0, 4).join("/"); // "/node/<host>/<port>"

const api = axios.create({
  baseURL: `${BASE_PREFIX}/api/`,  // e.g., "/node/myhost/8000/api/"
});

//const api = axios.create({
//    baseURL: `/api/`,  // e.g., "/node/myhost/8000/api/"
//});

export default api;

