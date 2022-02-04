/// <reference types="cypress" />

describe('Various tests to ensure responsiveness', () => {
  it('Home page should not be wider than viewport on smallest mobile screen', () => {
    cy.visit('http://localhost:3000');
    cy.check_mobile_width();
  });
  // Other pages will be added as they are created
});
