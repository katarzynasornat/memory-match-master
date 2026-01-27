import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '@/hooks/useAuth';
import { useLeaderboard } from '@/hooks/useLeaderboard';

describe('useAuth', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should start with no user after loading', async () => {
    const { result } = renderHook(() => useAuth());
    
    // Wait for loading to complete
    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    expect(result.current.user).toBe(null);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should login successfully', async () => {
    const { result } = renderHook(() => useAuth());
    
    // Wait for initial load
    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    act(() => {
      result.current.login('TestPlayer');
    });
    
    expect(result.current.user?.username).toBe('TestPlayer');
    expect(result.current.isAuthenticated).toBe(true);
  });

  it('should persist user to localStorage', async () => {
    const { result } = renderHook(() => useAuth());
    
    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    act(() => {
      result.current.login('TestPlayer');
    });
    
    const stored = localStorage.getItem('memory_game_user');
    expect(stored).toBe(JSON.stringify({ username: 'TestPlayer' }));
  });

  it('should logout successfully', async () => {
    const { result } = renderHook(() => useAuth());
    
    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    act(() => {
      result.current.login('TestPlayer');
    });
    
    act(() => {
      result.current.logout();
    });
    
    expect(result.current.user).toBe(null);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('should trim whitespace from username', async () => {
    const { result } = renderHook(() => useAuth());
    
    await vi.waitFor(() => {
      expect(result.current.isLoading).toBe(false);
    });
    
    act(() => {
      result.current.login('  Spaces  ');
    });
    
    expect(result.current.user?.username).toBe('Spaces');
  });
});

describe('useLeaderboard', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should start with empty entries', () => {
    const { result } = renderHook(() => useLeaderboard());
    expect(result.current.entries).toHaveLength(0);
  });

  it('should add entry to leaderboard', () => {
    const { result } = renderHook(() => useLeaderboard());
    
    act(() => {
      result.current.addEntry('Player1', 100, 2);
    });
    
    expect(result.current.entries).toHaveLength(1);
    expect(result.current.entries[0].username).toBe('Player1');
    expect(result.current.entries[0].score).toBe(100);
    expect(result.current.entries[0].round).toBe(2);
  });

  it('should sort entries by score descending', () => {
    const { result } = renderHook(() => useLeaderboard());
    
    act(() => {
      result.current.addEntry('Player1', 100, 1);
      result.current.addEntry('Player2', 300, 3);
      result.current.addEntry('Player3', 200, 2);
    });
    
    expect(result.current.entries[0].username).toBe('Player2');
    expect(result.current.entries[1].username).toBe('Player3');
    expect(result.current.entries[2].username).toBe('Player1');
  });

  it('should limit to 10 entries', () => {
    const { result } = renderHook(() => useLeaderboard());
    
    act(() => {
      for (let i = 0; i < 15; i++) {
        result.current.addEntry(`Player${i}`, i * 10, 1);
      }
    });
    
    expect(result.current.entries).toHaveLength(10);
    // Highest scores should be kept
    expect(result.current.entries[0].score).toBe(140);
  });

  it('should persist entries to localStorage', () => {
    const { result } = renderHook(() => useLeaderboard());
    
    act(() => {
      result.current.addEntry('Player1', 100, 1);
    });
    
    const stored = localStorage.getItem('memory_game_leaderboard');
    expect(stored).toBeTruthy();
    
    const parsed = JSON.parse(stored!);
    expect(parsed).toHaveLength(1);
  });

  it('should clear leaderboard', () => {
    const { result } = renderHook(() => useLeaderboard());
    
    act(() => {
      result.current.addEntry('Player1', 100, 1);
      result.current.clearLeaderboard();
    });
    
    expect(result.current.entries).toHaveLength(0);
  });
});
