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

Cypress.Commands.add('login', () => {
  cy.request({
    method: 'POST',
    url: 'http://localhost:8000/api/token',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: {
      grant_type: '',
      username: 'user@navigator.com',
      password: 'password',
      scope: '',
      client_id: 'test',
      client_secret: 'super_secret',
    },
  }).then((resp) => {
    window.localStorage.setItem('jwt', resp.body.access_token);
  });
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
  cy.intercept('GET', 'action_types', { fixture: 'action-types' }).as(
    'getActionTypes'
  );
  cy.intercept('GET', 'languages', { fixture: 'languages' }).as('getLanguages');
  cy.visit('http://localhost:3000/');
  cy.wait('@getSources');
  cy.wait('@getGeographies');
  cy.wait('@getActionTypes');
  cy.wait('@getLanguages');
});

Cypress.Commands.add('check_mobile_width', () => {
  // smallest mobile width (320) including a scrollbar (335)
  cy.viewport(335, 600);
  // should scroll horizontally if elements too wide
  cy.scrollTo(1000, 0);
  cy.window().its('scrollX').should('equal', 0);
});
