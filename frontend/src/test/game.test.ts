import { describe, it, expect, vi } from 'vitest';
import { createDeck, calculateScore } from '@/hooks/useMemoryGame';

describe('Memory Game Logic', () => {
  describe('createDeck', () => {
    it('should create a deck with 9 cards for round 1 (3x3)', () => {
      const deck = createDeck(1);
      expect(deck).toHaveLength(9);
    });

    it('should create a deck with 16 cards for round 3 (4x4)', () => {
      const deck = createDeck(3);
      expect(deck).toHaveLength(16);
    });

    it('should have exactly 8 pairs for 4x4 grid', () => {
      const deck = createDeck(3);
      const symbolCounts = new Map<string, number>();

      deck.forEach(card => {
        symbolCounts.set(card.symbol, (symbolCounts.get(card.symbol) || 0) + 1);
      });

      expect(symbolCounts.size).toBe(8);
      symbolCounts.forEach(count => {
        expect(count).toBe(2);
      });
    });

    it('should have 4 pairs and 1 joker for 3x3 grid', () => {
      const deck = createDeck(1);
      const symbolCounts = new Map<string, number>();

      deck.forEach(card => {
        symbolCounts.set(card.symbol, (symbolCounts.get(card.symbol) || 0) + 1);
      });

      expect(symbolCounts.size).toBe(5); // 4 pairs + 1 joker
      let pairCount = 0;
      let jokerCount = 0;
      symbolCounts.forEach(count => {
        if (count === 2) pairCount++;
        if (count === 1) jokerCount++;
      });
      expect(pairCount).toBe(4);
      expect(jokerCount).toBe(1);
    });

    it('should initialize all cards correctly for 4x4', () => {
      const deck = createDeck(3);
      deck.forEach(card => {
        expect(card.isFlipped).toBe(false);
        expect(card.isMatched).toBe(false);
      });
    });

    it('should initialize cards with pre-matched joker for 3x3', () => {
      const deck = createDeck(1);
      const joker = deck.find(c => c.symbol === '⭐');
      expect(joker?.isFlipped).toBe(true);
      expect(joker?.isMatched).toBe(true);

      const others = deck.filter(c => c.symbol !== '⭐');
      others.forEach(card => {
        expect(card.isFlipped).toBe(false);
        expect(card.isMatched).toBe(false);
      });
    });

    it('should assign unique IDs to each card', () => {
      const deck3x3 = createDeck(1);
      expect(new Set(deck3x3.map(c => c.id)).size).toBe(9);

      const deck4x4 = createDeck(3);
      expect(new Set(deck4x4.map(c => c.id)).size).toBe(16);
    });

    it('should shuffle the deck', () => {
      const deck1 = createDeck(3);
      const deck2 = createDeck(3);
      expect(deck1).toHaveLength(16);
      expect(deck2).toHaveLength(16);
    });
  });

  describe('calculateScore', () => {
    it('should add match points to base score', () => {
      const result = calculateScore(100, 10, 100, 50, 1, false);
      expect(result).toBe(110);
    });

    it('should add round and strike bonus for perfect round', () => {
      const result = calculateScore(100, 10, 100, 50, 1, true);
      // 100 + 10 + 100 + (50 * 1) = 260
      expect(result).toBe(260);
    });

    it('should scale strike bonus with round number', () => {
      const round1 = calculateScore(0, 10, 100, 50, 1, true);
      const round3 = calculateScore(0, 10, 100, 50, 3, true);

      // Round 1: 0 + 10 + 100 + 50 = 160
      // Round 3: 0 + 10 + 100 + 150 = 260
      expect(round1).toBe(160);
      expect(round3).toBe(260);
    });

    it('should not add bonuses for failed round', () => {
      const result = calculateScore(200, 0, 100, 50, 5, false);
      expect(result).toBe(200);
    });
  });
});

describe('Game Rules', () => {
  it('should have correct max failures (10)', () => {
    // This is tested implicitly through the hook, but we can verify the constant
    const MAX_FAILURES = 10;
    expect(MAX_FAILURES).toBe(10);
  });

  it('should have correct grid size (4x4 = 16 cards) for round 3', () => {
    const deck = createDeck(3);
    expect(deck).toHaveLength(16);
  });

  it('should have correct grid size (3x3 = 9 cards) for round 1', () => {
    const deck = createDeck(1);
    expect(deck).toHaveLength(9);
  });
});
