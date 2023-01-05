const menuIconSelector = '[data-cy="menu-icon"]';
const menuSelector = '[data-cy="dropdown-menu"]';
const footerSelector = '[data-cy="footer-nav"]';

const openMenu = () => {
  /* First check if menu is already open */
  cy.get("body").then((body) => {
    if (body.find(menuSelector).length === 0) {
      cy.get(menuIconSelector).click();
    }
  });

  cy.get(menuSelector);
};

const navigateDropdownMenuItem = (el, title, pathname) => {
  openMenu();
  cy.contains(`${menuSelector} ${el}`, title).click();
  // timeout will not 'wait' but it should account for any lag
  cy.location("pathname", { timeout: 10000 }).should("eq", pathname);
};

const handleMenuExternalLink = (title, url) => {
  openMenu();
  cy.contains(`${menuSelector} a`, title)
    .invoke("attr", "href")
    .then((href) => {
      expect(href).to.equal(url);
    });
};

const handleFooterExternalLink = (title, url) => {
  cy.contains(`${footerSelector} a`, title)
    .invoke("attr", "href")
    .then((href) => {
      expect(href).to.equal(url);
    });
};

const handleFooterTextLink = (title) => {
  cy.contains(`${footerSelector} a`, title)
    .invoke("attr", "href")
    .then((href) => {
      cy.contains(`${footerSelector} a`, title).click();
      cy.location("pathname").should("eq", href);
    });
};

export class NavigationConstructor {
  logoLink() {
    // visit any other page first, then make sure logo links back to home page
    cy.visit("/terms-of-use");
    cy.get('[data-cy="cpr-logo"]').find("a").click();
    cy.location("pathname").should("eq", "/");
    return this;
  }
  aboutUsPage() {
    handleMenuExternalLink("About us", "https://climatepolicyradar.org");
    return this;
  }
  methodologyPage() {
    handleMenuExternalLink("Methodology", "https://github.com/climatepolicyradar/methodology");
    return this;
  }
  footerLinkMethodology() {
    handleFooterExternalLink("Methodology", "https://github.com/climatepolicyradar/methodology");
    return this;
  }
  footerLinkTerms() {
    handleFooterExternalLink("Terms & conditions", "/terms-of-use");
    return this;
  }
  footerLinkPrivacy() {
    handleFooterExternalLink("Privacy policy", "https://climatepolicyradar.org/privacy-policy");
    return this;
  }
  footerLinkCookies() {
    handleFooterTextLink("Cookies policy");
    return this;
  }
}
export const Navigation = new NavigationConstructor();
