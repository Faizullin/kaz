export type UserRole = "admin" | "superadmin" | "student";

export type User = {
  id: string;
  fullname: string;
  email: string;
  phone: string;
  roles: UserRole[];
};
