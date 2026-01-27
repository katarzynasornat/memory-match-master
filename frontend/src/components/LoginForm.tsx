import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Gamepad2, Eye, EyeOff } from 'lucide-react';

interface LoginFormProps {
  onLogin: (email: string) => void;
}

const USERS_KEY = 'memory_game_users';

const getStoredUsers = (): Record<string, string> => {
  try {
    const stored = localStorage.getItem(USERS_KEY);
    return stored ? JSON.parse(stored) : {};
  } catch {
    return {};
  }
};

const saveUser = (email: string, password: string) => {
  const users = getStoredUsers();
  users[email.toLowerCase()] = password;
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
};

export const LoginForm = ({ onLogin }: LoginFormProps) => {
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');

  const validateEmail = (email: string): string | null => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) return 'Please enter a valid email address';
    return null;
  };

  const validatePassword = (pass: string): string | null => {
    if (pass.length < 4) return 'Password must be at least 4 characters';
    return null;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedEmail = email.trim();
    const users = getStoredUsers();

    const emailError = validateEmail(trimmedEmail);
    if (emailError) {
      setError(emailError);
      return;
    }

    const passwordError = validatePassword(password);
    if (passwordError) {
      setError(passwordError);
      return;
    }

    if (isSignUp) {
      // Sign Up flow
      if (users[trimmedEmail.toLowerCase()]) {
        setError('User with this email already exists');
        return;
      }
      if (password !== confirmPassword) {
        setError('Passwords do not match');
        return;
      }
      saveUser(trimmedEmail, password);
      onLogin(trimmedEmail);
    } else {
      // Login flow
      const storedPassword = users[trimmedEmail.toLowerCase()];
      if (!storedPassword) {
        setError('User not found. Please sign up first.');
        return;
      }
      if (storedPassword !== password) {
        setError('Incorrect password');
        return;
      }
      onLogin(trimmedEmail);
    }
  };

  const toggleMode = () => {
    setIsSignUp(!isSignUp);
    setError('');
    setPassword('');
    setConfirmPassword('');
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
            {isSignUp ? 'Create an account to start playing' : 'Sign in to continue your game'}
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="neon-box bg-card/50 p-6 space-y-4">
          <div className="space-y-2">
            <Label htmlFor="email" className="text-foreground">
              Email Address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="player@example.com"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setError('');
              }}
              className="bg-background border-border focus:border-primary"
              autoComplete="email"
              autoFocus
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-foreground">
              Password
            </Label>
            <div className="relative">
              <Input
                id="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError('');
                }}
                className="bg-background border-border focus:border-primary pr-10"
                autoComplete={isSignUp ? 'new-password' : 'current-password'}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {isSignUp && (
            <div className="space-y-2">
              <Label htmlFor="confirmPassword" className="text-foreground">
                Confirm Password
              </Label>
              <Input
                id="confirmPassword"
                type={showPassword ? 'text' : 'password'}
                placeholder="••••••••"
                value={confirmPassword}
                onChange={(e) => {
                  setConfirmPassword(e.target.value);
                  setError('');
                }}
                className="bg-background border-border focus:border-primary"
                autoComplete="new-password"
              />
            </div>
          )}

          {error && (
            <p className="text-sm text-destructive">{error}</p>
          )}

          <Button
            type="submit"
            className="w-full bg-primary hover:bg-primary/80 text-primary-foreground font-display text-lg py-6"
          >
            {isSignUp ? 'Create Account' : 'Sign In'}
          </Button>

          <div className="text-center">
            <button
              type="button"
              onClick={toggleMode}
              className="text-sm text-muted-foreground hover:text-primary transition-colors"
            >
              {isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up"}
            </button>
          </div>
        </form>

        {/* Rules */}
        <div className="text-center text-sm text-muted-foreground space-y-1">
          <p>🎯 Match all 8 pairs to win each round</p>
          <p>❌ Only 10 mistakes allowed per round</p>
          <p>🏆 Chain rounds for bonus points!</p>
        </div>
      </div>
    </div>
  );
};