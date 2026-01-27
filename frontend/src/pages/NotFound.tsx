import { useLocation } from "react-router-dom";
import { useEffect } from "react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="text-center space-y-6 animate-in fade-in zoom-in duration-500">
        <h1 className="game-title text-8xl">404</h1>
        <div className="space-y-2">
          <p className="text-2xl font-display text-white">Glitch in the matrix!</p>
          <p className="text-muted-foreground">The level you're looking for doesn't exist.</p>
        </div>
        <a
          href="/"
          className="inline-flex items-center justify-center px-8 py-3 rounded-full bg-primary text-black font-bold hover:bg-primary/80 transition-all glow-primary"
        >
          Back to Game
        </a>
      </div>
    </div>
  );
};

export default NotFound;
