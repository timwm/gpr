import axios from "axios";
const token = localStorage.getItem("authtoken");

const axiosInstance = axios.create({
  baseURL: "https://api.example.com", // Replace with your API base URL
  timeout: 5000, // Request timeout in milliseconds
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`, // Add your authentication token here if needed
  },
});
// Add a response interceptor
axiosInstance.interceptors.response.use(
    (response) => response, // Pass successful responses
    (error) => {
      // Handle errors globally
      console.error("API Error:", error.response?.data || error.message);
      return Promise.reject(error);
    }
  );

export default axiosInstance;