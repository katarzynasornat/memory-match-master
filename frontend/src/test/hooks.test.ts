import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';
import { useLeaderboard } from '@/hooks/useLeaderboard';

// Mock fetch globally
global.fetch = vi.fn();

describe('useAuth', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('should start with no user after loading', async () => {
    const { result } = renderHook(() => useAuth());

    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    expect(result.current.user).toBe(null);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should login successfully', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ user: { email: 'test@example.com' }, token: 'mock-token' }),
    });

    const { result } = renderHook(() => useAuth());

    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });

    expect(result.current.user?.email).toBe('test@example.com');
    expect(result.current.token).toBe('mock-token');
    expect(result.current.isAuthenticated).toBe(true);
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/auth/login'), expect.any(Object));
  });

  it('should persist auth state to localStorage', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ user: { email: 'test@example.com' }, token: 'mock-token' }),
    });

    const { result } = renderHook(() => useAuth());

    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });

    const stored = localStorage.getItem('memory_game_auth');
    expect(JSON.parse(stored!)).toEqual({
      user: { email: 'test@example.com' },
      token: 'mock-token'
    });
  });

  it('should logout successfully', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ user: { email: 'test@example.com' }, token: 'mock-token' }),
    });

    const { result } = renderHook(() => useAuth());

    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });

    await act(async () => {
      await result.current.login('test@example.com', 'password');
    });

    act(() => {
      result.current.logout();
    });

    expect(result.current.user).toBe(null);
    expect(result.current.token).toBe(null);
    expect(result.current.isAuthenticated).toBe(false);
    expect(localStorage.getItem('memory_game_auth')).toBe(null);
  });
});

describe('useLeaderboard', () => {
  const mockEntries = [
    { email: 'player1@example.com', score: 100, round: 2, date: '2024-01-01' }
  ];

  beforeEach(() => {
    localStorage.clear();
    vi.clearAllMocks();
  });

  it('should fetch entries on mount', async () => {
    (fetch as any).mockResolvedValueOnce({
      ok: true,
      json: async () => mockEntries,
    });

    const { result } = renderHook(() => useLeaderboard());

    await vi.waitFor(() => {
      expect(result.current.entries).toEqual(mockEntries);
    });
    expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/leaderboard'), expect.any(Object));
  });

  it('should add entry to leaderboard and refresh', async () => {
    (fetch as any)
      .mockResolvedValueOnce({ ok: true, json: async () => [] }) // initial fetch
      .mockResolvedValueOnce({ ok: true, json: async () => ({}) }) // post result
      .mockResolvedValueOnce({ ok: true, json: async () => mockEntries }); // second fetch

    const { result } = renderHook(() => useLeaderboard('mock-token'));

    await act(async () => {
      await result.current.addEntry('player1@example.com', 100, 2);
    });

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining('/leaderboard'),
      expect.objectContaining({ method: 'POST' })
    );

    await vi.waitFor(() => {
      expect(result.current.entries).toEqual(mockEntries);
    });
  });

  it('should not add entry if no token provided', async () => {
    (fetch as any).mockResolvedValue({ ok: true, json: async () => [] });

    const { result } = renderHook(() => useLeaderboard(null));

    await act(async () => {
      await result.current.addEntry('player1@example.com', 100, 2);
    });

    // Only the initial GET should have been called
    expect(fetch).not.toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({ method: 'POST' })
    );
  });
});
