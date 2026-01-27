import { useState, useCallback, useEffect } from 'react';

export interface Card {
  id: number;
  symbol: string;
  isFlipped: boolean;
  isMatched: boolean;
}

export interface GameState {
  cards: Card[];
  failures: number;
  round: number;
  score: number;
  isGameOver: boolean;
  isRoundComplete: boolean;
  selectedCards: number[];
  isProcessing: boolean;
}

const SYMBOLS = ['🚀', '⚡', '🎮', '💎', '🔮', '🌟', '🎯', '🔥'];
const MAX_FAILURES = 3;
const ROUND_BONUS = 100;
const MATCH_POINTS = 10;
const STRIKE_BONUS = 50;

export const createDeck = (): Card[] => {
  const pairs = [...SYMBOLS, ...SYMBOLS];
  const shuffled = pairs.sort(() => Math.random() - 0.5);
  
  return shuffled.map((symbol, index) => ({
    id: index,
    symbol,
    isFlipped: false,
    isMatched: false,
  }));
};

export const calculateScore = (
  baseScore: number,
  matchPoints: number,
  roundBonus: number,
  strikeBonus: number,
  round: number,
  perfectRound: boolean
): number => {
  let score = baseScore + matchPoints;
  if (perfectRound) {
    score += roundBonus + (strikeBonus * round);
  }
  return score;
};

export const useMemoryGame = () => {
  const [gameState, setGameState] = useState<GameState>({
    cards: createDeck(),
    failures: 0,
    round: 1,
    score: 0,
    isGameOver: false,
    isRoundComplete: false,
    selectedCards: [],
    isProcessing: false,
  });

  const resetGame = useCallback(() => {
    setGameState({
      cards: createDeck(),
      failures: 0,
      round: 1,
      score: 0,
      isGameOver: false,
      isRoundComplete: false,
      selectedCards: [],
      isProcessing: false,
    });
  }, []);

  const startNextRound = useCallback(() => {
    setGameState(prev => ({
      ...prev,
      cards: createDeck(),
      failures: 0,
      isRoundComplete: false,
      selectedCards: [],
      isProcessing: false,
      score: prev.score + ROUND_BONUS + (STRIKE_BONUS * prev.round),
      round: prev.round + 1,
    }));
  }, []);

  const selectCard = useCallback((cardId: number) => {
    setGameState(prev => {
      if (prev.isProcessing || prev.isGameOver || prev.isRoundComplete) {
        return prev;
      }

      const card = prev.cards.find(c => c.id === cardId);
      if (!card || card.isFlipped || card.isMatched) {
        return prev;
      }

      if (prev.selectedCards.length >= 2) {
        return prev;
      }

      const newSelectedCards = [...prev.selectedCards, cardId];
      const newCards = prev.cards.map(c =>
        c.id === cardId ? { ...c, isFlipped: true } : c
      );

      if (newSelectedCards.length === 2) {
        return {
          ...prev,
          cards: newCards,
          selectedCards: newSelectedCards,
          isProcessing: true,
        };
      }

      return {
        ...prev,
        cards: newCards,
        selectedCards: newSelectedCards,
      };
    });
  }, []);

  // Process card matching after two cards are selected
  useEffect(() => {
    if (gameState.selectedCards.length !== 2 || !gameState.isProcessing) {
      return;
    }

    const [firstId, secondId] = gameState.selectedCards;
    const firstCard = gameState.cards.find(c => c.id === firstId);
    const secondCard = gameState.cards.find(c => c.id === secondId);

    if (!firstCard || !secondCard) return;

    const isMatch = firstCard.symbol === secondCard.symbol;

    const timer = setTimeout(() => {
      setGameState(prev => {
        if (isMatch) {
          const newCards = prev.cards.map(c =>
            c.id === firstId || c.id === secondId
              ? { ...c, isMatched: true }
              : c
          );

          const allMatched = newCards.every(c => c.isMatched);
          const newScore = prev.score + MATCH_POINTS;

          return {
            ...prev,
            cards: newCards,
            selectedCards: [],
            isProcessing: false,
            score: newScore,
            isRoundComplete: allMatched,
          };
        } else {
          const newCards = prev.cards.map(c =>
            c.id === firstId || c.id === secondId
              ? { ...c, isFlipped: false }
              : c
          );

          const newFailures = prev.failures + 1;
          const isGameOver = newFailures >= MAX_FAILURES;

          return {
            ...prev,
            cards: newCards,
            selectedCards: [],
            isProcessing: false,
            failures: newFailures,
            isGameOver,
          };
        }
      });
    }, 1000);

    return () => clearTimeout(timer);
  }, [gameState.selectedCards, gameState.isProcessing, gameState.cards]);

  return {
    ...gameState,
    selectCard,
    resetGame,
    startNextRound,
    maxFailures: MAX_FAILURES,
  };
};
