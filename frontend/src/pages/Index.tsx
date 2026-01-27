import { useAuth } from '@/hooks/useAuth';
import { LoginForm } from '@/components/LoginForm';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';
import { Button } from '@/components/ui/button';

const Index = () => {
  const { user, isLoading, login, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (email: string) => {
    login(email);
    navigate('/game');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  // If already logged in, we still show a "Welcome" view as the user requested "always be the welcome page"
  if (user) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="w-full max-w-md space-y-8 text-center animate-in fade-in slide-in-from-bottom-8 duration-500">
          <div className="space-y-4">
            <h1 className="game-title text-4xl md:text-5xl">Welcome Back</h1>
            <p className="text-xl text-muted-foreground">
              You are signed in as <span className="text-primary font-bold">{user.email}</span>
            </p>
          </div>

          <div className="flex flex-col gap-4">
            <Button
              className="w-full py-8 text-2xl font-display bg-primary text-black hover:bg-primary/80 glow-primary transition-all hover:scale-105"
              onClick={() => navigate('/game')}
            >
              Start Playing
            </Button>

            <Button
              variant="outline"
              className="border-white/10 hover:bg-white/5"
              onClick={logout}
            >
              Sign Out / Switch Account
            </Button>
          </div>

          <div className="pt-8">
            <p className="text-sm text-muted-foreground italic">
              "The ultimate memory challenge awaits..."
            </p>
          </div>
        </div>
      </div>
    );
  }

  return <LoginForm onLogin={handleLogin} />;
};

export default Index;
