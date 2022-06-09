const $menuIconSelector = '[data-cy="menu-icon"]'
const $menuSelector = '[data-cy="dropdown-menu"]'

const openMenu = () => {
  cy.get($menuIconSelector).click();
  cy.get($menuSelector)
}

const navigateMenuItem = (el, title, pathname) => {
  openMenu();
  cy.contains(`${$menuSelector} ${el}`, title).click()
  cy.location('pathname').should('eq', pathname)
}
const handleExternalLink = (title, url) => {
  openMenu();
  cy.contains(`${$menuSelector} a`, title).invoke('attr', 'href').then(href => {
    expect(href).to.equal(url)
  })
}

export class NavigationPage {
  aboutUsPage() {
    handleExternalLink('About us', 'https://climatepolicyradar.org')

  }
  methodologyPage() {
    navigateMenuItem('a', 'Methodology', '/methodology')
    
  }
  accountPage() {
    navigateMenuItem('a', 'My account', '/account')
  }
  signOutPage() {
    navigateMenuItem('button', 'Sign out', '/auth/signin')
  }
}
export const navigateTo = new NavigationPage();
