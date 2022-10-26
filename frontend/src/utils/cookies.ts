export function getCookie(cname: string) {
  let name = cname + "=";
  let ca = document.cookie.split(';');
  for(let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

export function setCookie(cname: string, cvalue: string) {
  const d = new Date();
  let y = d.getFullYear() + 1;
  d.setFullYear(y);
  let expires = "expires="+d.toUTCString();
  // document.cookie = cname + "=" + cvalue + ";" + expires + "; domain=climatepolicyradar.org; path=/;";
  document.cookie = cname + "=" + cvalue + ";" + expires + "; path=/;";
}

export function deleteCookie(cname: string, domain: string) {
  let ca = document.cookie.split(';');
  if (!!cname && ca.includes(cname)) {
    document.cookie = `${cname}=; domain=${domain}; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;`;
  }
}

export function deleteCookies() {
  let ca = document.cookie.split(';');
  for (let index = 0; index < ca.length; index++) {
    const cookie = ca[index];
    const eqPos = cookie.indexOf("=");
    const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
    document.cookie = name +'=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  }
}
