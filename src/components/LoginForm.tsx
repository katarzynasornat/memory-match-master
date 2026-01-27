import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Gamepad2 } from 'lucide-react';

interface LoginFormProps {
  onLogin: (username: string) => void;
}

export const LoginForm = ({ onLogin }: LoginFormProps) => {
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmed = username.trim();
    
    if (trimmed.length < 2) {
      setError('Username must be at least 2 characters');
      return;
    }
    
    if (trimmed.length > 15) {
      setError('Username must be 15 characters or less');
      return;
    }
    
    onLogin(trimmed);
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md space-y-8">
        {/* Logo */}
        <div className="text-center space-y-4">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl neon-box-secondary bg-card animate-float">
            <Gamepad2 className="w-10 h-10 text-secondary" />
          </div>
          <h1 className="game-title">Memory</h1>
          <p className="text-muted-foreground">
            Test your memory with this classic card game
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="neon-box bg-card/50 p-6 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="username" className="text-foreground">
              Enter your name
            </Label>
            <Input
              id="username"
              type="text"
              placeholder="Player1"
              value={username}
              onChange={(e) => {
                setUsername(e.target.value);
                setError('');
              }}
              className="bg-background border-border focus:border-primary"
              autoComplete="off"
              autoFocus
            />
            {error && (
              <p className="text-sm text-destructive">{error}</p>
            )}
          </div>
          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/80 text-primary-foreground font-display text-lg py-6"
          >
            Start Playing
          </Button>
        </form>

        {/* Rules */}
        <div className="text-center text-sm text-muted-foreground space-y-1">
          <p>🎯 Match all 8 pairs to win each round</p>
          <p>❌ Only 3 mistakes allowed per round</p>
          <p>🏆 Chain rounds for bonus points!</p>
        </div>
      </div>
    </div>
  );
};
