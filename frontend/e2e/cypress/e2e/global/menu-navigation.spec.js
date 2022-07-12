/// <reference types="cypress" />

import { navigateTo } from '../../support/page_objects/navigationPage';

describe('Site navigation', () => {
  beforeEach('login', () => {
    cy.login();
  });
  // it.only('figure out app actions, delete later', () => {
  //   cy.window().then(async (win) => {
  //     // console.log(win.queryClient.getQueryData('auth-user'));

  //     cy.visit('/account');
  //     await win.queryClient.getQueryData('auth-user');
  //     cy.wait(2000);
  //     console.log('change user');
  //     await win.queryClient.setQueryData('auth-user', {
  //       names: 'Another user name',
  //     });
  //     console.log(win.queryClient.getQueryData('auth-user'));
  //   });

  // });
  it('Click each dropdown menu icon', () => {
    navigateTo.aboutUsPage().methodologyPage().accountPage().signOutPage();
  });
  it('Click each footer link', () => {
    navigateTo
      .footerLinkMethodology()
      .footerLinkTerms()
      .footerLinkPrivacy()
      .footerLinkCookies();
  });
  it('Clicking logo should return to landing page', () => {
    navigateTo.logoLink();
  });
});
