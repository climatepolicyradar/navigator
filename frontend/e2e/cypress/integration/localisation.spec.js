/// <reference types="cypress" />

describe('Check that language changes when changing localised url', () => {
  it('Main page title should be in English', () => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="banner-title"] span')
      .invoke('text')
      .then((titleEnglish) => {
        cy.visit('http://localhost:3000/fr');
        cy.get('[data-cy="banner-title"] span')
          .invoke('text')
          .should((titleFrench) => {
            expect(titleFrench).not.to.eq(titleEnglish);
          });
      });
  });
});
