/// <reference types="cypress" />

describe('Check that language changes when changing localised url', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
  });
  it('Main page title should change when switching to a different localisation (fr)', () => {
    cy.check_localisation();
  });
  // it('Add Action page title should change when switching to a different localisation (fr)', () => {
  //   cy.check_localisation('add-action');
  // });
});
