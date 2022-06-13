export class SignInPage {
  signIn(email, password) {
    cy.get('input[type="email"]').type(email);
    cy.get('input[type="password"]').type(password);
    cy.get('form').submit();
    return this;
  }
  enterEmail(email) {
    cy.get('input[type="email"]').type(email);
    return this;
  }
  enterPassword(password) {
    cy.get('input[type="password"]').type(password);
    return this;
  }
  submitForm() {
    cy.get('form').submit();
    return this;
  }
  getEmailError() {
    return cy.get('input[type="email"]').next('.error');
  }
  getPasswordError() {
    return cy.get('input[type="password"]').next('.error');
  }
}
export const signInPage = new SignInPage();
