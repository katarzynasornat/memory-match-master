export interface User {
    id?: string;
    email: string;
}

export interface AuthResponse {
    user: User;
    token: string;
}

export interface LeaderboardEntry {
    email: string;
    score: number;
    round: number;
    date: string;
}

export interface LeaderboardEntryCreate {
    email: string;
    score: number;
    round: number;
    date?: string;
}
