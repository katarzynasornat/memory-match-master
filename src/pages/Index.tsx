import { useAuth } from '@/hooks/useAuth';
import { LoginForm } from '@/components/LoginForm';
import { GameScreen } from '@/components/GameScreen';

const Index = () => {
  const { user, isLoading, login, logout } = useAuth();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!user) {
    return <LoginForm onLogin={login} />;
  }

  return <GameScreen username={user.username} onLogout={logout} />;
};

export default Index;
