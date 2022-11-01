/// <reference types="cypress" />

import { Navigation } from "../../support/page_objects/NavigationConstructor";

describe("Site navigation", () => {
  before(() => {
    cy.visit("/");
  });

  it("Click each dropdown menu icon", () => {
    Navigation.aboutUsPage().methodologyPage();
  });
  it("Clicking logo should return to landing page", () => {
    Navigation.logoLink();
  });
  it("Click each footer link", () => {
    // Close cookie consent popup
    cy.get('[data-cy="cookie-consent-reject"]').click();
    Navigation.footerLinkMethodology().footerLinkTerms().footerLinkPrivacy();
  });
});
