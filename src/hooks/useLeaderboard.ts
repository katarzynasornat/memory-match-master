import { useState, useEffect, useCallback } from 'react';

export interface LeaderboardEntry {
  username: string;
  score: number;
  round: number;
  date: string;
}

const LEADERBOARD_KEY = 'memory_game_leaderboard';
const MAX_ENTRIES = 10;

export const useLeaderboard = () => {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    const stored = localStorage.getItem(LEADERBOARD_KEY);
    if (stored) {
      try {
        setEntries(JSON.parse(stored));
      } catch {
        localStorage.removeItem(LEADERBOARD_KEY);
      }
    }
  }, []);

  const addEntry = useCallback((username: string, score: number, round: number) => {
    const newEntry: LeaderboardEntry = {
      username,
      score,
      round,
      date: new Date().toISOString(),
    };

    setEntries(prev => {
      const updated = [...prev, newEntry]
        .sort((a, b) => b.score - a.score)
        .slice(0, MAX_ENTRIES);
      
      localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  const clearLeaderboard = useCallback(() => {
    localStorage.removeItem(LEADERBOARD_KEY);
    setEntries([]);
  }, []);

  return {
    entries,
    addEntry,
    clearLeaderboard,
  };
};
