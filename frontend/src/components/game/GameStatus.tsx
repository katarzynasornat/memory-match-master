import { cn } from '@/lib/utils';

interface GameStatusProps {
  score: number;
  round: number;
  failures: number;
  maxFailures: number;
}

export const GameStatus = ({ score, round, failures, maxFailures }: GameStatusProps) => {
  return (
    <div className="flex flex-wrap items-center justify-center gap-4 md:gap-8">
      {/* Score */}
      <div className="text-center">
        <p className="text-xs md:text-sm text-muted-foreground uppercase tracking-wider">Score</p>
        <p className="text-2xl md:text-3xl font-display neon-text">{score}</p>
      </div>

      {/* Round */}
      <div className="text-center">
        <p className="text-xs md:text-sm text-muted-foreground uppercase tracking-wider">Round</p>
        <p className="text-2xl md:text-3xl font-display text-secondary">{round}</p>
      </div>

      {/* Failures */}
      <div className="text-center">
        <p className="text-xs md:text-sm text-muted-foreground uppercase tracking-wider mb-1">Lives</p>
        <div className="flex gap-2 justify-center">
          {Array.from({ length: maxFailures }).map((_, index) => (
            <div
              key={index}
              className={cn(
                'failure-dot',
                index < failures && 'active'
              )}
              aria-label={index < failures ? 'Life lost' : 'Life remaining'}
            />
          ))}
        </div>
      </div>
    </div>
  );
};
