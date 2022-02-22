/// <reference types="cypress" />

describe('Check that language changes when changing localised url', () => {
  it('Main page title should be in English', () => {
    // cy.intercept('/locales/en/search-start.json').as('English');
    cy.visit('http://localhost:3000');
    // cy.wait('@English');
    // cy.wait(500); // wait for translations to load
    cy.get('[data-cy="banner-title"] span')
      .invoke('text')
      .then((titleEnglish) => {
        // cy.log(titleEnglish);
        // expect(titleEnglish).not.to.equal('title');
        // cy.intercept('/locales/fr/search-start.json').as('French');
        cy.visit('http://localhost:3000/fr');
        // cy.wait('@French');
        // cy.wait(500); // wait for new translations to load
        cy.get('[data-cy="banner-title"] span')
          .invoke('text')
          .should((titleFrench) => {
            // expect(titleFrench).not.to.equal('title');
            expect(titleFrench).not.to.eq(titleEnglish);
          });
      });
  });
});
