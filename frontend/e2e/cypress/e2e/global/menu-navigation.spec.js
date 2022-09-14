/// <reference types="cypress" />

import { Navigation } from "../../support/page_objects/NavigationConstructor";

describe("Site navigation", () => {
  before(() => {
    cy.visit("/");
  });

  it("Click each dropdown menu icon", () => {
    Navigation.aboutUsPage().methodologyPage();
  });
  it("Click each footer link", () => {
    Navigation.footerLinkMethodology().footerLinkTerms().footerLinkPrivacy().footerLinkCookies();
  });
  it("Clicking logo should return to landing page", () => {
    Navigation.logoLink();
  });
});
