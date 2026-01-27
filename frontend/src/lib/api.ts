const API_BASE_URL = 'http://localhost:3000';

export const api = {
    async get(path: string, token?: string) {
        const headers: Record<string, string> = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const response = await fetch(`${API_BASE_URL}${path}`, {
            headers,
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            console.error(`API Error [${response.status}] ${path}:`, error);
            throw new Error(error.detail || `API request failed (${response.status})`);
        }
        return response.json();
    },

    async post(path: string, body: any, token?: string) {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        const response = await fetch(`${API_BASE_URL}${path}`, {
            method: 'POST',
            headers,
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
            console.error(`API Error [${response.status}] ${path}:`, error);
            throw new Error(error.detail || `API request failed (${response.status})`);
        }
        return response.json();
    },
};
