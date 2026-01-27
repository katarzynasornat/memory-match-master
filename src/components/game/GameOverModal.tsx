import { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

interface GameOverModalProps {
  isOpen: boolean;
  score: number;
  round: number;
  onPlayAgain: () => void;
  onSubmitScore: () => void;
  scoreSubmitted: boolean;
}

export const GameOverModal = ({
  isOpen,
  score,
  round,
  onPlayAgain,
  onSubmitScore,
  scoreSubmitted,
}: GameOverModalProps) => {
  const [hasSubmitted, setHasSubmitted] = useState(false);

  useEffect(() => {
    if (!isOpen) {
      setHasSubmitted(false);
    }
  }, [isOpen]);

  const handleSubmit = () => {
    onSubmitScore();
    setHasSubmitted(true);
  };

  return (
    <Dialog open={isOpen} onOpenChange={() => {}}>
      <DialogContent className="neon-box-accent bg-card">
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
        <DialogFooter className="flex-col gap-2 sm:flex-col">
          {!hasSubmitted && !scoreSubmitted && (
            <Button
              onClick={handleSubmit}
              className="w-full bg-secondary hover:bg-secondary/80"
            >
              Submit to Leaderboard
            </Button>
          )}
          {(hasSubmitted || scoreSubmitted) && (
            <p className="text-center text-success text-sm">
              ✓ Score submitted!
            </p>
          )}
          <Button
            onClick={onPlayAgain}
            variant="outline"
            className="w-full border-primary text-primary hover:bg-primary hover:text-primary-foreground"
          >
            Play Again
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
