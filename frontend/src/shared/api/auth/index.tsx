import { api } from "..";

export type UserCredentialsDTO = {
  username: "";
  password: "";
};

export const signUp = (body: UserCredentialsDTO) => api.post("/register", body);
