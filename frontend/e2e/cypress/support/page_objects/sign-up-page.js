import { getError } from "../../utils/getError";

const namesInput = 'input[name="names"]';
const organisationInput = 'input[name="affiliation_organisation"]';
const affiliationInput = 'select[name="affiliation_type"]';
const emailInput = 'input[name="email"]';

class SignUpPage {
  clearForm() {
    cy.get(namesInput).clear();
    cy.get(organisationInput).clear();
    cy.get(affiliationInput).select("");
    cy.get(emailInput).clear();
  }
  submitForm() {
    cy.get('form').submit();
    return this;
  }
  getNamesError() {
    return getError(namesInput);
  }
  getOrgnisationError() {
    return getError(organisationInput);
  }
  getAffiliationError() {
    return getError(affiliationInput);
  }
  getEmailError() {
    return getError(emailInput);
  }
}

export const signUpPage = new SignUpPage();
