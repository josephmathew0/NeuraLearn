import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Fetch all quiz questions from Flask API
export const fetchQuestions = async () => {
  try {
    const response = await api.get("/questions");
    console.log("🔍 API Response (Questions):", response.data); // Debug log
    return response.data;
  } catch (error) {
    console.error("🚨 Error fetching questions:", error);
    return [];
  }
};

// Submit a user response to Flask API
export const submitAnswer = async (userId, questionId, answer) => {
  try {
    const response = await api.post("/responses", {
      user_id: userId,
      question_id: questionId,
      answer: answer,
    });
    return response.data;
  } catch (error) {
    console.error("Error submitting response:", error);
    return { correct: false, message: "Error submitting answer" };
  }
};

// Fetch past responses for a user
export const fetchUserResponses = async (userId) => {
  try {
    const response = await api.get(`/users/${userId}/responses`);
    return response.data;
  } catch (error) {
    console.error("Error fetching user responses:", error);
    return [];
  }
};
