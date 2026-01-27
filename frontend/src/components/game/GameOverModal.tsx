import { useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';

interface GameOverModalProps {
  isOpen: boolean;
  score: number;
  round: number;
  onPlayAgain: () => void;
  onSubmitScore: () => void;
  submissionStatus: 'idle' | 'submitting' | 'success' | 'error';
}

export const GameOverModal = ({
  isOpen,
  score,
  round,
  onPlayAgain,
  onSubmitScore,
  submissionStatus,
}: GameOverModalProps) => {
  const submissionAttempted = useRef(false);

  // Auto-submit score when modal opens
  useEffect(() => {
    if (isOpen && !submissionAttempted.current && submissionStatus === 'idle') {
      submissionAttempted.current = true;
      onSubmitScore();
    }

    // Reset the ref when modal closes so it can submit again next game
    if (!isOpen) {
      submissionAttempted.current = false;
    }
  }, [isOpen, onSubmitScore, submissionStatus]);

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
        <div className="flex flex-col gap-4 mt-4">
          <div className="flex items-center justify-center gap-2 py-2 border-y border-border/50">
            {submissionStatus === 'submitting' && (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
                <span className="text-sm text-muted-foreground">Saving score...</span>
              </>
            )}
            {submissionStatus === 'success' && (
              <>
                <CheckCircle2 className="w-4 h-4 text-success" />
                <span className="text-sm text-success font-medium">Score saved to leaderboard!</span>
              </>
            )}
            {submissionStatus === 'error' && (
              <div className="flex flex-col items-center gap-2">
                <div className="flex items-center gap-2 text-destructive">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-sm font-medium">Failed to save score</span>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={onSubmitScore}
                  className="h-8 text-xs border-destructive/50 hover:bg-destructive/10"
                >
                  Retry Submission
                </Button>
              </div>
            )}
          </div>

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
