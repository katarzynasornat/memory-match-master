import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

interface RoundCompleteModalProps {
  isOpen: boolean;
  round: number;
  onNextRound: () => void;
}

export const RoundCompleteModal = ({
  isOpen,
  round,
  onNextRound,
}: RoundCompleteModalProps) => {
  return (
    <Dialog open={isOpen} onOpenChange={() => {}}>
      <DialogContent className="neon-box bg-card">
        <DialogHeader>
          <DialogTitle className="text-2xl font-display text-center text-success">
            Round {round} Complete!
          </DialogTitle>
          <DialogDescription className="text-center pt-4">
            <p className="text-lg text-foreground">
              Amazing! You cleared all pairs!
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              +100 round bonus • +{50 * round} strike bonus
            </p>
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button
            onClick={onNextRound}
            className="w-full bg-primary hover:bg-primary/80 text-primary-foreground font-display"
          >
            Start Round {round + 1}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
