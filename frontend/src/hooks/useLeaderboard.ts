import { useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import type { LeaderboardEntry, LeaderboardEntryCreate } from '@/types/api';

export const useLeaderboard = (token?: string | null) => {
  const queryClient = useQueryClient();

  const { data: entries = [], isLoading, refetch } = useQuery<LeaderboardEntry[]>({
    queryKey: ['leaderboard'],
    queryFn: () => api.get('/leaderboard'),
  });

  const addEntryMutation = useMutation({
    mutationFn: (entry: LeaderboardEntryCreate) =>
      api.post('/leaderboard', entry, token || undefined),
    onSuccess: () => {
      // Invalidate and refetch leaderboard after a successful submission
      queryClient.invalidateQueries({ queryKey: ['leaderboard'] });
    },
  });

  const addEntry = useCallback((email: string, score: number, round: number) => {
    if (!token) return Promise.reject(new Error('Authentication required'));
    return addEntryMutation.mutateAsync({ email, score, round });
  }, [token, addEntryMutation.mutateAsync]);

  return {
    entries,
    isLoading,
    addEntry,
    refresh: refetch,
    isSubmitting: addEntryMutation.isPending,
  };
};
