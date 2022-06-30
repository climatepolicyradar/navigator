import { newPasswordPage } from '../../support/page_objects/newPasswordPage';

describe('Validate reset password page fields', () => {
  before('visit page', () => {
    cy.visit('/auth/reset-password');
  });
  beforeEach('visit page', () => {
    newPasswordPage.clearForm();
  });
  it('Logo should link to the CPR website', () => {
    cy.checkAuthPagesLogo();
  });
  it('Title should be Reset your password', () => {
    cy.getAuthPageTitle('Reset your password');
  });
  it('should not allow empty password', () => {
    newPasswordPage.submitForm();
    newPasswordPage
      .getPasswordError()
      .should('have.text', 'Password is required');
  });
  it('should not allow less than 8 characters', () => {
    newPasswordPage.enterPassword('1234').submitForm();
    newPasswordPage.getPasswordError().should('have.text', 'Minimum 8 chars');
  });
  it('should not allow less than 8 characters', () => {
    newPasswordPage.enterPassword('1234567').submitForm();
    newPasswordPage.getPasswordError().should('have.text', 'Minimum 8 chars');
  });
  it('should make sure passwords match', () => {
    newPasswordPage.enterPassword('1234').confirmPassword('1111').submitForm();
    newPasswordPage
      .getConfirmPasswordError()
      .should('have.text', 'Passwords must match');
  });
});
