import { MemoryCard } from './MemoryCard';
import type { Card } from '@/hooks/useMemoryGame';

interface GameBoardProps {
  cards: Card[];
  onCardClick: (id: number) => void;
  isProcessing: boolean;
  isGameOver: boolean;
}

export const GameBoard = ({ cards, onCardClick, isProcessing, isGameOver }: GameBoardProps) => {
  return (
    <div className="grid grid-cols-4 gap-2 md:gap-4 max-w-md mx-auto">
      {cards.map(card => (
        <MemoryCard
          key={card.id}
          card={card}
          onClick={onCardClick}
          disabled={isProcessing || isGameOver}
        />
      ))}
    </div>
  );
};
