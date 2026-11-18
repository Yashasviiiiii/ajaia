// API configuration based on environment
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Use the API URL for development, or the deployed URL for production
export const apiClient = {
  baseURL: API_URL,
  withCredentials: true,
};
