const menuIconSelector = '[data-cy="menu-icon"]';
const menuSelector = '[data-cy="dropdown-menu"]';
const footerSelector = '[data-cy="footer-nav"]';

const openMenu = () => {
  /* First check if menu is already open */
  cy.get('body').then((body) => {
    if (body.find(menuSelector).length === 0) {
      cy.get(menuIconSelector).click();
    }
  });

  cy.get(menuSelector);
};

const navigateDropdownMenuItem = (el, title, pathname) => {
  openMenu();
  cy.contains(`${menuSelector} ${el}`, title).click();
  cy.location('pathname').should('eq', pathname);
};
const handleExternalLink = (title, url) => {
  openMenu();
  cy.contains(`${menuSelector} a`, title)
    .invoke('attr', 'href')
    .then((href) => {
      expect(href).to.equal(url);
    });
};

const handleTextLink = (title) => {
  cy.contains(`${footerSelector} a`, title)
    .invoke('attr', 'href')
    .then((href) => {
      cy.contains(`${footerSelector} a`, title).click();
      cy.location('pathname').should('eq', href);
    });
};

export class NavigationPage {
  logoLink() {
    // visit any other page first, then make sure logo links back to home page
    cy.visit('/terms');
    cy.get('[data-cy="cpr-logo"]').find('a').click();
    cy.location('pathname').should('eq', '/');
    return this;
  }
  aboutUsPage() {
    handleExternalLink('About us', 'https://climatepolicyradar.org');
    return this;
  }
  methodologyPage() {
    navigateDropdownMenuItem('a', 'Methodology', '/methodology');
    return this;
  }
  accountPage() {
    navigateDropdownMenuItem('a', 'My account', '/account');
    return this;
  }
  signOutPage() {
    navigateDropdownMenuItem('button', 'Sign out', '/auth/signin');
    return this;
  }
  footerLinkMethodology() {
    handleTextLink('Methodology');
    return this;
  }
  footerLinkTerms() {
    handleTextLink('Terms & conditions');
    return this;
  }
  footerLinkPrivacy() {
    handleTextLink('Privacy policy');
    return this;
  }
  footerLinkCookies() {
    handleTextLink('Cookies policy');
    return this;
  }
}
export const navigateTo = new NavigationPage();
