import { getError } from "../../utils/getError";

const emailInput = 'input[type="email"]';
const passwordInput = 'input[type="password"]';

export class SignInPage {
  signIn(email, password) {
    cy.get(emailInput).type(email);
    cy.get(passwordInput).type(password);
    cy.get('form').submit();
    return this;
  }
  enterEmail(email) {
    cy.get(emailInput).type(email);
    return this;
  }
  enterPassword(password) {
    cy.get(passwordInput).type(password);
    return this;
  }
  submitForm() {
    cy.get('form').submit();
    return this;
  }
  getEmailError() {
    return getError(emailInput);
  }
  getPasswordError() {
    return getError(passwordInput);
  }
}
export const signInPage = new SignInPage();
