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
    <div className="grid grid-cols-4 gap-3 md:gap-5 w-full max-w-2xl mx-auto">
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
