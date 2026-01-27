import { useState, useEffect, useCallback } from 'react';
import { api } from '@/lib/api';

export interface LeaderboardEntry {
  email: string;
  score: number;
  round: number;
  date: string;
}

export const useLeaderboard = (token?: string | null) => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchLeaderboard = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await api.get('/leaderboard');
      setEntries(data);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchLeaderboard();
  }, [fetchLeaderboard]);

  const addEntry = useCallback(async (email: string, score: number, round: number) => {
    if (!token) return;
    try {
      await api.post('/leaderboard', { email, score, round }, token);
      await fetchLeaderboard();
    } catch (error) {
      console.error('Failed to submit score:', error);
      throw error;
    }
  }, [token, fetchLeaderboard]);

  return {
    entries,
    isLoading,
    addEntry,
    refresh: fetchLeaderboard,
  };
};
