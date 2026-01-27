import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';

interface User {
  email: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
}

const AUTH_KEY = 'memory_game_auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({ user: null, token: null });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem(AUTH_KEY);
    if (stored) {
      try {
        setAuthState(JSON.parse(stored));
      } catch {
        localStorage.removeItem(AUTH_KEY);
      }
    }
    setIsLoading(false);
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const data = await api.post('/auth/login', { email, password });
    const newState = { user: data.user, token: data.token };
    localStorage.setItem(AUTH_KEY, JSON.stringify(newState));
    setAuthState(newState);
    return data.user;
  }, []);

  const signup = useCallback(async (email: string, password: string) => {
    const data = await api.post('/auth/signup', { email, password });
    const newState = { user: data.user, token: data.token };
    localStorage.setItem(AUTH_KEY, JSON.stringify(newState));
    setAuthState(newState);
    return data.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(AUTH_KEY);
    setAuthState({ user: null, token: null });
  }, []);

  return {
    user: authState.user,
    token: authState.token,
    isLoading,
    isAuthenticated: !!authState.token,
    login,
    signup,
    logout,
  };
};
