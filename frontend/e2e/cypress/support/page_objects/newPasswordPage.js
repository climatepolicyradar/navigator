const passwordInput = '[data-cy="password"] input';
const confirmInput = '[data-cy="confirm-password"] input';

export class NewPasswordPage {
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
    return cy.get(passwordInput).next('.error');
  }
  getConfirmPasswordError() {
    return cy.get(confirmInput).next('.error');
  }
}
export const newPasswordPage = new NewPasswordPage();
