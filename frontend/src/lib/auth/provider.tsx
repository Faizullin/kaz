'use client'


import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { User } from "@/lib/types/user";

interface UserContextProps {
  user: User | null;
  saveUserData: (userData: User | null) => void;
  removeUserData: (userData: User | null) => void;
}

const UserContext = createContext<UserContextProps>({
  user: null,
  saveUserData: () => {},
  removeUserData: () => {},
});

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  const saveUserData = (userData: User | null) => {
    setUser(userData);
  };

  const removeUserData = () => {
    setUser(null);
    localStorage.removeItem("user");
    localStorage.removeItem("token");
  }

  useEffect(() => {
    const token = localStorage.getItem('token')

    if (token) {
      fetch(`${process.env.NEXT_PUBLIC_BACKEND}/auth/users/me`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${JSON.parse(token).access_token}`,
          'ngrok-skip-browser-warning': 'true'
        },
      })
        .then(response => response.json())
        .then((data: User) => {
          setUser(data);
        })
        .catch(error => {
          console.error('Error fetching user data:', error);
          removeUserData();
        });
    }
  }, []);

  return (
    <UserContext.Provider value={{ user, saveUserData, removeUserData }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => useContext(UserContext);