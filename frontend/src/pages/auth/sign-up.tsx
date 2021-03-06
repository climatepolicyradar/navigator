import { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { useTranslation } from "react-i18next";
import { useForm } from "react-hook-form";
import * as Yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import Link from "next/link";
import { useAuth } from "@api/auth";
import { signUp, TSignUp } from "@api/index";
import LoaderOverlay from "@components/LoaderOverlay";
import Layout from "@components/layouts/Auth";
import AuthWrapper from "@components/auth/AuthWrapper";
import TextInput from "@components/form-inputs/TextInput";
import Select from "@components/form-inputs/Select";
import Button from "@components/buttons/Button";
import { affiliation_types } from "@constants/formOptions";

const SignUp = () => {
  const router = useRouter();
  const [status, setStatus] = useState(null);
  const { t } = useTranslation("auth");
  const { user } = useAuth();

  // redirect if already signed in
  useEffect(() => {
    if (user?.email) router.push("/");
  }, [user]);

  const schema = Yup.object({
    names: Yup.string().required(t("Full name is required")),
    affiliation_organisation: Yup.string().required(t("Organisation is required")),
    affiliation_type: Yup.string().required(t("Affiliation type is required")),
    email: Yup.string().email(t("Invalid email format")).required(t("Email is required")),
  });

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors, isSubmitSuccessful },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const submitForm = async (data: TSignUp) => {
    const newData = {
      names: data.names,
      affiliation_organisation: data.affiliation_organisation,
      affiliation_type: data.affiliation_type,
      email: data.email,
    };
    const status = await signUp(newData);
    setStatus(status);
  };

  const formSubmitted = isSubmitSuccessful && status?.data === true;

  const welcomeMessage = formSubmitted
    ? t("Please check your email and click the enclosed link to complete the sign up.")
    : t("Please fill in your details to get access, and we will send over an activation link shortly.");

  const heading = formSubmitted ? t("Sign up complete") : t("Sign up for an account");

  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={t("Sign up for an account")} height={1000}>
          <div className="container py-4">
            <AuthWrapper heading={heading} description={welcomeMessage}>
              {status?.error && <p className="text-red-500 font-bold mt-4">{status.error}</p>}

              {!isSubmitSuccessful && status?.data !== true && (
                <form className="w-full" onSubmit={handleSubmit(submitForm)} noValidate>
                  <div data-cy="signup-names" className="form-row text-white">
                    <TextInput label={t("Full name")} name="names" type="text" errors={errors} required register={register} placeholder={t("First and surname")} />
                  </div>
                  <div data-cy="signup-affiliation_organisation" className="form-row text-white">
                    <TextInput
                      label={t("Organisation/Affiliation")}
                      name="affiliation_organisation"
                      type="text"
                      errors={errors}
                      required
                      register={register}
                      placeholder={t("Organisation")}
                    />
                  </div>
                  <div data-cy="signup-affiliation_type" className="form-row text-white">
                    <Select label={t("Affiliation type")} name="affiliation_type" errors={errors} required register={register}>
                      <option value="">{t("Choose a type")}</option>
                      {affiliation_types.map((type, index) => (
                        <option key={`afftype${index}`} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </Select>
                  </div>
                  <div data-cy="signup-email" className="form-row text-white">
                    <TextInput label={t("Email")} name="email" type="email" errors={errors} required register={register} placeholder={t("Email address")} />
                  </div>
                  <div data-cy="signup-submit" className="form-row">
                    <Button type="submit" color="light" disabled={isSubmitting} extraClasses="w-full mt-8" fullWidth>
                      {t("Sign up")}
                    </Button>
                  </div>
                </form>
              )}
              <p className="mt-8 text-white text-center">
                {t("Already have an account?")} &nbsp;
                <Link href="/auth/sign-in">
                  <a className="text-blue-500 hover:text-white transition duration-300">{t("Sign in")}</a>
                </Link>
              </p>
            </AuthWrapper>
          </div>
        </Layout>
      )}
    </>
  );
};

export default SignUp;
