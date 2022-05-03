/// <reference types="cypress" />

describe('Various tests to ensure responsiveness', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
  });
  it('Home page should not be wider than viewport on smallest mobile screen', () => {
    cy.visit('http://localhost:3000');
    cy.check_mobile_width();
  });
  // it('Add Action page should not be wider than viewport on smallest mobile screen', () => {
  //   cy.visit('http://localhost:3000/add-action');
  //   cy.check_mobile_width();
  // });
  // Other pages will be added as they are created
});
