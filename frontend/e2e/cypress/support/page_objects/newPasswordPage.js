import { getError } from "../../utils/getError";

const passwordInput = '[data-cy="password"] input';
const confirmInput = '[data-cy="confirm-password"] input';

export class NewPasswordPage {
  clearForm() {
    cy.get(passwordInput).clear();
    cy.get(confirmInput).clear();
  }
  enterPassword(password) {
    cy.get(passwordInput).type(password);
    return this;
  }
  confirmPassword(password) {
    cy.get(confirmInput).type(password);
    return this;
  }
  submitForm() {
    cy.get('form').submit();
    return this;
  }

  getPasswordError() {
    return getError(passwordInput);
  }
  getConfirmPasswordError() {
    return getError(confirmInput);
  }
}
export const newPasswordPage = new NewPasswordPage();
