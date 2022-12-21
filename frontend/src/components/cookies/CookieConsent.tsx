import { useEffect, useState } from "react";
import Script from "next/script";
import Button from "@components/buttons/Button";
import { getCookie, setCookie } from "@utils/cookies";
import { COOKIE_CONSENT_NAME } from "@constants/cookies";
import { ExternalLink } from "@components/ExternalLink";

export const CookieConsent = () => {
  const [hide, setHide] = useState(true);
  const [enableAnalytics, setEnableAnalytics] = useState(false);
  const [hotjar, setHotjar] = useState(false);

  useEffect(() => {
    const cc = getCookie(COOKIE_CONSENT_NAME);
    if (!cc) setHide(false);
    if (cc === "true") setEnableAnalytics(true);
  }, []);

  useEffect(() => {
    // If the user has accepted cookies, enable Google Tag Manager
    // and Hotjar
    if (enableAnalytics) {
      setHotjar(true);
      (function (w, d, s, l, i) {
        w[l] = w[l] || [];
        w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
        var f = d.getElementsByTagName(s)[0],
          j = d.createElement(s) as HTMLScriptElement,
          dl = l != "dataLayer" ? "&l=" + l : "";
        j.async = true;
        j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
        f.parentNode.insertBefore(j, f);
      })(window, document, "script", "dataLayer", "GTM-NTNH983");
    }
  }, [enableAnalytics]);

  const cookiesAcceptHandler = () => {
    setCookie(COOKIE_CONSENT_NAME, "true");
    setHide(true);
    setEnableAnalytics(true);
  };

  const cookiesRejectHandler = () => {
    setCookie(COOKIE_CONSENT_NAME, "false");
    setHide(true);
  };

  return (
    <>
      <div data-cy="cookie-consent" className={`${hide ? "hidden" : ""} fixed w-[90%] max-w-[600px] bottom-6 left-1/2 translate-x-[-50%] z-[9999] rounded-xl bg-blue-100`}>
        <div className="py-4 px-6">
          <h3 className="">Cookies and your privacy</h3>
          <p className="text-content text-sm">
            We take your trust and privacy seriously. Climate Policy Radar uses cookies to make our site work optimally, analyse traffic to our website and improve your experience.
            Read our <ExternalLink url="https://climatepolicyradar.org/privacy-policy">privacy and cookie policy</ExternalLink> to learn more. By accepting cookies you will help us
            make our site better, but you can reject them if you wish.
          </p>
          <div className="flex justify-end">
            <div className="">
              <Button color="light-hover-dark" thin onClick={cookiesAcceptHandler} data-cy="cookie-consent-accept">
                Accept
              </Button>
            </div>
            <div className="ml-4">
              <Button color="clear" thin onClick={cookiesRejectHandler} data-cy="cookie-consent-reject">
                Reject
              </Button>
            </div>
          </div>
        </div>
      </div>
      {enableAnalytics && <Script id="google-tag-manager" async src={`https://www.googletagmanager.com/gtm.js?id=GTM-NTNH983`} />}
      {hotjar && (
        <Script id="hotjar" strategy="afterInteractive">
          {`
            (function(h,o,t,j,a,r){
              h.hj=h.hj||function(){(h.hj.q=h.hj.q||[]).push(arguments)};
              h._hjSettings={hjid:3192374,hjsv:6};
              a=o.getElementsByTagName('head')[0];
              r=o.createElement('script');r.async=1;
              r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
              a.appendChild(r);
            })(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
          `}
        </Script>
      )}
    </>
  );
};
