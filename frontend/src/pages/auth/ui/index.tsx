import { UserCredentialsDTO, signUp } from "@/shared/api/auth";
import { SubmitHandler, useForm } from "react-hook-form";
import styles from "./styles.module.scss";

export const Auth = () => {
  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<UserCredentialsDTO>();

  const onSubmit: SubmitHandler<UserCredentialsDTO> = async (
    values: UserCredentialsDTO
  ) => {
    try {
      const { data } = await signUp(values);
      console.log(data);
    } catch (e: any) {
      if (e.response.status === 400) {
        setError("username", { message: e.response.data.detail });
      }
    }
  };
  return (
    <div className={styles["sign-up"]}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <input
          className={styles["input"]}
          type="text"
          {...register("username")}
        />
        <input
          className={styles["input"]}
          type="password"
          {...register("password")}
        />
        {errors.username && <p>{errors.username.message}</p>}
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};
