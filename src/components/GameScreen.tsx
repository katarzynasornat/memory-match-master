import { useState } from 'react';
import { useMemoryGame } from '@/hooks/useMemoryGame';
import { useLeaderboard } from '@/hooks/useLeaderboard';
import { GameBoard } from './game/GameBoard';
import { GameStatus } from './game/GameStatus';
import { GameOverModal } from './game/GameOverModal';
import { RoundCompleteModal } from './game/RoundCompleteModal';
import { Leaderboard } from './Leaderboard';
import { Button } from '@/components/ui/button';
import { LogOut, Trophy, RotateCcw } from 'lucide-react';

interface GameScreenProps {
  username: string;
  onLogout: () => void;
}

export const GameScreen = ({ username, onLogout }: GameScreenProps) => {
  const game = useMemoryGame();
  const { entries, addEntry } = useLeaderboard();
  const [scoreSubmitted, setScoreSubmitted] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  const handleSubmitScore = () => {
    addEntry(username, game.score, game.round);
    setScoreSubmitted(true);
  };

  const handlePlayAgain = () => {
    game.resetGame();
    setScoreSubmitted(false);
  };

  return (
    <div className="min-h-screen flex flex-col p-4">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div>
          <h1 className="game-title text-2xl md:text-3xl">Memory</h1>
          <p className="text-sm text-muted-foreground">
            Playing as <span className="text-primary">{username}</span>
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setShowLeaderboard(!showLeaderboard)}
            className="text-muted-foreground hover:text-foreground"
            title="Leaderboard"
          >
            <Trophy className="w-5 h-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={handlePlayAgain}
            className="text-muted-foreground hover:text-foreground"
            title="Restart"
          >
            <RotateCcw className="w-5 h-5" />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={onLogout}
            className="text-muted-foreground hover:text-foreground"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col lg:flex-row gap-6 max-w-6xl mx-auto w-full">
        {/* Game Area */}
        <div className="flex-1 flex flex-col">
          {/* Game Status */}
          <div className="mb-6">
            <GameStatus
              score={game.score}
              round={game.round}
              failures={game.failures}
              maxFailures={game.maxFailures}
            />
          </div>

          {/* Game Board */}
          <div className="flex-1 flex items-center justify-center">
            <GameBoard
              cards={game.cards}
              onCardClick={game.selectCard}
              isProcessing={game.isProcessing}
              isGameOver={game.isGameOver}
            />
          </div>
        </div>

        {/* Leaderboard Sidebar (Desktop) or Toggle (Mobile) */}
        {showLeaderboard && (
          <aside className="lg:w-80 neon-box bg-card/50 p-4 rounded-lg">
            <h2 className="font-display text-xl mb-4 flex items-center gap-2">
              <Trophy className="w-5 h-5 text-warning" />
              Leaderboard
            </h2>
            <Leaderboard entries={entries} currentUser={username} />
          </aside>
        )}
      </main>

      {/* Modals */}
      <GameOverModal
        isOpen={game.isGameOver}
        score={game.score}
        round={game.round}
        onPlayAgain={handlePlayAgain}
        onSubmitScore={handleSubmitScore}
        scoreSubmitted={scoreSubmitted}
      />

      <RoundCompleteModal
        isOpen={game.isRoundComplete}
        round={game.round}
        onNextRound={game.startNextRound}
      />
    </div>
  );
};
