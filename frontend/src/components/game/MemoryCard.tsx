import { memo } from 'react';
import { cn } from '@/lib/utils';
import type { Card } from '@/hooks/useMemoryGame';

interface MemoryCardProps {
  card: Card;
  onClick: (id: number) => void;
  disabled: boolean;
}

export const MemoryCard = memo(({ card, onClick, disabled }: MemoryCardProps) => {
  const handleClick = () => {
    if (!disabled && !card.isFlipped && !card.isMatched) {
      onClick(card.id);
    }
  };

  return (
    <button
      onClick={handleClick}
      disabled={disabled || card.isFlipped || card.isMatched}
      className="card-container w-full aspect-square cursor-pointer disabled:cursor-default focus:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background rounded-2xl min-h-[80px] md:min-h-[120px]"
      aria-label={card.isFlipped || card.isMatched ? `Card showing ${card.symbol}` : 'Hidden card'}
    >
      <div
        className={cn(
          'card-inner',
          (card.isFlipped || card.isMatched) && 'flipped'
        )}
      >
        {/* Back of card */}
        <div className="card-face card-back">
          <span className="text-4xl md:text-5xl font-display text-secondary-foreground opacity-50">
            ?
          </span>
        </div>
        
        {/* Front of card */}
        <div
          className={cn(
            'card-face card-front',
            card.isMatched && 'card-matched'
          )}
        >
          <span className="text-5xl md:text-6xl">
            {card.symbol}
          </span>
        </div>
      </div>
    </button>
  );
});

MemoryCard.displayName = 'MemoryCard';
