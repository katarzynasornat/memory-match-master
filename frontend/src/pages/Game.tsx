import { useAuth } from '@/hooks/useAuth';
import { GameScreen } from '@/components/GameScreen';
import { useNavigate } from 'react-router-dom';
import { useEffect } from 'react';

const Game = () => {
    const { user, token, isLoading, logout } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (!isLoading && !user) {
            navigate('/');
        }
    }, [user, isLoading, navigate]);

    if (isLoading || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <GameScreen
            email={user.email}
            token={token}
            onLogout={() => {
                logout();
                navigate('/');
            }}
        />
    );
};

export default Game;
