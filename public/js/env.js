async function fetchEnv() {
  try {
    const response = await fetch('/api/env');
    if (!response.ok) {
      throw new Error('Failed to fetch environment variables');
    }
    const env = await response.json();
    window.env = env;
  } catch (error) {
    console.error('Error fetching environment variables:', error);
    window.env = {};
  }
}

fetchEnv(); 