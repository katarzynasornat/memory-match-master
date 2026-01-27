import { useEffect } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

interface GameOverModalProps {
  isOpen: boolean;
  score: number;
  round: number;
  onPlayAgain: () => void;
  onSubmitScore: () => void;
}

export const GameOverModal = ({
  isOpen,
  score,
  round,
  onPlayAgain,
  onSubmitScore,
}: GameOverModalProps) => {
  // Auto-submit score when modal opens
  useEffect(() => {
    if (isOpen) {
      onSubmitScore();
    }
  }, [isOpen, onSubmitScore]);

  return (
    <Dialog open={isOpen}>
      <DialogContent className="neon-box-accent bg-card" hideCloseButton>
        <DialogHeader>
          <DialogTitle className="text-2xl font-display text-center text-accent">
            Game Over
          </DialogTitle>
          <DialogDescription className="text-center pt-4 space-y-2">
            <p className="text-lg text-foreground">
              You reached <span className="text-secondary font-display">Round {round}</span>
            </p>
            <p className="text-3xl font-display neon-text">
              {score} points
            </p>
          </DialogDescription>
        </DialogHeader>
        <div className="flex flex-col gap-2 mt-4">
          <p className="text-center text-success text-sm">
            ✓ Score submitted to leaderboard!
          </p>
          <Button
            onClick={onPlayAgain}
            className="w-full bg-primary hover:bg-primary/80 text-primary-foreground font-display"
          >
            Play Again
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};
