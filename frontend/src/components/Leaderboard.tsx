import { cn } from '@/lib/utils';
import type { LeaderboardEntry } from '@/hooks/useLeaderboard';
import { Trophy } from 'lucide-react';

interface LeaderboardProps {
  entries: LeaderboardEntry[];
  currentUser?: string;
}

export const Leaderboard = ({ entries, currentUser }: LeaderboardProps) => {
  if (entries.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <Trophy className="w-12 h-12 mx-auto mb-3 opacity-50" />
        <p>No scores yet. Be the first!</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {entries.map((entry, index) => (
        <div
          key={`${entry.email}-${entry.date}`}
          className={cn(
            'leaderboard-row',
            entry.email === currentUser && 'border border-primary/30'
          )}
        >
          <div className="flex items-center gap-3">
            <div
              className={cn(
                'rank-badge',
                index === 0 && 'rank-1',
                index === 1 && 'rank-2',
                index === 2 && 'rank-3',
                index > 2 && 'bg-muted text-muted-foreground'
              )}
            >
              {index + 1}
            </div>
            <div>
              <p className={cn(
                'font-medium',
                entry.email === currentUser && 'text-primary'
              )}>
                {entry.email}
              </p>
              <p className="text-xs text-muted-foreground">
                Round {entry.round}
              </p>
            </div>
          </div>
          <div className="text-right">
            <p className="font-display text-lg neon-text">{entry.score}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
