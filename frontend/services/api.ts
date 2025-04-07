// api.ts
import axios from 'axios';

const BASE_URL = 'https://voice-fitness-app-backend.onrender.com'; // Replace with your actual backend URL

export const login = async (email: string, password: string): Promise<any> => {
  try {
    const response = await axios.post(`${BASE_URL}/login/`, {
      email,
      password,
    });
    return response.data;
  } catch (error) {
    console.error('Login failed', error);
    throw error;
  }
};
