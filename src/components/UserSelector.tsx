
import { useState } from 'react';
import { User } from '@/services/apiService';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Label } from "@/components/ui/label";

interface UserSelectorProps {
  users: User[];
  onSelectUser: (userId: number) => void;
}

const UserSelector = ({ users, onSelectUser }: UserSelectorProps) => {
  const handleChange = (value: string) => {
    onSelectUser(Number(value));
  };

  return (
    <div className="w-full md:w-80 mx-auto">
      <div className="space-y-2">
        <Label htmlFor="user-select">Select a user to get recommendations:</Label>
        <Select onValueChange={handleChange}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select a user" />
          </SelectTrigger>
          <SelectContent>
            {users.map((user) => (
              <SelectItem key={user.id} value={user.id.toString()}>
                {user.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
    </div>
  );
};

export default UserSelector;
