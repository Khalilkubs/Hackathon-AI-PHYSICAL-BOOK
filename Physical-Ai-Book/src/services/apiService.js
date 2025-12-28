import axios from 'axios';

// API service to connect with RAG API
class ApiService {
  constructor() {
    // Use the same base URL as the existing API endpoints
    this.baseURL = 'http://127.0.0.1:8001'; // Default to local development server on port 8001
    this.apiClient = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 second timeout
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Method to set a different base URL (for production vs development)
  setBaseURL(url) {
    this.baseURL = url;
    this.apiClient.defaults.baseURL = url;
  }

  // Query the RAG system with retry mechanism
  async queryRAG(queryText, options = {}, maxRetries = 3) {
    const {
      userId = null,
      sessionId = null,
      metadata = null,
    } = options;

    let lastError;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const response = await this.apiClient.post('/query', {
          query_text: queryText,
          user_id: userId,
          session_id: sessionId,
          metadata: metadata,
        });

        return {
          success: true,
          data: response.data,
          status: response.status,
          attempt: attempt + 1,
        };
      } catch (error) {
        console.error(`API Error (attempt ${attempt + 1}/${maxRetries + 1}):`, error);
        lastError = error;

        // If this was the last attempt, return the error
        if (attempt === maxRetries) {
          break;
        }

        // Wait before retrying (exponential backoff: 1s, 2s, 4s...)
        const delay = Math.pow(2, attempt) * 1000;
        console.log(`Retrying in ${delay}ms...`);
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    // Handle the final error after all retries
    // Handle different types of errors
    if (lastError.response) {
      // Server responded with error status
      return {
        success: false,
        error: lastError.response.data || lastError.response.statusText,
        status: lastError.response.status,
        message: `API Error after ${maxRetries + 1} attempts: ${lastError.response.status} - ${lastError.response.statusText}`,
      };
    } else if (lastError.request) {
      // Request was made but no response received
      return {
        success: false,
        error: 'Network error - unable to reach server',
        status: null,
        message: `Unable to connect to the server after ${maxRetries + 1} attempts. Please check your connection.`,
      };
    } else {
      // Something else happened
      return {
        success: false,
        error: lastError.message,
        status: null,
        message: `Request error after ${maxRetries + 1} attempts: ${lastError.message}`,
      };
    }
  }

  // Validate query before sending to API
  async validateQuery(queryText) {
    try {
      const response = await this.apiClient.post('/validate-query', {
        query_text: queryText,
      });

      return {
        success: true,
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      console.error('Validation Error:', error);

      if (error.response) {
        return {
          success: false,
          error: error.response.data || error.response.statusText,
          status: error.response.status,
          message: `Validation Error: ${error.response.status} - ${error.response.statusText}`,
        };
      } else {
        return {
          success: false,
          error: error.message,
          status: null,
          message: `Validation request error: ${error.message}`,
        };
      }
    }
  }

  // Health check for the API
  async healthCheck() {
    try {
      const response = await this.apiClient.get('/health');

      return {
        success: true,
        data: response.data,
        status: response.status,
      };
    } catch (error) {
      console.error('Health Check Error:', error);

      return {
        success: false,
        error: error.message,
        status: error.response?.status || null,
        message: 'API health check failed',
      };
    }
  }
}

// Create a singleton instance
const apiService = new ApiService();

export default apiService;

// Export the class for potential direct instantiation
export { ApiService };