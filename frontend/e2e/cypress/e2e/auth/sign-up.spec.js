import { signUpPage } from "../../support/page_objects/sign-up-page";

describe("Validate user sign up fields", () => {
  before("visit page", () => {
    cy.visit("/auth/sign-up");
  });
  beforeEach("visit page", () => {
    signUpPage.clearForm();
  });
  it("Logo should link to the CPR website", () => {
    cy.checkAuthPagesLogo();
  });
  it("Should not allow empty fields", () => {
    signUpPage.submitForm();
    signUpPage.getNamesError().should("have.text", "Full name is required");
    signUpPage.getOrgnisationError().should("have.text", "Organisation is required");
    signUpPage.getAffiliationError().should("have.text", "Affiliation type is required");
    signUpPage.getEmailError().should("have.text", "Email is required");
  });
});

describe("Validate user sign up links", () => {
  beforeEach("visit page", () => {
    cy.visit("/auth/sign-up");
  });
  it("should redirect to the sign in page", () => {
    cy.clickTextLink("Sign in");
    cy.location("pathname", { timeout: 1000 }).should("eq", "/auth/sign-in");
  });
});