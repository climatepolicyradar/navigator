/// <reference types="cypress" />

describe('Landing page', () => {
  before(() => {
    cy.login();
  });

  it('should see placeholder text which should clear after clicking input', () => {
    // wait for text animation to finish
    cy.wait(2000);

    cy.get('[data-cy="search-input"]')
      .invoke('attr', 'placeholder')
      .then((text) => {
        expect(text).to.equal('Search full text of 3000+ laws and policies');
      });
    cy.get('[data-cy="search-input"]')
      .click()
      .invoke('attr', 'placeholder')
      .then((phText) => {
        expect(phText).to.be.empty;
      });
  });
});
