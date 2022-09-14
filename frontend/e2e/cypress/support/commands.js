// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })

import 'cypress-file-upload';
import 'cypress-pseudo-localization';

Cypress.Commands.add('clickTextLink', (text) => {
  cy.contains('a', text)
    .invoke('attr', 'href')
    .then((href) => {
      cy.contains('a', text).click();
      cy.location('pathname').should('eq', href);
    });
});
Cypress.Commands.add('checkAuthPagesLogo', () => {
  cy.get('[data-cy="header-logo"]')
    .parent()
    .invoke('attr', 'href')
    .then((href) => {
      expect(href).to.equal('https://climatepolicyradar.org');
    });
});
Cypress.Commands.add('getAuthPageTitle', (text) => {
  cy.get('h2').should('have.text', text);
});

Cypress.Commands.add('submit_pdf_file', () => {
  cy.intercept('POST', 'document', { fixture: 'document' }).as('postDocument');

  cy.get('[data-cy="add-document-form"] input[name=name]').type(
    'Name of document'
  );
  cy.get('[data-cy="add-document-form"] select[name=language_id]').select(
    '193'
  );
  cy.get('[data-cy="add-document-form"]  input[type="file"]').attachFile(
    'somefile.pdf'
  );
  cy.get('[data-cy="add-document-form"] select[name=year]').select('2020');
  cy.get('[data-cy="submit-add-document-form"]').click();
});

Cypress.Commands.add('get_lookups', () => {
  cy.intercept('GET', 'sources', { fixture: 'sources' }).as('getSources');
  cy.intercept('GET', 'geographies', { fixture: 'geographies' }).as(
    'getGeographies'
  );
  cy.intercept('GET', 'languages', { fixture: 'languages' }).as('getLanguages');
  cy.visit('http://localhost:3000/add-action');
  cy.wait('@getSources');
  cy.wait('@getGeographies');
  cy.wait('@getLanguages');
});

Cypress.Commands.add('check_mobile_width', () => {
  // This ensures page content is not too wide for screen size

  // test with pseudo localisation (possibly longer words)
  cy.pseudoLocalize();
  cy.log('Pseudo localise');

  // Smallest mobile width (320) including a scrollbar (335)
  cy.viewport(335, 600);
  // should scroll horizontally if elements too wide
  cy.scrollTo(1000, 0);
  cy.window().its('scrollX').should('equal', 0);
  cy.stopPseudoLocalize;
});

Cypress.Commands.add('is_not_in_viewport', (element) => {
  cy.get(element).then(($el) => {
    const bottom = Cypress.$(cy.state('window')).height();
    const rect = $el[0].getBoundingClientRect();

    expect(rect.top).to.be.greaterThan(bottom);
    expect(rect.bottom).to.be.greaterThan(bottom);
    expect(rect.top).to.be.greaterThan(bottom);
    expect(rect.bottom).to.be.greaterThan(bottom);
  });
});

Cypress.Commands.add('is_in_viewport', (element) => {
  cy.get(element).then(($el) => {
    const bottom = Cypress.$(cy.state('window')).height();
    const rect = $el[0].getBoundingClientRect();

    expect(rect.top).not.to.be.greaterThan(bottom);
    expect(rect.bottom).not.to.be.greaterThan(bottom);
    expect(rect.top).not.to.be.greaterThan(bottom);
    expect(rect.bottom).not.to.be.greaterThan(bottom);
  });
});

Cypress.Commands.add('check_localisation', (page = '') => {
  cy.visit(`/${page}`);
  cy.get('[data-cy="banner-title"] span')
    .invoke('text')
    .then((titleEnglish) => {
      cy.visit(`/fr/${page}`);
      cy.get('[data-cy="banner-title"] span')
        .invoke('text')
        .should((titleFrench) => {
          expect(titleFrench).not.to.eq(titleEnglish);
        });
    });
  cy.visit(`/${page}`);
  cy.pseudoLocalize();
  cy.log('Pseudo localise');
  cy.stopPseudoLocalize;
});
